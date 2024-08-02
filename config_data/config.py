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
    ("history", "возможность просмотра истории запросов и поиска фильма/сериала"),
    ("quit", "завершить")
)


GENRES_LIST = [
  {
    "name": "аниме",
    "slug": "anime"
  },
  {
    "name": "биография",
    "slug": "biografiya"
  },
  {
    "name": "боевик",
    "slug": "boevik"
  },
  {
    "name": "вестерн",
    "slug": "vestern"
  },
  {
    "name": "военный",
    "slug": "voennyy"
  },
  {
    "name": "детектив",
    "slug": "detektiv"
  },
  {
    "name": "детский",
    "slug": "detskiy"
  },
  {
    "name": "для взрослых",
    "slug": "dlya-vzroslyh"
  },
  {
    "name": "документальный",
    "slug": "dokumentalnyy"
  },
  {
    "name": "драма",
    "slug": "drama"
  },
  {
    "name": "игра",
    "slug": "igra"
  },
  {
    "name": "история",
    "slug": "istoriya"
  },
  {
    "name": "комедия",
    "slug": "komediya"
  },
  {
    "name": "концерт",
    "slug": "koncert"
  },
  {
    "name": "короткометражка",
    "slug": "korotkometrazhka"
  },
  {
    "name": "криминал",
    "slug": "kriminal"
  },
  {
    "name": "мелодрама",
    "slug": "melodrama"
  },
  {
    "name": "музыка",
    "slug": "muzyka"
  },
  {
    "name": "мультфильм",
    "slug": "multfilm"
  },
  {
    "name": "мюзикл",
    "slug": "myuzikl"
  },
  {
    "name": "новости",
    "slug": "novosti"
  },
  {
    "name": "приключения",
    "slug": "priklyucheniya"
  },
  {
    "name": "реальное ТВ",
    "slug": "realnoe-TV"
  },
  {
    "name": "семейный",
    "slug": "semeynyy"
  },
  {
    "name": "спорт",
    "slug": "sport"
  },
  {
    "name": "ток-шоу",
    "slug": "tok-shou"
  },
  {
    "name": "триллер",
    "slug": "triller"
  },
  {
    "name": "ужасы",
    "slug": "uzhasy"
  },
  {
    "name": "фантастика",
    "slug": "fantastika"
  },
  {
    "name": "фильм-нуар",
    "slug": "film-nuar"
  },
  {
    "name": "фэнтези",
    "slug": "fentezi"
  },
  {
    "name": "церемония",
    "slug": "ceremoniya"
  }
]

GENRES_SET = {'игра', 'документальный', 'ужасы', 'реальное ТВ', 'триллер', 'история', 'фильм-нуар', 'мелодрама', 'драма', 'детский', 'аниме', 'семейный', 'концерт', 'ток-шоу', 'комедия', 'новости', 'приключения', 'мультфильм', 'биография', 'спорт', 'церемония', 'боевик', 'для взрослых', 'военный', 'короткометражка', 'детектив', 'фантастика', 'музыка', 'фэнтези', 'мюзикл', 'вестерн', 'криминал'}
