import logging


class Question(object):
    def __init__(self, question_string: str, answers: list):
        self.question_string = question_string
        self.answer = []

        # add shuffling answers
        s = ""

        num = 1
        for answer in answers:
            s += f"{num}. " + answer[0] + '\n'
            if answer[1]:
                self.answer.append(num)
            num += 1

        self.answers_string = s





