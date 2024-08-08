# Используем базовый образ Ubuntu
FROM ubuntu:latest

# Используем базовый образ Nginx
FROM nginx:alpine AS nginx

# Используем базовый образ Python
FROM python:3.12 AS python
FROM python:3.9-slim

# Используем базовый образ Apache
FROM httpd:2.4 AS apache

LABEL authors="user_Mila"

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip

# Копируем конфигурационные файлы
COPY my-httpd.conf /usr/local/apache2/conf/httpd.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем файлы вашего приложения
COPY ./app /usr/local/apache2/htdocs/
COPY ./app /usr/share/nginx/html

# Копируем оставшийся код приложения в контейнер
COPY templates .

# Открываем порты для бота и серверов
EXPOSE 5000
EXPOSE 80

# Устанавливаем переменные окружения
ENV TELEGRAM_TOKEN="7270899136:AAGCO8kmsW2H0HQUFnitKiC6SOLNGT3DUUE"
ENV assistant="telebot_Mia"
ENV OPENAI_API_KEY="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"
ENV WEATHER_API_KEY="f7a51032f4c134dec171910751b38ff4"
ENV NEWS_API_KEY="b3165457-cc74-4cbb-b056-ff6aa2932955"
ENV FILMS_API_KEY="8b9a6909e5msh52f33564e72f167p185b6fjsnd4942c9e4d9e"
ENV DICTIONARY_API_KEY="26d88ad4-991f-4cab-b329-828e77ec236d"
ENV BASE_URL="http://api.openweathermap.org/data/2.5/weather"
ENV NEWS_URL="https://www.jsonapi.co/public-api/World%20News%20API"
ENV MUSIC_URL="https://open.spotify.com/playlist/1YL4XoegERoragv0RK2RC9?si=J_gjiiNUSwadNb25zIZbIw&dl_branch=1&nd=1&dlsi=19e8d23c01274ee0"
ENV MUSIC_API_KEY="nO9Y4AsZqO7EChld21340LkeJSJjg02O"
ENV FILMS_URL="https://streaming-availability.p.rapidapi.com/shows/%7Btype%7D/%7Bid%7D"
ENV FILMS_URL2="https://kinogo.vin/"
ENV REQUESTS_URL="https://google-news13.p.rapidapi.com/business?lr=en-US"
ENV DICTIONARY_URL="https://Free-Dictionary.allthingsdev.co/endpoint"

# Запуск бота
CMD ["python", "main.py"]

# Запуск Django приложения и сервера Nginx
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000 & nginx -g 'daemon off;'"]