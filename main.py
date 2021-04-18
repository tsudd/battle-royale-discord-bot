#!/usr/bin/python3
import logging
import random
import json
from time import sleep
from info import TOKEN

from bot import EqualizerBot


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    bot = EqualizerBot()
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
