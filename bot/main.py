#!/home/tsudd/anaconda3/envs/battle-royale-discord-bot/bin/python3
import logging

import discord

from arenabot.info import TOKEN
from arenabot.config import COMMAND_PREFIX
from arenabot.bot import StudentArenaBot

import json


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_config():
    try:
        fs = open("./bot/config.json", "r")
        c = json.load(fs)
        fs.close()
        logging.info("Successfully read default configuration for bot.")
    except FileNotFoundError:
        raise AssertionError("Couldn't find config file.")
    return c


def main():
    intents = discord.Intents.default()
    intents.members = True
    intents.reactions = True
    conf = get_config()
    bot = StudentArenaBot(conf, intents=intents)
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
