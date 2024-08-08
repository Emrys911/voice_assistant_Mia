
from django.urls import path
from .views import AssistantView

urlpatterns = [
    path('assistant/', AssistantView.as_view(), name='assistant'),
    path('weather/', get_weather, name='weather'),
    path('news/', get_news, name='news'),
    path('movies/', get_movies, name='movies'),
    path('play_music/', play_music_view, name='play_music'),
]
