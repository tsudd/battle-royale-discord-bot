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

BOT_ID = 833194405594529803

GUILD_TOKEN = '833201505346650132'

ARGS_FLAGS = {
    "-t": "ANSWER_TIME",
    "-q": "QUESTIONS_AMOUNT",
}

TOPICS_ACCESSOR = "TOPICS"
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

QUESTION_STRING_FIELD = 'question'
QUESTION_ANSWERS_FIELD = 'answers'
QUESTION_DESCRIPTION = "description"

QUESTION_DESCRIPTION_FIELD = "description"
PATH_TO_QUESTIONS_FILE = "questions.json"

VARIANTS = [ONE_EMOJI, TWO_EMOJI, THREE_EMOJI, FOUR_EMOJI]

# info outputs
PRINT_HL = "-" * 50 + '\n'
WINNERS_AMOUNT = 1

RULES_MESSAGE = f"Hello everyone! If you read this, it means you are on the battle-royale Arena. " \
                f"Yoo will have %d round(s). " \
              f"Your task is survive as many rounds as you can. Every round consist of one question " \
              f"with 4 variants of answer. Use EMOJI to select your answer. You will have %d seconds on every " \
              f"question to select the answer, so after this time your answers will be recorded and processed. Pay " \
              f"attention, because if you are wrong, you will be kicked out of the game. Try to become the king of " \
              f"Arena or answer all questions. Good luck!!!\n\n"

ARENA_INVITE = "Arena in <#%d> will start in %d seconds. React below to join!"
WRONG_ARGUMENTS_START = "Unable to create new battle: wrong arguments"
NO_ARGUMENTS = "Couldn't execute this command: no arguments. Watch info."
TOPICS_SEQUENCE = " Inside topics: %s."

TOPICS_SELECTION_MESSAGE = "To start arena choose one or more topics below.\n" \
                           "%s."

BATTLE_ABORTED = "Battle in %s was aborted: holding for too long."
END_OF_ANSWERING = "Answers recorded!"
PLAYERS_KICKED = "%s was kicked from %s."

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

SECONDS_TO_JOIN = 5

# strings templates
BATTLE_CHANNEL_TEMPLATE = "Arena #%d"
BATTLE_ROLE_TEMPLATE = "Arena %d warrior"


