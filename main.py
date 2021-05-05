#!/usr/bin/python3
import logging

import discord

from info import TOKEN
from config import COMMAND_PREFIX

from bot import EqualizerBot


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    intents = discord.Intents.default()
    intents.members = True
    intents.reactions = True
    bot = EqualizerBot(command_prefix=COMMAND_PREFIX, intents=intents)
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
