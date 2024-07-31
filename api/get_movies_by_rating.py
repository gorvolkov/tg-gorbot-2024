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
        'https://api.kinopoisk.dev/v1.4/movie',
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
        if movie_title is None:
            movie_data = f'{movie_number}. {movie_alt_title} (не выходил на русском языке), {movie_rating_imdb}'
        elif movie_alt_title is None:
            movie_data = f'{movie_number}. {movie_title}, {movie_rating_imdb}'
        else:
            movie_data = f'{movie_number}. {movie_title} ({movie_alt_title}), {movie_rating_imdb}'
        res_list.append(movie_data)

    res_text = '\n'.join(res_list)
    return res_text


def test() -> None:
    """Тестировочная функция"""

    user_genre = input('Введите жанр: ')
    user_count = int(input('Количество фильмов в выборке: '))
    text_to_user = get_movies_by_rating(user_genre, user_count)
    print(text_to_user)


test()