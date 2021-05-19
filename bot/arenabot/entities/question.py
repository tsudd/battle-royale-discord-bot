import logging
import random

from .recorder_config import ID_ACCESSOR, QUESTION_RIGHT_ANSWER, QUESTION_STRING_FIELD, QUESTION_ANSWERS_FIELDS


class Question(object):
    def __init__(self, question_fields: dict):
        self.question_string = question_fields[QUESTION_STRING_FIELD]
        self.id = question_fields[ID_ACCESSOR]
        self.answer = question_fields[QUESTION_RIGHT_ANSWER]

        answers = []
        for var in QUESTION_ANSWERS_FIELDS:
            answers.append([question_fields[var], False])

        answers[question_fields[self.answer - 1]][1] = True
        random.shuffle(answers)

        num = 1
        s = ""
        for answer in answers:
            s += f"{num}. " + answer[0] + '\n'
            if answer[1]:
                self.answer = num
            num += 1

        self.answers_string = s
        # self.description = description

    def get_question_message(self):
        return f"{self.question_string}\n{self.answers_string}\n"

    def check_answer(self, answer: int):
        if answer == self.answer:
            return True
        return False
