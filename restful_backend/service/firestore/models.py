from .config import *
import datetime

# Create your models here.


class Player(object):
    def __init__(
        self,
        dis_id=228,
        nick="NO NICK",
        lifetime=1,
        games_amount=0,
        wins=0
    ) -> None:
        super().__init__()
        self.dis_id = dis_id
        self.nick = nick
        self.lifetime = lifetime
        self.games_amount = games_amount
        self.wins = wins
        self.id = str(self.dis_id)

    @staticmethod
    def from_dict(data):
        return Player(
            dis_id=data[UID_ACCESSOR],
            nick=data[NAME_ACCESSOR],
            lifetime=data[LIFETIME_ACCESSOR],
            games_amount=data[GAMES_AMOUNT_ACCESSOR],
            wins=data[WINS_AMOUNT_ACCESSOR]
        )

    def to_dict(self):
        return {
            UID_ACCESSOR: self.dis_id,
            NAME_ACCESSOR: self.nick,
            LIFETIME_ACCESSOR: self.lifetime,
            GAMES_AMOUNT_ACCESSOR: self.games_amount,
            WINS_AMOUNT_ACCESSOR: self.wins,
            ID_ACCESSOR: self.dis_id
        }

    def update_lifetime(self, score, rounds, alive):
        total = self.games_amount + 1
        cycle = score / rounds if not alive else 1
        self.lifetime = (self.lifetime * self.games_amount + cycle) / total
        self.games_amount = total

    def update_info(self, data: dict, rounds_amount):
        if data[ALIVE_ACCESSOR]:
            self.wins += 1
        self.update_lifetime(data[TOTAL_RIGHTS_ACCESSOR],
                             rounds_amount, data[ALIVE_ACCESSOR])

    def __str__(self):
        return f"{self.nick} with {self.games_amount} games."


class QuestionTopic(object):
    def __init__(self, name=DEFAULT_EMPTY_STRING, emoji="🖕🏻", tid="0") -> None:
        super().__init__()
        self.name = name
        self.emoji = emoji
        self.id = tid

    @staticmethod
    def from_dict(data):
        return QuestionTopic(
            name=data["name"],
            emoji=data["emoji"],
            tid=data[ID_ACCESSOR]
        )

    def to_dict(self):
        return {
            "name": self.name,
            "emoji": self.emoji,
            "id": self.id
        }

    def __str__(self):
        return f"{self.name} topic."


class QuestionVariant(object):
    def __init__(self, variant=DEFAULT_EMPTY_STRING, vid="0") -> None:
        super().__init__()
        self.variant = variant
        self.id = vid

    @staticmethod
    def from_dict(data, many=False):
        if many:
            ans = []
            for v in data:
                ans.append(
                    QuestionVariant(
                        variant=v[QUESTION_VARIANT],
                        vid=v[ID_ACCESSOR]
                    )
                )
            return ans
        return QuestionVariant(
            variant=data[QUESTION_VARIANT],
            vid=data[ID_ACCESSOR]
        )

    @staticmethod
    def many_to_list(data):
        ans = []
        for v in data:
            ans.append(
                v.to_dict()
            )
        return ans

    def to_dict(self):
        return {
            QUESTION_VARIANT: self.variant,
            ID_ACCESSOR: self.id
        }

    def __str__(self):
        return f"Question variant {self.variant}"


class Question(object):
    def __init__(
        self,
        question_string=DEFAULT_EMPTY_STRING,
        variants=None,
        topic="0",
        right_ind="1",
        qid="0"
    ) -> None:
        super().__init__()
        self.question_string = question_string
        self.variants = QuestionVariant.from_dict(variants, many=True)
        self.topic = topic
        self.right_ind = right_ind
        self.id = qid

    @staticmethod
    def from_dict(data):
        return Question(
            question_string=data[QUESTION_STRING_FIELD],
            variants=data[VARIANTS_ACCESSOR],
            topic=data[TOPIC_QUERY],
            right_ind=data[QUESTION_RIGHT_ANSWER],
            qid=data[ID_ACCESSOR]
        )

    def to_dict(self):
        return {
            QUESTION_STRING_FIELD: self.question_string,
            VARIANTS_ACCESSOR: QuestionVariant.many_to_list(self.variants),
            TOPIC_QUERY: self.topic,
            QUESTION_RIGHT_ANSWER: self.right_ind,
            ID_ACCESSOR: self.id
        }

    def __str__(self):
        return f"Question {self.question_string}."


