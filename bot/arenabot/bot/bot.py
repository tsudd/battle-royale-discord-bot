import asyncio
from discord import colour

from discord.ext.commands.errors import DisabledCommand
from .entities.recorder_config import *
import logging
import random
import re
import time as tm

import discord
from discord.ext import commands

from .config import *
from .entities.quiz import Quiz
from .dataprovider.data_provider import DataProvider
from .dataprovider.back_config import *


class StudentArenaBot(commands.Bot):
    def __init__(self, config: dict, intents=None):
        commands.Bot.__init__(
            self, command_prefix=config[COMMAND_PREFIX_ACCESSOR], self_bot=config[SELF_BOT_OPTION], intents=intents)
        self.battles = {}
        self.broadcast_channel = config[BROADCAST_CHANNEL_ACCESSOR]
        self.admin_channel = config[ADMIN_CHANNEL_ACCESSOR]
        self.info_channel = config[INFO_CHANNEL_ACCESSOR]
        self.data_provider = DataProvider(config[BACKEND_BASE_URL_ACCESSOR])
        self.messages = {}
        self.answers = {}
        self.setting = Settings(config)
        logging.info(self.intents.members)
        self.__link_commands(config[COMMANDS_ACCESSOR])

    async def on_ready(self):
        self.broadcast_channel = await self.fetch_channel(self.broadcast_channel)
        self.admin_channel = await self.fetch_channel(self.admin_channel)
        self.info_channel = await self.fetch_channel(self.info_channel)
        logging.info(f"Bot creation - succeed. Logged as {self.user}")

    def __link_commands(self, commands):

        # self.add_command(Command(info, name="info", pass_context=True))
        try:
            @self.command(
                name=commands[MAKEARENA_COMMAND][COMMAND_KEYWORD_ACCESSOR],
                pass_context=commands[MAKEARENA_COMMAND][COMMAND_CONTEXT_ACCESSOR],
                enabled=commands[MAKEARENA_COMMAND][COMMAND_ENABLE_ACCESSOR],
                description=commands[MAKEARENA_COMMAND][COMMAND_DESCRIPTION],
                help=commands[MAKEARENA_COMMAND][COMMAND_HELP]
            )
            async def start_battle(ctx, *args):
                if ctx.channel.id == ADMIN_CHANNEL:
                    try:
                        parsed_args = StudentArenaBot.parse_arguments([*args])
                        parsed_args[TOPIC_ACCESSOR] = await self.get_topic_id(ctx)
                        logging.info("got it")
                    except ValueError:
                        logging.info(WRONG_ARGUMENTS_START)
                        await self.send_admin(WRONG_ARGUMENTS_START)
                        return
                    except Exception as e:
                        logging.info(f"{e}. Ending start battle")
                        return
                    logging.info(
                        f"Starting battle with arguments {parsed_args}")
                    role = await self.create_arena_role(ctx.guild)
                    text_channel = await self.create_battle_channel(ctx.guild, role)
                    players = await self.get_players(text_channel, parsed_args[TOPIC_ACCESSOR])
                    if len(players) == 0:
                        # not enough players
                        s = f"Stopped battle in {text_channel.name}. No players."
                        logging.info(s)
                        await self.send_admin(s)
                        return
                    await self.give_role(players, role)
                    new_battle = Quiz(
                        text_channel.id,
                        ctx.me,
                        players,
                        self.data_provider.topics[parsed_args[TOPIC_ACCESSOR]],
                        self.data_provider.get_questions(
                            parsed_args[QUESTION_AMOUNT_ACCESSOR], parsed_args[TOPIC_ACCESSOR])
                    )
                    self.battles[new_battle.cid] = [
                        new_battle, text_channel, role]
                    try:
                        await self.launch_game(new_battle)
                        logging.info(
                            f"Arena in {text_channel.name} has ended.")
                        # make all records, ok da?
                        if new_battle.state.game_ended:
                            logging.info(
                                f"Sending info about session in {text_channel.name} to the backend.")
                            self.data_provider.send_session_info(
                                new_battle.dump_game())
                    except Exception as e:
                        logging.info(
                            f"Game {new_battle.cid} stopped by exception {e}.")
                        if new_battle.cid in self.battles:
                            await self.admin_channel.send(BATTLE_STOPPED_AND_WHY % (text_channel.name, e))
                            self.battles[new_battle.cid][0].state.game_in_progress = False
        except KeyError:
            logging.info("Couldn't deploy arena creation comand.")

        try:
            @self.command(
                name=commands[CLEANALL_COMMAND][COMMAND_KEYWORD_ACCESSOR],
                pass_context=commands[CLEANALL_COMMAND][COMMAND_CONTEXT_ACCESSOR],
                enabled=commands[CLEANALL_COMMAND][COMMAND_ENABLE_ACCESSOR],
                description=commands[CLEANALL_COMMAND][COMMAND_DESCRIPTION],
                help=commands[CLEANALL_COMMAND][COMMAND_HELP]
            )
            async def clean_all(ctx):
                if ctx.channel.id == ADMIN_CHANNEL:
                    logging.info("Cleaning all info.")
                    for attrs in self.battles.values():
                        await attrs[1].delete()
                        await attrs[2].delete()
                        logging.info(f"{attrs[1]} was deleted.")
                    self.battles.clear()
                else:
                    await ctx.reply("Nice try you dummy.")
        except KeyError:
            logging.info("Couldn't deploy \"clean all\" command")

        try:
            @self.command(
                name=commands[CLEANARENA_COMMAND][COMMAND_KEYWORD_ACCESSOR],
                pass_context=commands[CLEANARENA_COMMAND][COMMAND_CONTEXT_ACCESSOR],
                enabled=commands[CLEANARENA_COMMAND][COMMAND_ENABLE_ACCESSOR],
                description=commands[CLEANARENA_COMMAND][COMMAND_DESCRIPTION],
                help=commands[CLEANARENA_COMMAND][COMMAND_HELP]
            )
            async def clean_arena(ctx, *args):
                if ctx.channel.id == ADMIN_CHANNEL:
                    arguments = [*args]
                    logging.info(f"Got arguments to delete: {arguments}")
                    if len(arguments) > 0:
                        for a in arguments:
                            cid = int(re.match(CHANNEL_LINK_REGEX, a).group(1))
                            ch = await self.fetch_channel(cid)
                            logging.info(
                                f"Deleting channel {ch} with {cid} id.")
                            if ch is not None and ch.id in self.battles:
                                await self.info_channel.send(ARENA_DELETED % ch.name)
                                await self.clean_game(cid)
                else:
                    await ctx.reply("Nice try you dummy.")
        except KeyError:
            logging.info("Couldn't deploy arena deletion comand.")

        try:
            @self.command(
                name=commands[PONG_COMMAND][COMMAND_KEYWORD_ACCESSOR],
                pass_context=commands[PONG_COMMAND][COMMAND_CONTEXT_ACCESSOR],
                enabled=commands[PONG_COMMAND][COMMAND_ENABLE_ACCESSOR],
                description=commands[PONG_COMMAND][COMMAND_DESCRIPTION],
                help=commands[PONG_COMMAND][COMMAND_HELP]
            )
            async def pong(ctx, *arg):
                await ctx.channel.send(f"Pong {[*arg]}")
        except KeyError:
            logging.info("Couldn't deploy pong comand.")

        try:
            @self.command(
                name=commands[GETPLAYERINFO_COMMAND][COMMAND_KEYWORD_ACCESSOR],
                pass_context=commands[GETPLAYERINFO_COMMAND][COMMAND_CONTEXT_ACCESSOR],
                enabled=commands[GETPLAYERINFO_COMMAND][COMMAND_ENABLE_ACCESSOR],
                description=commands[GETPLAYERINFO_COMMAND][COMMAND_DESCRIPTION],
                help=commands[GETPLAYERINFO_COMMAND][COMMAND_HELP]
            )
            async def get_player_info(ctx):
                ans = ""
                for user in ctx.message.mentions:
                    logging.info(f"Getting info about {user.name}")
                    try:
                        data = self.data_provider.get_player_sessions(user.id)
                        ans += self.form_player_data(data)
                    except ValueError:
                        logging.error(
                            f"Couldn't get info about {user.name} from backed")
                        ans += CANT_GET_INFO % user.name
                    except Exception as e:
                        logging.error(e)
                await ctx.reply(ans if len(ans) > 0 else NO_INFO)
        except KeyError:
            logging.info("Couldn't deploy comand for getting player info.")

        try:
            @self.command(
                name=commands[LAUNCHEDARENAS_COMMAND][COMMAND_KEYWORD_ACCESSOR],
                pass_context=commands[LAUNCHEDARENAS_COMMAND][COMMAND_CONTEXT_ACCESSOR],
                enabled=commands[LAUNCHEDARENAS_COMMAND][COMMAND_ENABLE_ACCESSOR],
                description=commands[LAUNCHEDARENAS_COMMAND][COMMAND_DESCRIPTION],
                help=commands[LAUNCHEDARENAS_COMMAND][COMMAND_HELP]
            )
            async def ps_battles(ctx):
                ans = ARENA_INFO_TOPIC
                num = 1
                if len(self.battles) > 0:
                    for b in self.battles.values():
                        ans += ARENA_INFO_STRING % (
                            num,
                            b[1].name,
                            ARENA_IN_PROGRESS_STRING if b[0].state.game_in_progress else ARENA_ENDED_STRING,
                            b[0].state.dead_counter,
                            b[0].state.player_counter
                        )
                        num += 1
                else:
                    ans += "None."
                await ctx.reply(ans)
        except KeyError:
            logging.info("Couldn't deploy ps command")

        try:
            @self.command(
                name=commands[GETSESSIONINFO_COMMAND][COMMAND_KEYWORD_ACCESSOR],
                pass_context=commands[GETSESSIONINFO_COMMAND][COMMAND_CONTEXT_ACCESSOR],
                enabled=commands[GETSESSIONINFO_COMMAND][COMMAND_ENABLE_ACCESSOR],
                description=commands[GETSESSIONINFO_COMMAND][COMMAND_DESCRIPTION],
                help=commands[GETSESSIONINFO_COMMAND][COMMAND_HELP]
            )
            async def session_info(ctx, *args):
                ans = ""
                for i in args:
                    logging.info(f"Getting info about {i} session.")
                    try:
                        data = self.data_provider.get_session_info(i)
                        ans += self.form_session_data(data)
                    except ValueError:
                        logging.error(
                            f"Couldn't get info about {i} from backed")
                    # except Exception as e:
                    #     logging.error(e)
                    if len(ans) == 0:
                        ans += CANT_GET_INFO % i
                await ctx.reply(ans)
        except KeyError:
            logging.info("Couldn't deploy comand for getting session info")

    def form_player_data(self, data: dict):
        player = data[PLAYER_ACCESSOR]
        ans = PLAYER_INFO % (
            player[ID_ACCESSOR],
            player[GAMES_AMOUNT_ACCESSOR],
            round(player[LIFETIME_ACCESSOR], 4) * 100,
            player[WINS_ACCESSOR]
        )
        if len(data[SESSIONS_ACCESSOR]) > 0:
            ans += PLAYERS_SESSIONS_TITLE % len(data[SESSIONS_ACCESSOR])
            num = 1
            for s in data[SESSIONS_ACCESSOR]:
                ans += SESSION_INFO_STRING % (
                    num,
                    s[DATETIME_ACCESSOR],
                    s[ID_ACCESSOR],
                    s[PLAYERS_AMOUNT],
                    s[ROUNDS_AMOUNT],
                    self.data_provider.get_topic_str(s[TOPIC_QUERY])
                )
                num += 1
        ans += '-' * 50
        return ans

    def form_session_data(self, data: dict):
        ans = SESSION_INFO_TITLE % (
            data[ID_ACCESSOR],
            data[DATETIME_ACCESSOR],
            data[PLAYERS_AMOUNT],
            data[ROUNDS_AMOUNT],
            self.data_provider.get_topic_str(data[TOPIC_QUERY])
        )
        ans += SESSION_ROUNDS_TITLE
        num = 1
        for r in data[ROUNDS_ACCESSOR]:
            ans += ROUND_INFO % (
                num,
                r[QUESTION_ID_ACCESSOR],
            )
            j = 1
            for answer in r[ANSWERS_ACCESSOR]:
                ans += ANSWER_INFO % (
                    j,
                    answer[PLAYER_ACCESSOR],
                    answer[ANSWER_ACCESSOR],
                    RIGHT_ANSWER if answer[ANSWER_STATUS_ACCESSOR] else WRONG_ANSWER
                )
                j += 1
            num += 1
        return ans

    async def send_admin(self, message: str):
        await self.admin_channel.send(message)

    async def get_topic_id(self, ctx):
        s = ""
        logging.info("Getting topic for new game.")
        for topic in self.data_provider.topics.values():
            s += f"- {topic[EMOJI_ACCESSOR]} is {topic[NAME_ACCESSOR]}.\n"
        message_string = TOPICS_SELECTION_MESSAGE % s
        mes = await ctx.reply(message_string, mention_author=True)
        logging.debug(f"Sent message to react {mes.id}")
        self.messages[mes.id] = (False, None)
        for emo in self.data_provider.topic_emojis.keys():
            await mes.add_reaction(emo)
        t0 = tm.time()
        while not self.messages[mes.id][0]:
            logging.info("Waiting for choosing the topic for new game.")
            if tm.time() - t0 > TOPIC_CHOOSING:
                raise ValueError
            await asyncio.sleep(3)
        ans = self.messages[mes.id][1]
        del self.messages[mes.id]
        logging.info(f"Got topic {self.data_provider.topics[ans]}")
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

    async def get_players(self, channel, topic):
        players = []
        info = TOPICS_SEQUENCE % (
            self.data_provider.topics[topic][NAME_ACCESSOR])
        message = await self.broadcast_invite(channel, self.setting.join_seconds, info)
        logging.info(f"Sent invite for {channel.name}.")
        await message.add_reaction(JOIN_EMOJI)
        await asyncio.sleep(self.setting.join_seconds)
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
            await self.get_answers(quiz, channel, quiz.question_message)
            quiz.question_message = None
            await channel.send(END_OF_ANSWERING)
            wrong_players = quiz.check_answers_and_kill(
                self.answers, quiz.state.last_question)
            players_to_ban = await self.get_members_with_id(wrong_players)
            logging.info(f"Players to kill {players_to_ban}")
            await self.kick_players(players_to_ban, self.battles[quiz.cid][2], channel)
            await channel.send(quiz.get_round_result())
            quiz.record_round(self.answers)
            quiz.is_game_end()
            await asyncio.sleep(HOLDING_BETWEEN_MESSAGES)
        result = quiz.get_game_result()
        await self.info_channel.send(result)
        await channel.send(result)
        quiz.state.game_ended = True

    async def get_answers(self, quiz, channel, mes):
        self.answers = {}
        for player in quiz.players.values():
            if not player.alive:
                continue
            self.answers[player.uid] = -1
        for var in VARIANTS.keys():
            await mes.add_reaction(var)
        await asyncio.sleep(quiz.answer_time)
        logging.info(f"Got reactions from {channel.name} - {self.answers}")

    async def kick_players(self, players, role, channel):
        for p in players:
            await channel.send(SHOUTS[random.randint(0, len(SHOUTS) - 1)] + PLAYER_REMOVED % p.id)
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
        arenas = len(guild.categories[0].channels)
        name = BATTLE_CHANNEL_TEMPLATE % (arenas + 1)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(
                read_messages=True, send_messages=False)
        }

        channel = await guild.create_text_channel(name, overwrites=overwrites, category=guild.categories[0])
        logging.info(f"Created channel {name} with {channel.id}.")
        return channel

    async def create_arena_role(self, guild):
        role_name = BATTLE_ROLE_TEMPLATE % (len(self.battles) + 1)
        # add random color generation -- done
        role = await guild.create_role(name=role_name, colour=self.get_random_color())
        logging.info(f"{role_name} role was created. {role}")
        return role

    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.user.id:
            return
        cid = payload.channel_id
        if cid in self.battles and \
                str(payload.emoji) in VARIANTS and \
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
                self.answers[player.uid] = VARIANTS[str(payload.emoji)]
                await self.battles[cid][1].send(PLAYER_ANSWERED % player.uid)
                logging.info(f"{member.name} is making decision!")
            else:
                await quiz.question_message.remove_reaction(payload.emoji, member)
                logging.info(
                    f"{member.name} tried to select more than one answer. Abort.")
        elif cid == self.admin_channel.id:
            emo = str(payload.emoji)
            if payload.message_id in self.messages and \
                    not self.messages[payload.message_id][0] and \
                    emo in self.data_provider.topic_emojis:
                self.messages[payload.message_id] = True,  self.data_provider.topic_emojis[emo]
                logging.info(
                    f"Got {payload.emoji} reaction when selecting topic.")

    async def on_command_error(self, context, exception):
        if isinstance(exception, DisabledCommand):
            logging.info(
                f"Tried to exec disabled command but got error: {exception}.")
            await context.reply(COMMAND_ERROR % exception)
            return
        return await super().on_command_error(context, exception)

    def get_random_color(self):
        return discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

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


class Settings(object):
    def __init__(self, settings) -> None:
        super().__init__()
        self.join_seconds = settings[JOIN_SECONDS_ACCESSOR]
