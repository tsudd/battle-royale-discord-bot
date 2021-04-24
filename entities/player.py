import logging


class Player(object):
    def __init__(self, uid, username):
        self.score = 0
        self.uid = uid
        self.alive = True
        self.name = username

    def kill(self):
        self.alive = False

    def add_points(self, amount=1):
        self.score += amount
