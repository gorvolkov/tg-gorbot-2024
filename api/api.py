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
    title = movie_data['docs'][0]['name']
    title_orig = movie_data['docs'][0]['alternativeName']
    year = movie_data['docs'][0]['year']

    genre_list = []
    genres = [{'name': 'фантастика'}, {'name': 'фэнтези'}, {'name': 'боевик'}, {'name': 'приключения'}]
    for genre in genres:
        genre_list.append(genre['name'])
    genre_str = ', '.join(genre_list)

    genres = movie_data['docs'][0]['genres']
    description = movie_data['docs'][0]['description']
    rating = movie_data['docs'][0]['description']
    age_rating = 'null'

    text = (f"Название: {title} ({title_orig})\n"
            f"Описание: {description}"
            f"Рейтинг: {rating}\n"
            f"Год производства: {year}\n"
            f"Жанр: {genre_str}\n"
            f"Возрастной рейтинг: {age_rating}\n"
            f"Постер к фильму:\n")

    return text


user_movie_title = input("Введите название фильма: ")

user_movie_data = get_movie_by_title(user_movie_title)
text_to_user = format_movie_data(user_movie_data)

print(user_movie_data)
print(text_to_user)
