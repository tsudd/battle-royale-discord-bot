from rest_framework import serializers
from models import *


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
    variant_1 = QuestionVariantSerializer(read_only=True)
    variant_2 = QuestionVariantSerializer(read_only=True)
    variant_3 = QuestionVariantSerializer(read_only=True)
    variant_4 = QuestionVariantSerializer(read_only=True)
    topic = QuestionTopicSerializer(read_only=True)

    class Meta:
        model = Question
        fields = [
            'question_string',
            'right_ind',
            "variant_1",
            "variant_2",
            "variant_3",
            "variant_4",
            "topic"
        ]


class SessionSerializer(serializers.ModelSerializer):
    topic = QuestionTopicSerializer(read_only=True)

    class Meta:
        model = Session
        fields = [
            "players_amount",
            "rounds_amount",
            "date",
            "topic"
        ]


class RoundSerializer(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)
    variant_1 = QuestionVariantSerializer(read_only=True)
    variant_2 = QuestionVariantSerializer(read_only=True)
    variant_3 = QuestionVariantSerializer(read_only=True)
    variant_4 = QuestionVariantSerializer(read_only=True)

    class Meta:
        model = Round
        fields = "__all__"

# why?
# class ParticipationSerializer


class AnswerSerializer(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)
    round = RoundSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = "__all__"
