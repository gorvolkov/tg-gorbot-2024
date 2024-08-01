import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
API_BASE_URL = "https://api.kinopoisk.dev/"
ALL_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("movie_search", "поиск фильма/сериала по названию"),
    ("movie_by_rating", "поиск фильмов/сериалов по рейтингу"),
    ("low_budget_movie", "поиск фильмов/сериалов с низким бюджетом"),
    ("high_budget_movie", "поиск фильмов/сериалов с высоким бюджетом"),
    ("history", "возможность просмотра истории запросов и поиска фильма/сериала")
)


