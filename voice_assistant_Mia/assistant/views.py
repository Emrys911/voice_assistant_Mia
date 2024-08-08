from rest_framework import serializers
from .models import Assistant
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import Assistant
from .serializers import AssistantSerializer
from .tasks import fetch_weather, fetch_news, suggest_movie, play_music


class AssistantView(generics.ListCreateAPIView):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer


class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = '__all__'
        serializer_class = AssistantSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request)
        # Add your training logic here
        return response


@api_view(['GET'])
def get_weather(request):
    weather = fetch_weather()
    return Response({"weather": weather})


@api_view(['GET'])
def get_news(request):
    news = fetch_news()
    return Response({"news": news})


@api_view(['GET'])
def get_movies(request):
    movies = suggest_movie()
    return Response({"movies": movies})


@api_view(['GET'])
def play_music_view(request):
    play_music()
    return Response({"message": "Playing music"})
