import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from conf import users
from gpt_message_handler import handle_response
import openai
import requests
from bs4 import BeautifulSoup
import sqlalchemy as db
from datetime import datetime
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
from telegram.ext import ApplicationBuilder

print('Starting up bot...')

load_dotenv()

print('Starting up bot...')

load_dotenv()

TOKEN = os.getenv('7270899136:AAGCO8kmsW2H0HQUFnitKiC6SOLNGT3DUUE')  # Fixed the environment variable name
BOTNAME = os.getenv('telebot_Mia')
openai.api_key = os.getenv('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')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Create a decorator that takes users as an argument and if the user is in the list, it will run the function
def user_allowed(users):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.message.from_user
            logging.info(
                f'User {user.username} is trying to access the bot. id: {user.id}, message: {update.message.text}')
            if user.username in users:
                await func(update, context)
            else:
                await update.message.reply_text('You are not allowed to use this command')

        return wrapper

    return decorator


@user_allowed(users)
async def start_command(update: Update):
    await update.message.reply_text('Привет! Я ваш голосовой помощник. Спросите меня о погоде, новостях или фильмах!')


engine = pyttsx3.init()

# Возможность настройки скорости голоса
engine.setProperty('rate', 150)


# Основная функция для синтеза и произнесения речи
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Пример использования
speak("Привет, как могу помочь вам?")


@user_allowed(users)
async def help_command(update: Update ):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')


@user_allowed(users)
async def custom_command(update: Update):
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')
    pass


@user_allowed(users)
async def restart_command(update: Update):
    sqlitre = db.create_engine("sqlite:///db.sqlite3")
    connection = sqlitre.connect()
    metadata = db.MetaData()

    try:
        conversations = db.Table('conversations', metadata, autoload=True, autoload_with=sqlitre)
    except:
        conversations = db.Table('conversations',
                                 metadata,
                                 db.Column('id', db.Integer, primary_key=True),
                                 db.Column('user_id', db.Integer),
                                 db.Column('user_name', db.String),
                                 db.Column('user_message', db.String),
                                 db.Column('message_id', db.Integer),
                                 db.Column('bot_response', db.String),
                                 db.Column('created_at', db.DateTime, default=datetime.now))

        metadata.create_all(sqlitre)
    query = db.delete(conversations)
    connection.execute(query)
    print('Deleted all rows from conversations table')
    await update.message.reply_text('Restarted the bot.')


users = []


def fetch_weather():
    url = f'http://api.openweathermap.org/data/2.5/weather?q=Минск&appid={os.getenv("f7a51032f4c134dec171910751b38ff4")}&units=metric&lang=ru'
    response = requests.get(url)
    weather_data = response.json()
    current_weather = weather_data['weather'][0]['description']
    current_temp = weather_data['main']['temp']
    return f"Текущая температура: {current_temp}°C, {current_weather}"


def fetch_requests():
    os.getenv('8b9a6909e5msh52f33564e72f167p185b6fjsnd4942c9e4d9e')
    f'https: https://streaming-availability.p.rapidapi.com/shows/%7Btype%7D/%7Bid%7D=ru&apiKey={'8b9a6909e5msh52f33564e72f167p185b6fjsnd4942c9e4d9e'}'
    response = requests.get('https://google-news13.p.rapidapi.com/business?lr=en-US')
    requests_data = response.json()
    return requests_data


def fetch_news():
    os.getenv('b3165457-cc74-4cbb-b056-ff6aa2932955')
    fetch('https://www.jsonapi.co/public-api/World%20News%20API')
    response = requests.get('b3165457-cc74-4cbb-b056-ff6aa2932955')
    news_data = response.json()
    return news_data


def fetch_music():
    api_key = os.getenv('nO9Y4AsZqO7EChld21340LkeJSJjg02O')
    url = fetch('https://open.spotify.com/playlist/1YL4XoegERoragv0RK2RC9?si=J_gjiiNUSwadNb25zIZbIw&dl_branch=1&nd=1&dlsi=19e8d23c01274ee0')
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    music_data = response.json()
    return music_data


def suggest_movie():
    url = fetch('https://streaming-availability.p.rapidapi.com/shows/%7Btype%7D/%7Bid%7D')
    headers = {
        "X-RapidAPI-Host": "imdb-movies-web-series-etc-search.p.rapidapi.com",
        "X-RapidAPI-Key": ''
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = [tag.text.strip() for tag in soup.select('.movies')[:5]]
    return movies


def dictionary_api():
    url = fetch('https://Free-Dictionary.allthingsdev.co/endpoint')
    headers = {
        "X-RapidAPI-Host": "imdb-movies-web-series-etc-search.p.rapidapi.com",
        "X-RapidAPI-Key": '26d88ad4-991f-4cab-b329-828e77ec236d'
    }
    response = requests.get(url, headers=headers)
    dict_data = response.json()
    definitions = [entry['meanings'][0]['definitions'][0]['definition'] for entry in dict_data]
    return definitions
    print(response.status_code)
    print(response.json())


def play_music():
    return "Playing music on Spotify"


@user_allowed(users)
async def weather_command(update: Update):
    weather = fetch_weather()
    await update.message.reply_text(weather)


@user_allowed(users)
async def news_command(update: Update):
    news = fetch_news()
    news_message = "\n".join(news)
    await update.message.reply_text(news_message)


@user_allowed(users)
async def movies_command(update: Update):
    movies = suggest_movie()
    movies_message = "\n".join(movies)
    await update.message.reply_text(movies_message)


@user_allowed(users)
async def music_command(update: Update):
    music_message = play_music()
    await update.message.reply_text(music_message)


@user_allowed(users)
async def handle_message(update: Update):
    print('Message received')
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    user = update.message.from_user
    message_id = update.message.message_id
    response = ''

    print(f'User ({update.message.chat.id}) says: "{text}" in: {message_type}')

    if text.startswith(BOTNAME.lower()):
        response = handle_response(text, user, message_id)

    await update.message.reply_text(response)


@user_allowed(users)
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Function to convert text to speech and save as MP3
def text_to_speech_mp3(text, filename):
    tts = gTTS(text=text, lang='ru')
    tts.save(filename)


# Example usage
text_to_speech_mp3("Привет, как могу помочь вам?", "output.mp3")


# Function for speech recognition
def recognize_speech_from_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='ru-RU')
        return text
    except sr.UnknownValueError:
        return "Не удалось распознать речь"
    except sr.RequestError as e:
        return f"Ошибка сервиса распознавания речи: {e}"


if __name__ == '__main__':
    application = ApplicationBuilder().token('7270899136:AAGCO8kmsW2H0HQUFnitKiC6SOLNGT3DUUE').build()

    application.add_handler(CommandHandler('weather', weather_command))
    application.add_handler(CommandHandler('news', news_command))
    application.add_handler(CommandHandler('movies', movies_command))
    application.add_handler(CommandHandler('music', music_command))

    application.add_handler(MessageHandler(filters.ALL, handle_message))

    application.add_error_handler(error_handler)
    application.run_polling()
