import os
import sys
import pyttsx3
import requests
import subprocess
from datetime import datetime
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import webbrowser

# Инициализация голосового движка при запуске программы
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # скорость речи


def alarm(text):
    engine.say(text)
    engine.runAndWait()


def open_browser():
    webbrowser.open('https://www.youtube.com', new=2)


def open_game():
    subprocess.Popen('C:/Program Files/paint.net/PaintDotNet.exe')


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: alarm("Подъем! Время вставать!"), 'cron', hour=6, minute=0)
    scheduler.start()


def fetch_weather():
    params = {'q': 'Minsk', 'units': 'metric', 'lang': 'ru', 'appid': 'f7a51032f4c134dec171910751b38ff4'}
    response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)

    if response.status_code == 200:
        weather_data = response.json()
        description = weather_data['weather'][0]['description']
        temperature = round(weather_data['main']['temp'])

        engine.say(f'На улице {description}, температура {temperature} градусов Цельсия.')
        engine.runAndWait()
    else:
        print("Error fetching weather data")
        fetch_weather()


def fetch_weather_google():
    response = requests.get('https://www.google.com/search?q=weather+London')
    soup = BeautifulSoup(response.text, 'html.parser')
    location = soup.select_one('div#wob_loc').text
    info = soup.select_one('span#wob_dc').text
    temperature = soup.select_one('span#wob_tm').text
    engine.say(f'Сейчас в {location} {info}, температура {temperature} градусов Цельсия.')
    engine.runAndWait()


def fetch_news():
    response = requests.get('https://allnews.ng/')
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.select('h2.title')[:5]
    news = [headline.text for headline in headlines]
    for idx, headline in enumerate(news, 1):
        engine.say(f'Новость {idx}: {headline}')
    engine.runAndWait()
    return news


def suggest_movie():
    response = requests.get('https://www.allmovie.com/')
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.select('.title a')[:5]
    movies = [title.text.strip() for title in titles]
    for idx, movie in enumerate(movies, 1):
        print(f"Movie {idx}: {movie}")
        engine.say(f"Movie {idx}: {movie}")
        engine.runAndWait()
    return movies


def play_music():
    webbrowser.open("https://www.spotify.com")


def offbot():
    sys.exit()


def passive():
    pass


def offpc():
    os.system('shutdown /s /t 0')
    print('ПК выключен')


def run_tests():
    print("Testing alarm function...")
    alarm("This is a test alarm")

    print("Testing open_browser function...")
    open_browser()

    print("Testing open_game function...")
    open_game()

    print("Testing fetch_weather function...")
    fetch_weather()

    print("Testing fetch_weather_google function...")
    fetch_weather_google()

    print("Testing fetch_news function...")
    news = fetch_news()
    print(news)

    print("Testing suggest_movie function...")
    movies = suggest_movie()
    print(movies)

    print("Testing play_music function...")
    play_music()

    print("Testing offbot function...")
    # offbot()

    print("Testing offpc function...")
    # offpc()


if __name__ == "__main__":
    start_scheduler()
    run_tests()