class Round(object):
    def __init__(
        self,
        session="0",
        question="0",
        variants=None,
        right_ind="0",
        rid="0"
    ) -> None:
        super().__init__()
        self.session = session
        self.question = question
        self.variants = variants
        self.right_ind = right_ind
        self.id = rid

    @staticmethod
    def from_dict(data):
        return Round(
            session=data[SESSION_ACCESSOR],
            question=data[QUESTION_ID_ACCESSOR],
            variants=data[VARIANTS_ACCESSOR],
            right_ind=data[QUESTION_RIGHT_ANSWER],
            rid=data[ID_ACCESSOR]
        )

    def to_dict(self):
        return {
            ID_ACCESSOR: self.id,
            SESSION_ACCESSOR: self.session,
            QUESTION_ID_ACCESSOR: self.question,
            VARIANTS_ACCESSOR: self.variants,
            QUESTION_RIGHT_ANSWER: self.right_ind,
        }

    def __str__(self):
        return f"Round of session {self.session} with question {self.question}."


class Answer(object):
    def __init__(
        self,
        session="0",
        round_arg="0",
        player="0",
        answer="0",
        right=False,
        aid="0"
    ) -> None:
        super().__init__()
        self.session = session
        self.round = round_arg
        self.player = player
        self.answer = answer
        self.right = right
        self.id = aid

    @staticmethod
    def from_dict(data):
        return Answer(
            session=data[SESSION_ACCESSOR],
            round_arg=data[ROUND_ACCESSOR],
            player=data[PLAYER_ACCESSOR],
            answer=data[QUESTION_VARIANT],
            right=data[ANSWER_STATUS_ACCESSOR],
            aid=data[ID_ACCESSOR]
        )

    def to_dict(self):
        return {
            ID_ACCESSOR: self.id,
            SESSION_ACCESSOR: self.session,
            ROUND_ACCESSOR: self.round,
            PLAYER_ACCESSOR: self.player,
            QUESTION_VARIANT: self.answer,
            ANSWER_STATUS_ACCESSOR: self.right
        }

    def __str__(self):
        return f"{self.right} answer of {self.player}."


class Session(object):
    def __init__(
        self,
        players_amount=0,
        dead_amount=0,
        rounds_amount=1,
        date=datetime.datetime.now().isoformat(sep='T'),
        topic="0",
        sid="0"
    ) -> None:
        super().__init__()
        self.players_amount = players_amount
        self.dead_amount = dead_amount
        self.rounds_amount = rounds_amount
        self.date = date
        self.topic = topic
        self.id = sid

    @staticmethod
    def from_dict(data):
        return Session(
            players_amount=data[PLAYERS_AMOUNT],
            dead_amount=data[DEAD_AMOUNT],
            rounds_amount=data[ROUNDS_AMOUNT],
            date=data[DATETIME_FIELD],
            topic=data[TOPIC_QUERY],
            sid=data[ID_ACCESSOR]
        )

    def to_dict(self):
        return {
            PLAYERS_AMOUNT: self.players_amount,
            DEAD_AMOUNT: self.dead_amount,
            ROUNDS_AMOUNT: self.rounds_amount,
            DATETIME_FIELD: self.date,
            TOPIC_QUERY: self.topic
        }

    def __str__(self):
        return f"Session of {self.date} with {self.topic}"


class Participation(object):
    def __init__(self, session="0", player="0") -> None:
        super().__init__()
        self.session = session
        self.player = player

    @staticmethod
    def from_dict(data):
        return Participation(
            session=data[SESSION_ACCESSOR],
            player=data[PLAYER_ACCESSOR]
        )

    def to_dict(self):
        return {
            SESSION_ACCESSOR: self.session,
            PLAYER_ACCESSOR: self.player
        }

    def __str__(self):
        return f"Participation record of {self.player}."
