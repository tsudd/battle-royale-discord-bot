from django.db import models

DEFAULT_EMPTY_STRING = "Empty"

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
    name = models.CharField("Topic name", max_length=30,
                            default=DEFAULT_EMPTY_STRING)
    emoji = models.CharField("Topic emoji", max_length=10, default="🖕🏻")

    def __str__(self):
        return f"{self.name} topic."


class QuestionVariant(models.Model):
    variant = models.TextField(
        "Variant", max_length=300, default=DEFAULT_EMPTY_STRING)

    def __str__(self):
        return f"Question variant {self.variant}"


class Question(models.Model):
    question_string = models.TextField(
        "Question", max_length=300, default=DEFAULT_EMPTY_STRING)
    varOne = models.ForeignKey(QuestionVariant, on_delete=models.CASCADE,
                               null=True, blank=True, related_name="first_question_variant")
    varTwo = models.ForeignKey(QuestionVariant, on_delete=models.CASCADE,
                               null=True, blank=True, related_name="second_question_variant")
    varThree = models.ForeignKey(QuestionVariant, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name="third_question_variant")
    varFour = models.ForeignKey(QuestionVariant, on_delete=models.CASCADE,
                                null=True, blank=True, related_name="fourth_question_variant")
    right_ind = models.IntegerField("Index of the right answer", default=1)
    topic = models.ForeignKey(
        QuestionTopic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Question {self.question_string}."


class Session(models.Model):
    players_amount = models.IntegerField("Players amount",  default=0)
    rounds_amount = models.IntegerField("Rounds played", default=1)
    date = models.DateTimeField("Arena ended", auto_now_add=True)
    topic = models.ForeignKey(
        QuestionTopic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Session of {self.date} with {self.topic}"


class Round(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, blank=True)
    first_variant = models.ForeignKey(
        QuestionVariant, on_delete=models.CASCADE, null=True, blank=True, related_name="first_round_variant")
    second_variant = models.ForeignKey(
        QuestionVariant, on_delete=models.CASCADE, null=True, blank=True, related_name="second_round_variant")
    three_variant = models.ForeignKey(
        QuestionVariant, on_delete=models.CASCADE, null=True, blank=True, related_name="third_round_variant")
    four_variant = models.ForeignKey(
        QuestionVariant, on_delete=models.CASCADE, null=True, blank=True, related_name="fouth_round_variant")
    right_ind = models.IntegerField("Index of the right answer", default=-1)

    def __str__(self):
        return f"Round of session {self.session} with question {self.question}."


class Participation(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, null=True, blank=True)
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Participation record of {self.player} player."


class Answer(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, null=True, blank=True)
    round = models.ForeignKey(
        Round, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, blank=True)
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(
        QuestionVariant, on_delete=models.CASCADE, null=True, blank=True)
    right = models.BooleanField("Answer is right", default=False)

    def __str__(self):
        return f"{self.right} answer of {self.player} player."
