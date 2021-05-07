import asyncio
import json
import logging
import random
import re
import time as tm

import discord
from discord import utils
from discord.ext import commands

from config import *
from entities.quiz import Quiz
from entities.recorder import Recorder


class EqualizerBot(commands.Bot):
    def __init__(self, command_prefix=COMMAND_PREFIX, self_bot=False, intents=None):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot, intents=intents)
        self.battles = {}
        self.broadcast_channel = None
        self.admin_channel = None
        self.info_channel = None
        self.question_base = EqualizerBot.load_questions()
        self.start_messages = {}
        self.recorder = Recorder(PATH_TO_STAT_FILE, self.question_base)
        logging.info(self.intents.members)
        self.link_commands()

    async def on_ready(self):
        self.broadcast_channel = await self.fetch_channel(BROADCAST_CHANNEL)
        self.admin_channel = await self.fetch_channel(ADMIN_CHANNEL)
        self.info_channel = await self.fetch_channel(INFO_CHANNEL)
        logging.info(f"Bot creation - succeed. Logged as {self.user}")

    def link_commands(self):

        @self.command(name=INFO_COMMAND, pass_context=True)
        async def info(ctx):
            logging.info(f"Passed help command with context - {ctx}")
            ans = "Existing commands:\n"
            for st in COMMANDS:
                ans += st + '\n'
            await ctx.channel.send(ans)

        @self.command(name=CREATE_BATTLE_COMMAND, pass_context=True)
        async def start_battle(ctx, *args):
            if ctx.channel.id == ADMIN_CHANNEL:
                try:
                    parsed_args = EqualizerBot.parse_arguments([*args])
                    parsed_args[TOPICS_ACCESSOR] = await EqualizerBot.get_topics(ctx)
                except ValueError:
                    logging.info(WRONG_ARGUMENTS_START)
                    await self.send_admin(WRONG_ARGUMENTS_START)
                    return
                except Exception as e:
                    logging.info(e)
                    return
                logging.info(f"Starting battle with arguments {parsed_args}")
                role = await self.crate_arena_role(ctx.guild)
                text_channel = await self.create_battle_channel(ctx.guild, role)
                players = await self.get_players(text_channel, parsed_args[TOPICS_ACCESSOR], SECONDS_TO_JOIN)
                if len(players) == 0:
                    # not enough players
                    s = f"Stopped battle in {text_channel.name}. No players."
                    logging.info(s)
                    await self.send_admin(s)
                    return
                await self.give_role(players, role)
                new_battle = Quiz(
                    text_channel.id,
                    ctx.me, players,
                    parsed_args[TOPICS_ACCESSOR],
                    self.question_base,
                    parsed_args[ANSWER_TIME_ACCESSOR],
                    parsed_args[QUESTION_AMOUNT_ACCESSOR]
                )
                self.battles[new_battle.cid] = [new_battle, text_channel, role]
                try:
                    await self.launch_game(new_battle)
                    if new_battle.state.game_ended:
                        await self.record_results(new_battle)
                except Exception as e:
                    logging.info(f"Game {new_battle.cid} stopped by exception {e}.")
                    if new_battle.cid in self.battles:
                        await self.admin_channel.send(BATTLE_STOPPED_AND_WHY % (text_channel.name, e))
                        self.battles[new_battle.cid][0].state.game_in_progress = False

        @self.command(name=CLEAN_ALL_COMMAND, pass_context=True)
        async def clean_all(ctx):
            if ctx.channel.id == ADMIN_CHANNEL:
                logging.info("Cleaning all info.")
                for battle, attrs in self.battles.items():
                    await attrs[1].delete()
                    await attrs[2].delete()
                    logging.info(f"{attrs[1]} was deleted.")
                self.battles.clear()
            else:
                await ctx.reply("Nice try you dummy.")

        @self.command(name=DELETE_BATTLE_COMMAND, pass_context=True)
        async def clean_arena(ctx, *args):
            if ctx.channel.id == ADMIN_CHANNEL:
                arguments = [*args]
                logging.info(f"Got arguments to delete: {arguments}")
                if len(arguments) > 0:
                    for a in arguments:
                        cid = int(re.match(CHANNEL_LINK_REGEX, a).group(1))
                        ch = await self.fetch_channel(cid)
                        logging.info(f"Deleting channel {ch} with {cid} id.")
                        if ch is not None and ch.id in self.battles:
                            await self.clean_game(cid)

        @self.command(name="ping", pass_context=True)
        async def pong(ctx, *arg):
            await ctx.channel.send(f"Pong {[*arg]}")

        @self.command(name=GET_PLAYER_INFO_COMMAND, pass_context=True)
        async def get_player_info(ctx):
            ans = ""
            for user in ctx.message.mentions:
                ans += self.recorder.get_player(user.id) + '\n'
            await self.admin_channel.send(ans)

    async def send_admin(self, message: str):
        await self.admin_channel.send(message)

    @staticmethod
    async def get_topics(ctx):
        s = ""
        for emo, topic in QUESTION_EMOJI_DICT.items():
            s += f"- {emo} is {topic}.\n"
        message_string = TOPICS_SELECTION_MESSAGE % s
        mes = await ctx.reply(message_string, mention_author=True)
        for emo in QUESTION_EMOJI:
            await mes.add_reaction(emo)
        t0 = tm.time()
        selecting = True
        while True:
            message = await ctx.channel.fetch_message(mes.id)
            logging.info(message.reactions)
            for r in message.reactions:
                if r.emoji in QUESTION_EMOJI and r.count > 1:
                    selecting = False
                    break
            if not selecting:
                break
            if tm.time() - t0 > TOPIC_CHOOSING:
                raise ValueError
            await asyncio.sleep(3)
        message = await ctx.channel.fetch_message(mes.id)
        ans = []
        for r in message.reactions:
            if r.emoji in QUESTION_EMOJI and r.count > 1:
                ans.append(QUESTION_EMOJI_DICT[r.emoji])
        logging.info(f"Got topics {ans}")
        return ans

    @staticmethod
    def parse_arguments(args):
        parsed = {
            ANSWER_TIME_ACCESSOR: ANSWER_TIME,
            QUESTION_AMOUNT_ACCESSOR: DEFAULT_QUESTIONS_AMOUNT
        }
        for i in range(len(args)):
            if args[i].startswith("-") and args[i] in ARGS_FLAGS:
                parsed[ARGS_FLAGS[args[i]]] = int(args[i + 1])
        logging.info(f"Parsed arguments {parsed}")
        return parsed

    async def get_players(self, channel, topics, time=15):
        players = []
        info = TOPICS_SEQUENCE % (",".join(topics))
        message = await self.broadcast_invite(channel, time, info)
        logging.info(f"Sent invite for {channel.name}.")
        await message.add_reaction(JOIN_EMOJI)
        await asyncio.sleep(time)
        message = await self.broadcast_channel.fetch_message(message.id)
        if join_react := message.reactions[0]:
            async for user in join_react.users():
                if user.id == BOT_ID:
                    continue
                players.append(user.id)
        players = await self.get_members_with_id(players)
        logging.info(f"List of players to join - {players}")
        return players

    async def get_members_with_id(self, ids: list):
        members = []
        # bad code
        for i in ids:
            # members.append(utils.get(self.get_all_members(), id=i))
            members.append(await self.guilds[0].fetch_member(i))
        return members

    async def broadcast_invite(self, channel, time, salt=""):
        return await self.broadcast_channel.send(ARENA_INVITE % (channel.id, time) + salt)

    async def launch_game(self, quiz: Quiz):
        channel = await self.fetch_channel(quiz.cid)
        mes = await channel.send(quiz.get_start_quiz())
        await mes.add_reaction(JOIN_EMOJI)
        t0 = tm.time()
        while True:
            message = await channel.fetch_message(mes.id)
            logging.info(message.reactions)
            if message.reactions[0].count - 1 == quiz.state.player_counter:
                break
            if tm.time() - t0 > BATTLE_HOLDING:
                await self.admin_channel.send(BATTLE_ABORTED % channel.name)
                return
            await asyncio.sleep(HOLDING_BETWEEN_MESSAGES)
        while quiz.state.game_in_progress:
            quiz.update_answer_statuses()
            quiz.question_message = await channel.send(quiz.get_start_new_round())
            await asyncio.sleep(HOLDING_BETWEEN_MESSAGES)
            answers = await self.get_answers(quiz, channel, quiz.question_message)
            quiz.question_message = None
            await channel.send(END_OF_ANSWERING)
            wrong_players = quiz.check_answers_and_kill(answers, quiz.state.last_question)
            players_to_ban = await self.get_members_with_id(wrong_players)
            logging.info(f"Players to kill {players_to_ban}")
            await self.kick_players(players_to_ban, self.battles[quiz.cid][2], channel)
            await channel.send(quiz.get_round_result())
            quiz.is_game_end()
            await asyncio.sleep(HOLDING_BETWEEN_MESSAGES)
        result = quiz.get_game_result()
        await self.info_channel.send(result)
        await channel.send(result)
        quiz.state.game_ended = True

    async def get_answers(self, quiz, channel, mes):
        answers = {}
        for id, player in quiz.players.items():
            if not player.alive:
                continue
            answers[player.uid] = []
        for var in VARIANTS:
            await mes.add_reaction(var)
        await asyncio.sleep(quiz.answer_time)
        mes = await channel.fetch_message(mes.id)
        reaction = 1
        for react in mes.reactions:
            async for user in react.users():
                if user.id in answers:
                    answers[user.id].append(reaction)
            reaction += 1
        logging.info(f"Got reactions from {channel.name} - {answers}")
        return answers

    async def kick_players(self, players, role, channel):
        for p in players:
            await channel.send(SHOUTS[random.randint(0, len(SHOUTS) - 1)] + f"{p.name} was removed!")
            await p.remove_roles(role)

    async def give_role(self, players, role):
        for p in players:
            await p.add_roles(role)

    async def clean_game(self, cid):
        logging.info(f"Cleaning battle {cid} in {self.battles}.")
        attrs = self.battles[cid]
        await attrs[1].delete()
        await attrs[2].delete()
        del self.battles[cid]

    async def create_battle_channel(self, guild, role):
        name = BATTLE_CHANNEL_TEMPLATE % (len(self.battles) + 1)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(name, overwrites=overwrites)
        logging.info(f"Created channel {name} with {channel.id}.")
        return channel

    async def crate_arena_role(self, guild):
        role_name = BATTLE_ROLE_TEMPLATE % (len(self.battles) + 1)
        # add random color generation
        role = await guild.create_role(name=role_name)
        logging.info(f"{role_name} role was created. {role}")
        return role

    async def record_results(self, quiz):
        for p in quiz.players.values():
            logging.info(f"Making record for {p.name}")
            self.recorder.update_or_add_player(p, quiz)

    @staticmethod
    def load_questions():
        fp = open(PATH_TO_QUESTIONS_FILE, "r")
        ans = json.load(fp)
        fp.close()
        return ans

    async def on_raw_reaction_add(self, payload):
        cid = payload.channel_id
        if cid in self.battles and \
                self.battles[cid][0].state.game_in_progress and \
                payload.user_id in self.battles[cid][0].players and \
                self.battles[cid][0].question_message is not None and\
                self.battles[cid][0].question_message.id == payload.message_id:
            quiz = self.battles[cid][0]
            player = quiz.players[payload.user_id]
            member = await self.guilds[0].fetch_member(payload.user_id)
            logging.info(f"{player.name} just reacted!")
            if not player.answered:
                player.answered = True
                logging.info(f"{member.name} is making decision!")
            else:
                await quiz.question_message.remove_reaction(payload.emoji, member)
                logging.info(f"{member.name} tried to select more than one answer. Abort.")

    # pathetic attempt to make canceling answer
    # async def on_reaction_remove(self, reaction, user):
    #     cid = reaction.message.channel.id
    #     logging.info(f"{user.name} canceled reation.")
    #     if cid in self.battles and \
    #             self.battles[cid][0].state.game_in_progress and \
    #             user.id in self.battles[cid][0].players and \
    #             self.battles[cid][0].question_message is not None and \
    #             self.battles[cid][0].question_message.id == reaction.message.id:
    #         quiz = self.battles[cid][0]
    #         player = quiz.players[user.id]
    #         if player.answered:
    #             player.answered = False
    #             logging.info(f"{user.name} canceled his answer!")
