import logging
import discord
from discord import utils
from discord.ext import commands
from config import *

from info import TOKEN


class EqualizerBot(commands.Bot):
    def __init__(self, command_prefix=COMMAND_PREFIX, self_bot=False):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
        self.link_commands()

    async def on_ready(self):
        logging.info(f"Bot creation - succeed. Logged as {self.user}")

    def link_commands(self):

        @self.command(name="info", pass_context=True)
        async def info(ctx):
            logging.info(f"Passed help command with context - {ctx}")
            ans = "Existing commands:\n"
            for st in COMMANDS:
                ans += st + '\n'
            await ctx.channel.send(ans)

        # self.add_command(info)




