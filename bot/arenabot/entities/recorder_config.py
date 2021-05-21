# fields accessors
ID_ACCESSOR = "id"
UID_ACCESSOR = "uid"

QUESTION_STRING_FIELD = 'question_string'
QUESTION_ANSWERS_FIELDS = ["varOne", "varTwo", "varThree", "varFour"]
QUESTION_RIGHT_ANSWER = "right_ind"
QUESTION_VARIANT = "variant"

# player model
PLAYERS_MODELS_ACCESSOR = "players"
NICK_ACCESSOR = "nick"
LIVECYCLE_ACCESSOR = "lifecycle"
PLAYED_GAMES_ACCESSOR = "played"
LAST_ARENA_ACCESSOR = "last-arena"
USUALLY_WRONG_ACCESSOR = "wrong"
WINS_ARENAS_ACCESSOR = "wins"
TOTAL_RIGHTS_ACCESSOR = "rights"
ALIVE_ACCESSOR = "alive"

# question model
QUESTION_ID_ACCESSOR = "question"
ANSWERS_ACCESSOR = "answers"
ANSWER_STATUS_ACCESSOR = "right"

# dump fields
DEAD_AMOUNT = "dead_amount"
PLAYERS_AMOUNT = "players_amount"
DATETIME_FIELD = "date"
TOPIC_FIELD = "topic"
ROUNDS_AMOUNT = "rounds_amount"
ROUNDS_ACCESSOR = "rounds"

# defaults
DEFAULT_USERNAME = "UNNAMED_USER"
DEFAULT_ID = 0
DEFAULT_LIVECYCLE = 0
DEFAULT_GAMES_AMOUNT = 0
DEFAULT_USUALLY_WRONG = {}
DEFAULT_LAST_ARENA = None
DEFAULT_WINS = 0
DEFAULT_RIGHTS = 0

DEFAULT_FILENAME = "stat.json"

# stat outputs
INFO_TEXT = f"""Info about <@%d>:
Arenas played - %d.
Average lifetime - %d percent.
Last arena - %s.
Right answers in total - %d.
Wins - %d.
"""

WRONGS_TITLE = "The most bad questions(question - wrong answers amount):\n"
NO_QUESTIONS = "Couldn't get question string: wrong key."
NO_PLAYER = "No info about <@%d>."
