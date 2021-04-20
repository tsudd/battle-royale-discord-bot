JOIN_EMOTE = '👍'

COMMAND_PREFIX = "!"

COMMANDS = [
    '/info - Info about all battle royale bots commands',
    '/startbattle - Starts new battle',
    '/questions - Shows info about existing questions in lib',
    '/cancelbattle - Cancels an existing battle',
    '/join - Joins an existing game'
]

QUESTION_TYPES = [
    "docker",
    "python",
    "git",
    "django/flusk"
]

QUESTION_STRING_FIELD = 'question'
QUESTION_ANSWERS_FIELD = 'answers'

QUESTION_DESCRIPTION_FIELD = "description"

PRINT_HL = "-" * 50 + '\n'
WINNERS_AMOUNT = 1

RULES_MESSAGE = f"Hello everyone! If you read this, it means you are on the battle-royale Arena." \
              f"Your task is survive as many rounds as you can. Every round consist of one question " \
              f"with 4 variants of answer. Use EMOJI to select your answer. You will have 15 seconds on every " \
              f"question to select the answer, so after this time your answers will be recorded and processed. Pay " \
              f"attention, because if you are wrong, you will be kicked out of the game. Try to become the king of " \
              f"Arena or answer all questions. Good luck!!!\n\n"

