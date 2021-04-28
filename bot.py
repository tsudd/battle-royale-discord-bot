import logging
import discord
import json
import random
import time as tm
from discord import utils
from discord.ext import commands
from config import *
from entities.quiz import Quiz

from info import TOKEN


class EqualizerBot(commands.Bot):
    def __init__(self, command_prefix=COMMAND_PREFIX, self_bot=False):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
        self.battles = {}
        self.broadcast_channel = None
        self.admin_channel = None
        self.info_channel = None
        self.question_base = EqualizerBot.load_questions()
        self.start_messages = {}
        self.link_commands()

    async def on_ready(self):
        self.broadcast_channel = await self.fetch_channel(BROADCAST_CHANNEL)
        self.admin_channel = await self.fetch_channel(ADMIN_CHANNEL)
        self.info_channel = await self.fetch_channel(INFO_CHANNEL)
        logging.info(f"Bot creation - succeed. Logged as {self.user}")

    def link_commands(self):

        @self.command(name="info", pass_context=True)
        async def info(ctx):
            logging.info(f"Passed help command with context - {ctx}")
            ans = "Existing commands:\n"
            for st in COMMANDS:
                ans += st + '\n'
            await ctx.channel.send(ans)

        @self.command(name="startbattle", pass_context=True)
        async def start_battle(ctx, *args):
            if ctx.channel.id == ADMIN_CHANNEL:
                try:
                    topics = self.parse_topics([*args])
                    if len(topics) == 0:
                        await self.admin_channel.send(NO_ARGUMENTS)
                        return
                except ValueError:
                    await self.admin_channel.send(WRONG_ARGUMENTS_START)
                    return
                logging.info(f"Starting battle with topics {topics}")
                role = await self.crate_arena_role(ctx.guild)
                text_channel = await self.create_battle_channel(ctx.guild, role)
                players = await self.get_players(text_channel, topics, SECONDS_TO_JOIN)
                if len(players[1:]) == 0:
                    s = f"Stopped battle in {text_channel.name}. No players."
                    logging.info(s)
                    await self.admin_channel.send(s)
                    return
                await self.give_role(players, role)
                new_battle = Quiz(text_channel.id, ctx.me, players[1:], topics, self.question_base)
                self.battles[new_battle.cid] = [new_battle, text_channel, role]
                await self.launch_game(new_battle)

        @self.command(name="clean", pass_context=True)
        async def clean_all(ctx):
            if ctx.channel.id == ADMIN_CHANNEL:
                logging.info("Cleaning all info.")
                for battle, attrs in self.battles.items():
                    await attrs[1].delete()
                    await attrs[2].delete()
                    logging.info(f"{attrs[1]} was deleted.")
                self.battles.clear()

    def parse_topics(self, args):
        topics = []
        for arg in args:
            if arg in QUESTION_FLAGS:
                topics.append(QUESTION_FLAGS[arg])
            else:
                raise ValueError
        return topics

    async def get_players(self, channel, topics=[], time=15):
        players = []
        message = await self.broadcast_invite(channel, time)
        logging.info(f"Sent invite for {channel.name}.")
        await message.add_reaction(JOIN_EMOJI)
        tm.sleep(time)
        message = await self.broadcast_channel.fetch_message(message.id)
        if join_react := message.reactions[0]:
            async for user in join_react.users():
                players.append(user.id)
        players = await self.get_members_with_id(players)
        logging.info(f"List of players to join - {players}")
        return players

    async def get_members_with_id(self, id: list):
        members = []
        # bad code
        for i in id:
            members.append(await self.guilds[0].fetch_member(i))
        return members

    async def broadcast_invite(self, channel, time, salt=""):
        return await self.broadcast_channel.send(ARENA_INVITE % (channel.name, time) + salt)

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
            tm.sleep(HOLDING_BETWEEN_MESSAGES)
        while quiz.state.game_in_progress:
            mes = await channel.send(quiz.get_start_new_round())
            tm.sleep(HOLDING_BETWEEN_MESSAGES)
            answers = await self.get_answers(quiz, channel, mes)
            await channel.send(END_OF_ANSWERING)
            quiz.check_answers_and_kill(answers, quiz.state.last_question)
            players_to_ban = await self.get_members_with_id(quiz.ban_players())
            logging.info(f"Players to kill {players_to_ban}")
            await self.kick_players(players_to_ban, self.battles[quiz.cid][2])
            await channel.send(quiz.get_round_result())
            quiz.is_game_end()
            tm.sleep(HOLDING_BETWEEN_MESSAGES)
        result = quiz.get_game_result()
        await self.info_channel.send(result)
        await channel.send(result)

    async def get_answers(self, quiz, channel, mes):
        answers = {}
        for id, player in quiz.players.items():
            answers[player.uid] = []
        for var in VARIANTS:
            await mes.add_reaction(var)
        tm.sleep(ANSWER_TIME)
        mes = await channel.fetch_message(mes.id)
        reaction = 1
        for react in mes.reactions:
            async for user in react.users():
                if user.id in answers:
                    answers[user.id].append(reaction)
            reaction += 1
        logging.info(f"Got reactions from {channel.name} - {answers}")
        return answers

    async def kick_players(self, players, role):
        for p in players:
            await p.remove_roles(role)
            # await self.info_channel(SHOUTS[random.randint(len(SHOUTS))])

    async def give_role(self, players, role):
        for p in players:
            await p.add_roles(role)

    async def clean_game(self, quiz):
        logging.info(f"Cleaning battle in {quiz.id}")
        attrs = self.battles[quiz.id]
        await attrs[1].delete()
        await attrs[2].delete()
        del self.battles[quiz.id]

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

    @staticmethod
    def load_questions():
        fp = open(PATH_TO_QUESTIONS_FILE, "r")
        ans = json.load(fp)
        fp.close()
        return ans
