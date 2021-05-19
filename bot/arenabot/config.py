# emos for bot
JOIN_EMOJI = '👍'
ONE_EMOJI = '1️⃣'
TWO_EMOJI = '2️⃣'
THREE_EMOJI = '3️⃣'
FOUR_EMOJI = '4️⃣'
FIVE_EMOJI = '5️⃣'
SIX_EMOJI = '6️⃣'
SEVEN_EMOJI = '7️⃣'
EIGHT_EMOJI = '8️⃣'
NINE_EMOJI = "9️⃣"

# bot settings and info
COMMAND_PREFIX = "!"

CREATE_BATTLE_COMMAND = "mkarena"
CLEAN_ALL_COMMAND = "clean"
INFO_COMMAND = "info"
DELETE_BATTLE_COMMAND = "rmarena"
GET_PLAYER_INFO_COMMAND = "get"

COMMANDS = [
    f'!{INFO_COMMAND} - Info about all battle royale bots commands',
    f'!{CREATE_BATTLE_COMMAND} - Starts new battle with parameters.\n -q (questions) - amount of questions\n'
    f' -t (time) - time for answering',
    '/questions - Shows info about existing questions in lib',
    f'!{DELETE_BATTLE_COMMAND} - Deleting existing arena and role.',
    f'!{CLEAN_ALL_COMMAND} - Deleting ALL existing arenas and roles.'
]

ADMIN_CHANNEL = 833201507888267265
BROADCAST_CHANNEL = "835537204188545073"
INFO_CHANNEL = 835908933725978645
CATEGORY_ID = 840303711544934407

BOT_ID = 833194405594529803

GUILD_TOKEN = '833201505346650132'

ARGS_FLAGS = {
    "-t": "ANSWER_TIME",
    "-q": "QUESTIONS_AMOUNT",
}

TOPIC_ACCESSOR = "TOPICS"
ANSWER_TIME_ACCESSOR = "ANSWER_TIME"
QUESTION_AMOUNT_ACCESSOR = "QUESTIONS_AMOUNT"

# question processing
QUESTION_TYPES = [
    "docker",
    "python",
    "git",
    "django",
    "flusk"
]

QUESTION_EMOJI = [
    "🐋",
    "🐍",
    "💾",
    "🤯",
    "🐘"
]

QUESTION_EMOJI_DICT = {
    "🐋": "docker",
    "🐍": "python",
    "💾": "git",
    "🤯": "flusk",
    "🐘": "django"
}

PATH_TO_QUESTIONS_FILE = "questions.json"
PATH_TO_STAT_FILE = "stat.json"

VARIANTS = [ONE_EMOJI, TWO_EMOJI, THREE_EMOJI, FOUR_EMOJI]

# info outputs
DIVADER = "#" * 50 + '\n'
PRINT_HL = "-" * 50 + '\n'
WINNERS_AMOUNT = 1

RULES_MESSAGE = f"Hello everyone! If you read this, it means you are on the battle-royale Arena. " \
                f"Yoo will have %d round(s). " \
    f"Your task is survive as many rounds as you can. Every round consist of one question " \
    f"with 4 variants of answer. Use EMOJI to select your answer. You will have %d seconds on every " \
    f"question to select the answer, so after this time your answers will be recorded and processed. Pay " \
    f"attention, because if you are wrong, you will be kicked out of the game. Try to become the king of " \
    f"Arena or answer all questions. Good luck!!!\n\nLets meet our warriors:\n"

ARENA_INVITE = "Arena in <#%d> will start in %d seconds. React below to join!"
WRONG_ARGUMENTS_START = "Unable to create new battle: wrong arguments"
NO_ARGUMENTS = "Couldn't execute this command: no arguments. Watch info."
TOPICS_SEQUENCE = " Insided topic: %s."

TOPICS_SELECTION_MESSAGE = "To start arena choose one or more topics below.\n" \
                           "%s."

BATTLE_ABORTED = "Battle in %s was aborted: holding for too long."
END_OF_ANSWERING = "Answers recorded!"
PLAYERS_KICKED = "%s was kicked from %s."
BATTLE_STOPPED_AND_WHY = "Battle in %s was stop by %s."

ARENA_DELETED = "Battle in %s was stopped and deleted."

ROUND_RESULT_TOPIC = "Round result.\nStill in game %d:\n"
POINTS_NAME = "points"
BANNED_PLAYERS_INFO = "%d players was banned.\n"

GAME_RESULT_TOPIC = DIVADER + "After %d rounds battle in %s ended.\n" + \
    PRINT_HL + "Survivors and scores:\n"
KICKED_PLAYERS_MESSAGE = PRINT_HL + "Who didn't make it...\n"

GAME_TOPICS_INFO = "In this game you will meet %s topics. Forewarned is forearmed."
CLICK_TO_START_MESSAGE = f"Please, vote {JOIN_EMOJI} below to start."

ROUND_START_TOPIC = "Round %d.\nPlayers dead %d. Players alive %d.\n"

SHOUTS = [
    "Poor thing! ",
    "Damn son... ",
    "Mission failed. ",
    "Bruh... ",
    "Bakayaro..."
]

# battle settings
BATTLE_HOLDING = 100
TOPIC_CHOOSING = 15
HOLDING_BETWEEN_MESSAGES = 3
ANSWER_TIME = 10
DEFAULT_QUESTIONS_AMOUNT = 10

SECONDS_TO_JOIN = 11

# strings templates
BATTLE_CHANNEL_TEMPLATE = "Arena #%d"
BATTLE_ROLE_TEMPLATE = "Arena %d warrior"

# other
CHANNEL_LINK_REGEX = r"<#([\d]+)>"
