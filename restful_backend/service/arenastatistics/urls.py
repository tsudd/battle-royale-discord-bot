from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/topics', TopicsList.as_view(), name="topics"),
    path('api/questions', QuestionsList.as_view(), name="questions"),
    path('api/sessions', SessionsList.as_view(), name="sessions"),
    path('api/players', PlayerDetail.as_view(), name="players"),
    path('api/sessions/<int:pk>', SessionDetail.as_view(), name="session-detail")
]
