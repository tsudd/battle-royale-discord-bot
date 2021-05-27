# bot commands
COMMAND_PREFIX = "!"

CREATE_BATTLE_COMMAND = "mkarena"
CLEAN_ALL_COMMAND = "clean"
INFO_COMMAND = "info"
DELETE_BATTLE_COMMAND = "rmarena"
GET_PLAYER_INFO_COMMAND = "gets"

COMMANDS = [
    f'!{INFO_COMMAND} - Info about all battle royale bots commands',
    f'!{CREATE_BATTLE_COMMAND} - Starts new battle with parameters.\n -q (questions) - amount of questions\n'
    f' -t (time) - time for answering',
    '/questions - Shows info about existing questions in lib',
    f'!{DELETE_BATTLE_COMMAND} - Deleting existing arena and role.',
    f'!{CLEAN_ALL_COMMAND} - Deleting ALL existing arenas and roles.',
    f"!{GET_PLAYER_INFO_COMMAND} - get info about player and his participation"
]




