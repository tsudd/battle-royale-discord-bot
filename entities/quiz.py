import logging
import random
import datetime
from .player import Player
from .question import Question

from config import PRINT_HL, RULES_MESSAGE, WINNERS_AMOUNT
from .recorder_config import QUESTION_STRING_FIELD, QUESTION_ANSWERS_FIELD, QUESTION_DESCRIPTION, ID_ACCESSOR


class Quiz(object):
    def __init__(self, cid, initiator, players: list, question_types: list, data: dict, time_to_ans=10, rounds=10):
        self.players = {}
        self.cid = cid
        self.initiator = initiator
        self.state = State()
        self.topics = question_types
        self.answer_time = time_to_ans
        self.rounds_amount = rounds
        self.question_message = None

        for player in players:
            self.players[player.id] = Player(player.id, player.name)

        self.questions = []
        diff_question = []
        for typ in question_types:
            diff_question += data[typ]

        random.shuffle(diff_question)

        for question in diff_question[:self.rounds_amount]:
            self.questions.append(Question(
                question[QUESTION_STRING_FIELD],
                question[QUESTION_ANSWERS_FIELD],
                question[ID_ACCESSOR]
                )
            )

        self.question_stack = [*self.questions]
        self.state.player_counter = len(self.players)
        self.state.question_amount = len(self.questions)

        logging.info(f"Game in {self.cid} with {self.state.question_amount} questions was created.")

    def check_answers_and_kill(self, player_answers: dict, question: Question):
        kill_uid_list = []
        for playerid, answer in player_answers.items():
            if not question.check_answer(answer):
                self.players[playerid].kill()
                self.players[playerid].bad_question = self.state.last_question
                logging.info(f"{self.players[playerid].name} was killed!")
                self.state.dead_players.append(self.players[playerid])
                kill_uid_list.append(playerid)
            else:
                logging.info(f"{self.players[playerid].name} got points after write answer!")
                self.players[playerid].add_points(len(question.answer))
        self.state.last_ban_amount = len(kill_uid_list)
        self.state.dead_counter += self.state.last_ban_amount
        self.state.player_counter -= self.state.last_ban_amount
        self.state.question_answered += 1
        return kill_uid_list

    def get_question(self):
        if len(self.question_stack) == 0:
            return "No question."
        q = self.question_stack.pop()

        logging.info(f"New question was sent to players - {q.question_string}")
        self.state.last_question = q

        return q.get_question_message()

    def get_round_result(self):
        ans = f"Round result.\nStill in game {self.state.player_counter}:\n"

        for uid, player in self.players.items():
            if not player.alive:
                continue
            ans += f" - {player.name} - {player.score} points. (+{self.state.added_score})\n"

        ans += f"{self.state.last_ban_amount} players was banned.\n"
        logging.info(f"Round ended.\n{ans}")
        return ans

    def get_game_result(self):
        if self.state.game_in_progress:
            return "Game still in progress."

        ans = PRINT_HL
        ans += f"After {self.state.question_answered} rounds battle ended.\n"
        ans += PRINT_HL
        ans += "Survivors and scores:\n"

        for uid, player in self.players.items():
            if not player.alive:
                continue
            ans += f" - {player.name} - {player.score} points.\n"

        ans += PRINT_HL
        ans += "Who didn't make it...\n"
        date = datetime.datetime.now().strftime("%d.%m.%Y")
        for player in self.state.dead_players:
            ans += f" F to {player.name}(?-{date}) - {player.score} points.\n"

        logging.info(f"Round results.\n{ans}")
        return ans

    def get_start_quiz(self):
        if not self.state.game_in_progress:
            return f"This game is no longer active."

        ans = RULES_MESSAGE % (self.rounds_amount, self.answer_time)
        ans += f"Lets meet our warriors:\n"

        for uid, player in self.players.items():
            ans += f" - {player.name} - {player.score} points.\n"

        ans += "In this game you will meet "
        for topic in self.topics:
            ans += f"{topic} "
        ans += "topics. Forewarned is forearmed. "

        ans += "The game will start when all participants vote (click on the emoji below this message, please."
        logging.info(f"The game in {self.cid} with {self.state.player_counter} player is about to start")
        return ans

    def get_start_new_round(self):
        ans = f"Round {self.state.question_answered + 1}.\n\nPlayers dead {self.state.dead_counter}. Players alive " \
               f"{len(self.players)}.\n"

        ans += self.get_question()
        self.state.last_ban_amount = 0
        logging.info(f"Round {self.state.question_answered} in {self.cid} started.")
        return ans

    def is_game_end(self):
        if self.state.player_counter <= 1:
            self.state.game_in_progress = False
        if self.state.question_answered == self.state.question_amount:
            self.state.game_in_progress = False

    def update_answer_statuses(self):
        for uid, player in self.players.items():
            player.answered = False


class State(object):
    def __init__(self):
        self.dead_counter = 0
        self.player_counter = 0
        self.question_amount = 0
        self.question_answered = 0
        self.game_in_progress = True
        self.added_score = 1
        self.game_ended = False
        self.last_question = None
        self.last_ban_amount = 0
        self.dead_players = []
