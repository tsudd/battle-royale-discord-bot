import json
import logging
import datetime

from .quiz import Quiz
from .recorder_config import *
from .stat_models import PlayerModel
from .player import Player


class Recorder(object):
    def __init__(self, data_file=None, question_base=None):
        self.data = None
        self.filename = data_file
        self.data = Recorder.load_data(data_file)
        self.questions = question_base
        self.records = {}
        if self.data is not None and PLAYERS_MODELS_ACCESSOR in self.data:
            for record in self.data[PLAYERS_MODELS_ACCESSOR]:
                self.records[record[ID_ACCESSOR]] = PlayerModel(
                    record[ID_ACCESSOR],
                    record[NICK_ACCESSOR],
                    record[LIVECYCLE_ACCESSOR],
                    record[LAST_ARENA_ACCESSOR],
                    record[USUALLY_WRONG_ACCESSOR],
                    record[WINS_ARENAS_ACCESSOR],
                    record[TOTAL_RIGHTS_ACCESSOR]
                )

    def update_or_add_player(self, player: Player, quiz: Quiz):
        if player.uid not in self.records:
            logging.info(f"Adding new player to base info - {player.name}")
            self.records[player.uid] = PlayerModel(
                player.uid,
                player.name
            )
        logging.info(f"Updating record about {player.name}")
        model = self.records[player.uid]
        model.update_livecycle_and_total(player.score, quiz.state.question_answered, player.alive)
        model.last_arena = datetime.datetime.now().strftime("%d.%m.%Y")
        if player.alive:
            model.wins += 1
        else:
            model.add_bad_question(player.bad_question)

    def save_data(self):
        logging.info(f"Saving stats in file {DEFAULT_FILENAME}")
        fs = open(DEFAULT_FILENAME, "w")
        data = {PLAYERS_MODELS_ACCESSOR: list(self.records.values())}
        json.dump(data, fs)
        fs.close()

    @staticmethod
    def load_data(filename):
        assert type(filename) == str
        data = {}
        try:
            logging.info(f"Parsing {filename} with data...")
            f = open(filename, "r")
            data = json.load(f)
            f.close()
        except FileNotFoundError:
            logging.info(f"Couldn't parse {filename}: file doesn't exist.")
            raise ValueError
        except Exception as e:
            logging.info(f"Couldn't parse {filename} because of {e}")
            raise ValueError
        else:
            return None
        finally:
            return data

    def get_player(self, uid):
        if uid in self.records:
            return str(self.records[uid]) + self.get_player_misses(self.records[uid].wrongs)
        else:
            return NO_PLAYER % uid

    def get_question_string(self, id_arg):
        ans = ""
        try:
            for topic, lt in self.questions.items():
                for q in lt:
                    if q[ID_ACCESSOR] == id_arg:
                        ans = q[QUESTION_STRING_FIELD]
        except KeyError:
            ans = NO_QUESTIONS
        return ans

    def get_player_misses(self, player_misses):
        if len(player_misses) == 0:
            return ""
        s = WRONGS_TITLE
        for qid, count in player_misses.items():
            s += f"{qid}. {self.get_question_string(qid)} - {count}\n"
        return s

