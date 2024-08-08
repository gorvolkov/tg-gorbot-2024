import requests
from config_data.config import API_KEY, API_BASE_URL

from database.models import Movie

headers = {"X-API-KEY": API_KEY}


def _format_movie_data(movie_data: dict) -> Movie:
    """Функция, приводящая данные по каждому фильму в нужный формат"""

    new_movie = Movie()

    new_movie.title = movie_data['name']

    title_orig = movie_data['alternativeName']
    if title_orig:
        new_movie.title_orig = f'({movie_data['alternativeName']})'
    else:
        new_movie.title_orig = ''

    year = movie_data['year']
    if year:
        new_movie.year = movie_data['year']
    else:
        new_movie.year = 'не найден'

    # обрабатываем все полученные жанры и склеиваем в одну строку
    genre_list = []
    genres_parsed = movie_data['genres']
    for genre in genres_parsed:
        genre_list.append(genre['name'])
    genre_str = ', '.join(genre_list)
    new_movie.genres = genre_str

    description = movie_data['description']
    if description:
        new_movie.description = movie_data['description']
    else:
        new_movie.description = 'отсутствует'

    rating_kp = movie_data['rating']['kp']
    if rating_kp:
        new_movie.rating = movie_data['rating']['kp']
    else:
        new_movie.rating = 'не указан'

    age_rating = movie_data['ageRating']
    if age_rating:
        new_movie.age_rating = f'{movie_data['ageRating']}+'
    else:
        new_movie.age_rating = f'не указан'

    poster = movie_data['poster']['previewUrl']
    if poster:
        new_movie.poster = movie_data['poster']['previewUrl']
    else:
        new_movie.poster = 'не найден'
    # постер пока добавляется как URL, и картинка прогружается самим телеграмом. Надо выяснить, как приделать картинку к сообщению

    return new_movie


def _get_selection(resp_data) -> list:
    """Функция, принимающая данные в виде json-объекта, полученные по запросу к API Кинопоиска.
    Возвращает список данных по найденным фильмам"""

    # получаем список с данными по каждому найденному фильму
    selection = resp_data.json()['docs']
    movie_list = []

    for index, movie in enumerate(selection):
        new_movie = _format_movie_data(movie_data=movie)
        movie_list.append(new_movie)

    return movie_list


def get_by_name(name: str, count: int) -> list:
    """Функция, реализующая поиск фильмов по названию.
    Принимает название и заданное число фильмов в выборке,
    отдаёт список с текстами по фильмам"""

    params = {
        'notNullFields': 'name',
        'query': name,
        'limit': count
    }
    response = requests.get(
        f'{API_BASE_URL}/search',
        headers=headers,
        params=params
    )

    result = _get_selection(resp_data=response)
    return result


def get_by_rating(genre: str, count: str, rating: str) -> list:
    """Функция поиска фильмов по рейтингу в рамках заданного жанра"""

    if rating == '10':
        rating_query = '10-10'
    else:
        rating_query = f'{rating}-{rating}.9'

    params = {
        'notNullFields': 'name',
        # добавлено, чтобы убрать из выборки фильмы, которые не выходили на русском языке
        # и результат был сопоставим с выборкой, которую дает приложение Кинопоиска

        'genres.name': genre,
        'limit': count,
        'rating.kp': rating_query,
        'sortField': 'rating.kp',
        'sortType': '1'
    }

    response = requests.get(
        f'{API_BASE_URL}',
        headers=headers,
        params=params
    )

    result = _get_selection(resp_data=response)
    return result


def get_low_budget(genre: str, count: str) -> list:
    """Функция поиска фильмов с высоким бюджетом в рамках заданного жанра"""

    params = {
        'notNullFields': 'name',
        'genres.name': genre,
        'limit': count,
        'sortField': 'budget.value',
        'sortType': '1'
    }

    response = requests.get(
        f'{API_BASE_URL}',
        headers=headers,
        params=params
    )

    result = _get_selection(resp_data=response)
    return result


def get_high_budget(genre: str, count: str) -> list:
    """Функция поиска фильмов с высоким бюджетом в рамках заданного жанра"""

    params = {
        'notNullFields': 'name',
        'genres.name': genre,
        'limit': count,
        'sortField': 'budget.value',
        'sortType': '-1'
    }

    response = requests.get(
        f'{API_BASE_URL}',
        headers=headers,
        params=params
    )

    result = _get_selection(resp_data=response)
    return result