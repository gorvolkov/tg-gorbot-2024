import requests
import json
from typing import List, Dict
from config_data.config import API_KEY, API_BASE_URL

headers = {"X-API-KEY": API_KEY}


def get_movies_by_rating(genre: str, count: int) -> str:
    """Функция поиска фильмов по рейтингу в рамках заданного жанра"""

    params = {
        'genres.name': genre,
        'limit': count,
        'rating.kp': '5-10',
        'sortField': 'rating.kp',
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




def search_list():
    """Тестировочная функция"""
    user_genre = input('Введите жанр: ')
    user_count = int(input('Количество фильмов в выборке: '))
    text_to_user = sort_movie_by_rating(user_genre, user_count)
    print(text_to_user)