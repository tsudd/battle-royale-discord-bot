from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .serializers import *
from .models import *

import random
import logging

# Create your views here.


class TopicsList(generics.ListAPIView):
    serializer_class = QuestionTopicSerializer
    queryset = QuestionTopic.objects.all()


class QuestionsList(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def get(self, request, *args, **kwargs):
        params = dict(request.query_params)
        amount = 10
        questions = []
        if 'amount' in params:
            amount = int(params['amount'][0])
        if 'topic' in params:
            topic_id = int(params['topic'][0])
            all_questoins = list(Question.objects.filter(topic__id=topic_id))
            random.shuffle(all_questoins)
            questions = all_questoins[0:amount]
            logging.info(
                f"Sending questions list by params: amount - {amount}, topic - {topic_id}")
            return Response(
                self.serializer_class(
                    questions, many=True, context=self.get_serializer_context()).data
            )
        else:
            return super().get(request, args, kwargs)
