from .recorder_config import *
from .question import Question


class PlayerModel(object):
    def __init__(
            self,
            id_arg=DEFAULT_ID,
            nick_arg=DEFAULT_USERNAME,
            livecycle=DEFAULT_LIVECYCLE,
            last_arena_arg=DEFAULT_LAST_ARENA,
            wrongs_arg=DEFAULT_USUALLY_WRONG,
            wins_arg=DEFAULT_WINS,
            rights_arg=DEFAULT_RIGHTS,
            games_arg=DEFAULT_GAMES_AMOUNT
    ):
        self.id = id_arg
        self.nick = nick_arg
        self.livecycle = livecycle
        self.last_arena = last_arena_arg
        self.wrongs = wrongs_arg
        self.rights = rights_arg
        self.wins = wins_arg
        self.total_games = games_arg

    def update_livecycle_and_total(self, score, rounds, alive):
        total = self.total_games + 1
        cycle = score / rounds if not alive else 1
        self.livecycle = (self.livecycle * self.total_games + cycle) / total
        self.total_games = total
        self.rights += score

    def add_bad_question(self, question: Question):
        if question.id in self.wrongs:
            self.wrongs[question.id] += 1
        else:
            self.wrongs[question.id] = 1

    def __str__(self):
        s = INFO_TEXT % (
            self.id,
            self.total_games,
            (self.livecycle * 100),
            self.last_arena,
            self.rights,
            self.wins
        )
        return s



# class QuestionModel(object):
#     def __inti__(
#             self,
#     ):