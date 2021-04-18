import logging
from player import Player
from question import Question

from config import QUESTION_STRING_FIELD, QUESTION_ANSWERS_FIELD


class Quiz(object):
    def __init__(self, cid, initiator, players: list, question_types: list, data: dict):
        self.player_list = {}
        self.cid = cid
        self.initiator = initiator

        self.players_list = []
        for player in players:
            self.players_list.append(Player(player.uid, player.name))

        self.questions = []
        for type in question_types:
            for question in data[type]:
                self.questions.append(Question(question[QUESTION_STRING_FIELD], question[QUESTION_ANSWERS_FIELD]))

        # add shuffle questions here

        logging.info(f"Game in {self.cid} with {len(self.questions)} questions was created.")

