import os
import sys
import random
from gtts import gTTS
import time
import speech_recognition as sr
from playsound import playsound
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pyttsx3
import requests
from bs4 import BeautifulSoup
import webbrowser

# Provide the correct path to the sound file
playsound('path_to_sound_file.mp3')

TRIGGERS = {'Mia', 'assistant Mia', 'friend Mia'}

data_set = {
    'привет': 'и тебе, привет',
    'какая сейчас погода': 'weather сейчас скажу',
    'какая погода на улице': 'weather боишься замерзнуть?',
    'что там на улице': 'weather сейчас гляну',
    'сколько градусов': 'weather можешь выглянуть в окно, но сейчас проверю',
    'запусти браузер': 'browser запускаю браузер',
    'открой браузер': 'browser открываю браузер',
    'открой интернет': 'browser интернет активирован',
    'играть': 'game лишь бы баловаться',
    'хочу поиграть в игру': 'game а нам лишь бы баловаться',
    'запусти игру': 'game запускаю, а нам лишь бы баловаться',
    'посмотреть фильм': 'browser сейчас открою браузер',
    'выключи компьютер': 'offpc отключаю',
    'отключись': 'offbot отключаюсь',
    'как у тебя дела': 'passive работаю в фоне, не переживай',
    'что делаешь': 'passive жду очередной команды, мог бы и сам на кнопку нажать',
    'работаешь': 'passive как видишь',
    'расскажи анекдот': 'passive вчера помыл окна, теперь у меня рассвет на 2 часа раньше',
    'ты тут': 'passive вроде, да',
    'how are you doing today': 'passive nice, and what about you',
    'good night': 'passive bye, bye',
    'пока': 'passive Пока'
}

OPENWEATHER_API_KEY = 'f7a51032f4c134dec171910751b38ff4'


def alarm(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: alarm("Подъем! Время вставать!"), 'cron', hour=6, minute=0)
    scheduler.start()


def fetch_weather():
    f"""https://api.openweathermap.org/data/2.5/weather?q=Minsk&appid={'f7a51032f4c134dec171910751b38ff4'}&units=metric&lang=ru"""
    response = requests.get('https://www.worldweatheronline.com/country.aspx')
    weather_data = response.json()
    current_weather = weather_data['weather'][0]  # Adjusted key based on typical OpenWeatherMap API response
    temperature = weather_data['main']['temp']
    return f"Current temperature: {temperature}°C, {current_weather['description']}"


def fetch_news():
    response = requests.get('https://allnews.ng/')
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.select('https://m.youtube.com/@setstories?reload=9')[:5]
    news = [headline.text for headline in headlines]
    return news


def suggest_movie():
    response = requests.get('https://www.allmovie.com/')
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.select('Iron Man')[:5]
    movies = [title.text for title in titles]
    return movies


def play_music():
    webbrowser.open("https://www.spotify.com")



def respond_to_command(command):
    response = data_set.get(command.lower(), "Команда не распознана")
    if response.startswith('weather'):
        weather_info = fetch_weather()
        print(weather_info)
        alarm(weather_info)
    elif response.startswith('browser'):
        print("Opening browser...")
        webbrowser.open("https://www.google.com")
    elif response.startswith('game'):
        print("Starting game...")
        # Add your game starting code here
    elif response.startswith('offpc'):
        print("Shutting down computer...")
        os.system('shutdown /s /t 1')
    elif response.startswith('offbot'):
        print("Shutting down bot...")
        sys.exit()
    else:
        print(response)
        alarm(response)


def main():
    start_scheduler()
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            print("Listening for a command...")
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Recognized command: {command}")

            if any(trigger in command for trigger in TRIGGERS):
                command = command.replace('Mia', '').strip()
                respond_to_command(command)

        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")


if __name__ == "__main__":
    main()
