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

ADMIN_CHANNEL = 833201507888267265
BROADCAST_CHANNEL = "835537204188545073"
INFO_CHANNEL = 835908933725978645
CATEGORY_ID = 840303711544934407

BOT_ID = 833194405594529803

GUILD_TOKEN = '833201505346650132'

# config structure
COMMAND_PREFIX_ACCESSOR = "commandPrefix"
ADMIN_CHANNEL_ACCESSOR = "adminChannel"
BROADCAST_CHANNEL_ACCESSOR = "broadcastChannel"
INFO_CHANNEL_ACCESSOR = "infoChannel"
CHANNELS_CATEGORY_ACCESSOR = "channelsCategory"
SELF_BOT_OPTION = "selfBot"
BACKEND_BASE_URL_ACCESSOR = "backendBaseUrl"
JOIN_SECONDS_ACCESSOR = "waitingForJoin"
LOAD_QUESTIONS_ACCESSOR = "loadQuestions"

COMMANDS_ACCESSOR = "commands"
COMMAND_NAME_ACCESSOR = "commandName"
COMMAND_KEYWORD_ACCESSOR = "commandKeyWord"
COMMAND_ENABLE_ACCESSOR = "enabled"
COMMAND_CONTEXT_ACCESSOR = "passContext"
COMMAND_DESCRIPTION = "description"
COMMAND_HELP = "help"

# commands accessors
INFO_COMMAND = "info"
MAKEARENA_COMMAND = "makeArena"
CLEANALL_COMMAND = "cleanAll"
CLEANARENA_COMMAND = "cleanArena"
PONG_COMMAND = "pong"
GETPLAYERINFO_COMMAND = "getPlayerInfo"
LAUNCHEDARENAS_COMMAND = "ps"
GETSESSIONINFO_COMMAND = "sessionInfo"

ARGS_FLAGS = {
    "-t": "ANSWER_TIME",
    "-q": "QUESTIONS_AMOUNT",
}

TOPIC_ACCESSOR = "TOPICS"
ANSWER_TIME_ACCESSOR = "ANSWER_TIME"
QUESTION_AMOUNT_ACCESSOR = "QUESTIONS_AMOUNT"

SESSIONS_ACCESSOR = "sessions"

# question processing

VARIANTS = {
    ONE_EMOJI: 1,
    TWO_EMOJI: 2,
    THREE_EMOJI: 3,
    FOUR_EMOJI: 4
}

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
COMMAND_ERROR = "Couldn't exec the command: %s."
END_OF_ANSWERING = "Answers recorded!"
PLAYERS_KICKED = "<@%d> was kicked from %s."
BATTLE_STOPPED_AND_WHY = "Battle in %s was stop by %s."
CANT_GET_INFO = "Couldn't get info about %s."

ARENA_DELETED = "Battle in %s was stopped and deleted."

ROUND_RESULT_TOPIC = "Round result.\nStill in game %d:\n"
POINTS_NAME = "points"
BANNED_PLAYERS_INFO = "%d players was banned.\n"

ARENA_INFO_TOPIC = "Launched arenas list\n"
ARENA_INFO_STRING = "%d. %s %s. Players kicked - %d. Players alive - %d.\n"
ARENA_IN_PROGRESS_STRING = "in progress..🛐"
ARENA_ENDED_STRING = "ended☯️"

GAME_RESULT_TOPIC = DIVADER + "After %d rounds battle in %s ended.\n" + \
    PRINT_HL + "Survivors and scores:\n"
KICKED_PLAYERS_MESSAGE = PRINT_HL + "Who didn't make it...\n"

GAME_TOPICS_INFO = "In this game you will meet %s topics. Forewarned is forearmed."
CLICK_TO_START_MESSAGE = f"Please, vote {JOIN_EMOJI} below to start."

ROUND_START_TOPIC = "Round %d.\nPlayers dead %d. Players alive %d.\n"

PLAYER_ANSWERED = "<@%d> answered!"
PLAYER_REMOVED = "<@%d> was removed!"

NO_ATTACHMENTS = "No attachments to the message. Attache file to send questions."
PUT_QUESTIONS_ERROR = "Couldn't load questions from %s. Make sure, that file format is csv and filled correctly."

LOADED_QUESTIONS = "Loaded %d questions to the database.\n"

SHOUTS = [
    "Poor thing! ",
    "Damn son... ",
    "Mission failed. ",
    "Bruh... ",
    "Bakayaro... ",
    "It was going so well... ",
    "Didn't want to say it, but... "
]

# battle settings
BATTLE_HOLDING = 100
TOPIC_CHOOSING = 15
HOLDING_BETWEEN_MESSAGES = 3
ANSWER_TIME = 20
DEFAULT_QUESTIONS_AMOUNT = 10

SECONDS_TO_JOIN = 11

# strings templates
BATTLE_CHANNEL_TEMPLATE = "Arena #%d"
BATTLE_ROLE_TEMPLATE = "Arena %d warrior"
DATETIME_TEMPLATE = '%d.%m.%Y %H:%M:%S'

# information outputs

NO_INFO = "Nothing to output"

PLAYER_INFO = """----Info about <@%d>----
Arenas played - %d.
Average lifetime - %.2f percent.
Wins - %d.
"""

PLAYERS_SESSIONS_TITLE = "----Last %d arenas----\n"

SESSION_INFO_STRING = "%d. Arena from %s\nID - %s\nPlayers amount - %d\nRounds amount - %d\nTopic - %s\n"
SESSION_INFO_TITLE = "Information about %s session\nArena from %s\nPlayers amount - %d\nRounds amount - %d\nTopic - %s\n"
SESSION_ROUNDS_TITLE = f"----Session rounds----\n"
ROUND_INFO = "----Round #%d----\nQuestion - %s.\nPlayers answers:\n"
ANSWER_INFO = "%d. <@%d> answered %s, which is %s.\n"
RIGHT_ANSWER = "right✅"
WRONG_ANSWER = "wrong❌"

# other
CHANNEL_LINK_REGEX = r"<#([\d]+)>"

CONFIGURATIONS_PATH = "./bot/start_configs/"
CONFIG_FILENAME = "config.json"
STANDART_CONFIG_FILE_PATH = "./"
