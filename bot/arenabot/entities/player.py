from .recorder_config import ALIVE_ACCESSOR, ID_ACCESSOR, NICK_ACCESSOR, TOTAL_RIGHTS_ACCESSOR
import logging


class Player(object):
    def __init__(self, uid, username):
        self.score = 0
        self.uid = uid
        self.alive = True
        self.name = username
        self.answered = False
        self.bad_question = None

    def kill(self):
        self.alive = False

    def add_points(self, amount=1):
        self.score += amount

    def dump(self):
        answer = {}
        answer[ID_ACCESSOR] = self.uid
        answer[NICK_ACCESSOR] = self.name
        answer[ALIVE_ACCESSOR] = self.alive
        answer[TOTAL_RIGHTS_ACCESSOR] = self.score
        return answer
