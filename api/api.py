import requests
import json
from typing import List, Dict
from config_data.config import API_KEY, API_BASE_URL

headers = {"X-API-KEY": API_KEY}

# def api_request(endpoint: str, params={}) -> requests.Response:
#     params['key'] = API_KEY
#     # return requests.get(
#     #     f'{API_BASE_URL}/{endpoint}',
#     #     params=params
#     # )
#     return
#
# def get_langs() -> List[str]:
#     response = api_request('getLangs');
#     return response.json()
#
#
# def lookup(lang: str, text: str, ui: str = 'ru') -> Dict:
#     response = api_request('lookup', params={
#         'lang': lang,
#         'text': text,
#         'ui': ui
#     })
#
#     return response.json().get('def', {})


def get_movie_by_title(title: str) -> dict:
    """Функция, выполняющая поиск сведений о фильме в каталоге Кинопоиска"""

    params = {
        'query': title
    }
    response = requests.get(
        'https://api.kinopoisk.dev/v1.4/movie/search',
        headers=headers,
        params=params
    )
    return response.json()


def format_movie_data(movie_data: dict) -> str:
    """Функция, форматирующая вывод данных по одному фильму"""

    title = movie_data['docs'][0]['name']
    title_orig = movie_data['docs'][0]['alternativeName']
    year = movie_data['docs'][0]['year']

    genre_list = []
    genres = movie_data['docs'][0]['genres']
    for genre in genres:
        genre_list.append(genre['name'])
    genre_str = ', '.join(genre_list)

    description = movie_data['docs'][0]['description']
    rating = movie_data['docs'][0]['description']
    age_rating = f'{movie_data['docs'][0]['ageRating']}+'
    poster = movie_data['docs'][0]['poster']['previewUrl']
    # необходимо решить с добавлением постера к выдаче

    text = (f"Название: {title} ({title_orig})\n"
            f"Описание: {description}"
            f"Рейтинг: {rating}\n"
            f"Год производства: {year}\n"
            f"Жанр: {genre_str}\n"
            f"Возрастной рейтинг: {age_rating}\n"
            f"Постер к фильму: {poster}\n")

    return text


def sort_movie_by_rating(genre: str, count: int) -> str:
    """Функция поиска фильмов по рейтингу в рамках заданного жанра"""

    params = {
        'genres.name': genre,
        'limit': count,
        'rating.imdb': '5-10',
        'sortField': 'rating.imdb',
        'sortType': '-1'
    }

    response = requests.get(
        'https://api.kinopoisk.dev/v1.4/movie?rating.imdb=8-10',
        headers=headers,
        params=params
    )

    result = response.json()['docs']
    res_list = []
    for index, movie in enumerate(result):
        movie_number = str(index + 1)
        movie_title = result[index]['name']
        movie_alt_title = result[index]['alternativeName']
        movie_rating_imdb = result[index]['rating']['imdb']
        movie_data = f'{movie_number}. {movie_title} ({movie_alt_title}), {movie_rating_imdb}'
        res_list.append(movie_data)

    res_text = '\n'.join(res_list)
    return res_text


def sort_low_budget_movie(genre: str, count: int) -> str:
    """Функция поиска фильмов с высоким бюджетом в рамках заданного жанра"""
    pass


def sort_high_budget_movie(genre: str, count: int) -> str:
    """Функция поиска фильмов с низким бюджетом в рамках заданного жанра"""
    pass


def get_history():
    pass


# Тестировочные функции

def test_movie_search():
    """Функция для проверки работы поиска фильма по названию"""

    user_movie_title = input("Введите название фильма: ")
    user_movie_data = get_movie_by_title(user_movie_title)
    text_to_user = format_movie_data(user_movie_data)
    print(user_movie_data)
    print(text_to_user)


def search_list():
    """Функция для проверки работы с выборками"""
    user_genre = input('Введите жанр: ')
    user_count = int(input('Количество фильмов в выборке: '))
    text_to_user = sort_movie_by_rating(user_genre, user_count)
    print(text_to_user)




# test_movie_search()
search_list()
