from django.urls import path, include
from .views import *

urlpatterns = [
    path('firestore/sessions', sessions_api, name="sessions"),
    path('firestore/topics', topics, name="topics"),
    path('firestore/questions', questions, name="questions"),
    path('firestore/players/<int:pk>', player_info, name="player-detail")
]
