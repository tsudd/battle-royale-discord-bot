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

COMMAND_PREFIX = "!"

COMMANDS = [
    '/info - Info about all battle royale bots commands',
    '/startbattle - Starts new battle',
    '/questions - Shows info about existing questions in lib',
    '/cancelbattle - Cancels an existing battle',
    '/clean - Cleans channel after ended games'
]

QUESTION_TYPES = [
    "docker",
    "python",
    "git",
    "django",
    "flusk"
]

QUESTION_FLAGS = {
    "d": "docker",
    "p": "python",
    "g": "git",
    "dj": "django",
    "fl": "flusk"
}

QUESTION_EMOJI = {
    "docker": "docker🐋",
    "python": "python🐍",
    "git": "git💾",
    "flusk": "flusk🤯",
    "django": "django🐘"
}

QUESTION_STRING_FIELD = 'question'
QUESTION_ANSWERS_FIELD = 'answers'

QUESTION_DESCRIPTION_FIELD = "description"
PATH_TO_QUESTIONS_FILE = "questions.json"

PRINT_HL = "-" * 50 + '\n'
WINNERS_AMOUNT = 1

RULES_MESSAGE = f"Hello everyone! If you read this, it means you are on the battle-royale Arena." \
              f"Your task is survive as many rounds as you can. Every round consist of one question " \
              f"with 4 variants of answer. Use EMOJI to select your answer. You will have 15 seconds on every " \
              f"question to select the answer, so after this time your answers will be recorded and processed. Pay " \
              f"attention, because if you are wrong, you will be kicked out of the game. Try to become the king of " \
              f"Arena or answer all questions. Good luck!!!\n\n"

ARENA_INVITE = "Arena in %s will start in %d seconds. React below to join!"
WRONG_ARGUMENTS_START = "Unable to create new battle: wrong arguments"
NO_ARGUMENTS = "Couldn't execute this command: no arguments. Watch !info."


ADMIN_CHANNEL = 833201507888267265
BROADCAST_CHANNEL = "835537204188545073"

SECONDS_TO_JOIN = 5

BATTLE_CHANNEL_TEMPLATE = "Arena #%d"
BATTLE_ROLE_TEMPLATE = "Arena %d warrior"

GUILD_TOKEN = '833201505346650132'
