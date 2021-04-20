import logging
import random


class Question(object):
    def __init__(self, question_string: str, answers: list, description=""):
        self.question_string = question_string
        self.answer = []

        random.shuffle(answers)
        s = ""

        num = 1
        for answer in answers:
            s += f"{num}. " + answer[0] + '\n'
            if answer[1]:
                self.answer.append(num)
            num += 1

        self.answers_string = s
        self.description = description

    def get_question_message(self):
        return f"{self.question_string}\n{self.answers_string}\n\nP. S. {self.description}."

    def check_answer(self, answer: list):
        hits = 0
        for v in answer:
            if v in self.answer:
                hits += 1
        if hits == len(self.answer):
            return True
        return False





