from django.db import models
from ..service.settings import DEFAULT_EMPTY_STRING
# Create your models here.


class Player(models.Model):
    dis_id = models.IntegerField("User ID", default=228)
    nick = models.CharField("Nickname", max_length=90, default="NO NICK")
    lifetime = models.FloatField("Average lifetime", default=1)
    games_amount = models.IntegerField("Arenas played", default=0)
    wins = models.IntegerField("Won in total", default=0)

    def __str__(self):
        return f"{self.nick} with {self.games_amount} games."


class QuestionTopic(models.Model):
    name = models.CharField("Topic name", default=DEFAULT_EMPTY_STRING)

    def __str__(self):
        return f"{self.name} topic."


class QuestionVariant(models.Model):
    variant = models.TextField("Variant 1", max_length=300, default=DEFAULT_EMPTY_STRING)

    def __str__(self):
        return f"Question variant {self.variant}"


class Question(models.Model):
    question_string = models.TextField("Question", max_length=300, default=DEFAULT_EMPTY_STRING)
    variant_1 = models.TextField("Variant 1", max_length=300, default=DEFAULT_EMPTY_STRING)
    variant_2 = models.TextField("Variant 2", max_length=300, default=DEFAULT_EMPTY_STRING)
    variant_3 = models.TextField("Variant 3", max_length=300, default=DEFAULT_EMPTY_STRING)
    variant_4 = models.TextField("Variant 4", max_length=300, default=DEFAULT_EMPTY_STRING)
    right_ind = models.IntegerField("Index of the right answer", default=1)
    topic = models.ForeignKey(QuestionTopic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Question {self.question_string}."


class Session(models.Model):
    players_amount = models.IntegerField("Players amount",  default=0)
    rounds_amount = models.IntegerField("Rounds played", default=1)
    date = models.DateTimeField("Arena ended", auto_now_add=True)
    topic = models.ForeignKey(QuestionTopic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Session of {self.date} with {self.topic}"


class Round(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    variant_1 = models.TextField("Variant 1", max_length=300, default=DEFAULT_EMPTY_STRING)
    variant_2 = models.TextField("Variant 2", max_length=300, default=DEFAULT_EMPTY_STRING)
    variant_3 = models.TextField("Variant 3", max_length=300, default=DEFAULT_EMPTY_STRING)
    variant_4 = models.TextField("Variant 4", max_length=300, default=DEFAULT_EMPTY_STRING)
    right_ind = models.IntegerField("Index of the right answer", default=-1)

    def __str__(self):
        return f"Round of session {self.session} with question {self.question}."


class Participation(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Participation record of {self.player} player."


class Answer(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.IntegerField("Selected answer", default=-1)
    right = models.BooleanField("Answer is right", default=False)

    def __str__(self):
        return f"{self.right} answer of {self.player} player."
