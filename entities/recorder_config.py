# fields accessors
ID_ACCESSOR = "id"

QUESTION_STRING_FIELD = 'question'
QUESTION_ANSWERS_FIELD = 'answers'
QUESTION_DESCRIPTION = "description"

# player model
PLAYERS_MODELS_ACCESSOR = "players"
NICK_ACCESSOR = "nick"
LIVECYCLE_ACCESSOR = "lifecycle"
PLAYED_GAMES_ACCESSOR = "played"
LAST_ARENA_ACCESSOR = "last-arena"
USUALLY_WRONG_ACCESSOR = "wrong"
WINS_ARENAS_ACCESSOR = "wins"
TOTAL_RIGHTS_ACCESSOR = "rights"

# question model
PARTITION_COUNTER_ACCESSOR = "partam"
PLAYERS_LOST_ACCESSOR = "losers"


# defaults
DEFAULT_USERNAME = "UNNAMED_USER"
DEFAULT_ID = 0
DEFAULT_LIVECYCLE = 0
DEFAULT_GAMES_AMOUNT = 0
DEFAULT_USUALLY_WRONG = {}
DEFAULT_LAST_ARENA = None
DEFAULT_WINS = 0
DEFAULT_RIGHTS = 0

DEFAULT_FILENAME = "../stat.json"

INFO_TEXT = f"""Info about <@%d>:
Arenas played - %d.
Average lifetime - %d%.
Last arena - %s.
Right answers in total - %d.
Wins - %d.
"""

WRONGS_TITLE = "The most bad questions(question - wrong answers amount:\n"
NO_QUESTIONS = "Couldn't get question string: wrong key."
NO_PLAYER = "No info about <@%d>."
