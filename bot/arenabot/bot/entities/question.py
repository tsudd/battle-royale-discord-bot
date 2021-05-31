import logging
import random

from .recorder_config import ID_ACCESSOR, QUESTION_RIGHT_ANSWER, QUESTION_STRING_FIELD, QUESTION_ANSWERS_FIELDS, QUESTION_VARIANT, QUESTION_VARIANTS


class Question(object):
    def __init__(self, question_fields: dict):
        self.question_string = question_fields[QUESTION_STRING_FIELD]
        self.id = question_fields[ID_ACCESSOR]
        self.answer = question_fields[QUESTION_RIGHT_ANSWER]

        answers = []
        for var in question_fields[QUESTION_VARIANTS]:
            answers.append([var[QUESTION_VARIANT], False,
                           var[ID_ACCESSOR]])

        logging.info(f"{answers}")
        answers[question_fields[QUESTION_RIGHT_ANSWER] - 1][1] = True
        random.shuffle(answers)

        num = 1
        s = ""
        for answer in answers:
            s += f"{num}. " + answer[0] + '\n'
            if answer[1]:
                self.answer = num
            num += 1

        self.answers_string = s
        self.answers = answers
        # self.description = description

    def get_question_message(self):
        return f"{self.question_string}\n{self.answers_string}\n"

    def check_answer(self, answer: int):
        if answer == self.answer:
            return True
        return False
