# data fields

DEAD_AMOUNT = "dead_amount"
PLAYERS_AMOUNT = "players_amount"
DATETIME_FIELD = "date"
TOPIC_FIELD = "topic"
ROUNDS_AMOUNT = "rounds_amount"
ROUNDS_ACCESSOR = "rounds"

DEFAULT_EMPTY_STRING = "NO DATA"

# player model
PLAYERS_ACCESSOR = "players"
UID_ACCESSOR = "uid"
ID_ACCESSOR = "id"
DISID_ACCESSOR = "dis_id"
NAME_ACCESSOR = "nick"
LIFETIME_ACCESSOR = "lifetime"
GAMES_AMOUNT_ACCESSOR = "games_amount"
WINS_AMOUNT_ACCESSOR = "wins"
ALIVE_ACCESSOR = "alive"
TOTAL_RIGHTS_ACCESSOR = "rights"

# question model
QUESTION_STRING_FIELD = 'question_string'
QUESTION_ANSWERS_FIELDS = ["varOne", "varTwo", "varThree", "varFour"]
QUESTION_RIGHT_ANSWER = "right_ind"
QUESTION_VARIANT = "variant"
QUESTION_ID_ACCESSOR = "question"

ANSWERS_ACCESSOR = "answers"
ANSWER_ACCESSOR = "answer"
ANSWER_STATUS_ACCESSOR = "right"

SESSION_ACCESSOR = "session"
ROUND_ACCESSOR = "round"
PLAYER_ACCESSOR = "player"

VARIANTS_ACCESSOR = "variants"

# firestore collections names
SESSIONS_COLLECTION = u"sessions"
QUESIONS_COLLECTION = u"questions"
TOPICS_COLLECTION = u"topics"
PARTICIPATIONS_COLLECTION = u"participations"


# params
TOPIC_QUERY = "topic"
AMOUNT_QUERY = "amount"
ID_QUERY = "id"

# templates
DATETIME_TEMPLATE = '%d.%m.%Y %H:%M'
