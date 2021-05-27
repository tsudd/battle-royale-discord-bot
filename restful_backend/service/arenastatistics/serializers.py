from rest_framework import serializers
from .models import *


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class QuestionTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTopic
        fields = '__all__'


class QuestionVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionVariant
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    varOne = QuestionVariantSerializer(read_only=True)
    varTwo = QuestionVariantSerializer(read_only=True)
    varThree = QuestionVariantSerializer(read_only=True)
    varFour = QuestionVariantSerializer(read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'question_string',
            'right_ind',
            "varOne",
            "varTwo",
            "varThree",
            "varFour",
            "topic"
        ]


class SessionSerializer(serializers.ModelSerializer):
    topic = QuestionTopicSerializer(read_only=True)
    date = serializers.DateTimeField(format='%d.%m.%Y %H:%M')

    class Meta:
        model = Session
        fields = [
            "id",
            "players_amount",
            "rounds_amount",
            "date",
            "topic"
        ]


class RoundSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(
        read_only=True,
        slug_field="question_string"
    )

    class Meta:
        model = Round
        fields = [
            "session",
            "question"
        ]

# why?


class ParticipationSerializer(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = [
            "session"
        ]


class AnswerSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField(
        read_only=True,
        slug_field="dis_id"
    )
    answer = serializers.SlugRelatedField(
        read_only=True,
        slug_field="variant"
    )

    class Meta:
        model = Answer
        fields = [
            "player",
            "right",
            "answer",
        ]
