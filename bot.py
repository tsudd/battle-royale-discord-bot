import logging
import discord
import json
import time as tm
from discord import utils
from discord.ext import commands
from config import *
from entities.quiz import Quiz

from info import TOKEN


class EqualizerBot(commands.Bot):
    def __init__(self, command_prefix=COMMAND_PREFIX, self_bot=False):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
        self.battles = []
        self.broadcast_channel = None
        self.admin_channel = None
        self.question_base = EqualizerBot.load_questions()
        self.link_commands()

    async def on_ready(self):
        logging.info(f"Bot creation - succeed. Logged as {self.user}")
        self.broadcast_channel = await self.fetch_channel(BROADCAST_CHANNEL)
        self.admin_channel = await self.fetch_channel(ADMIN_CHANNEL)

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
                new_battle = Quiz(text_channel.id, ctx.me, players, topics, self.question_base)
                self.battles.append(new_battle)
                await self.launch_game(new_battle)

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
                players.append(user)
        logging.info(f"List of players to join - {players}")
        return players

    async def broadcast_invite(self, channel, time, salt=""):
        return await self.broadcast_channel.send(ARENA_INVITE % (channel.name, time))

    async def launch_game(self, quiz: Quiz):
        channel = await self.fetch_channel(quiz.cid)



    def send_message_admin(self):
        pass

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



        # self.add_command(info)




