from django.urls import path
from .views import *

urlpatterns = [
    path("play/", play, name="play_game"),
    path('', index, name="game_index"),
]
