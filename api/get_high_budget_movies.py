import requests
from config_data.config import API_KEY

headers = {"X-API-KEY": API_KEY}


def get_low_budget_movies(genre: str, count: int) -> str:
    """Функция поиска фильмов с высоким бюджетом в рамках заданного жанра"""

    params = {
        'notNullFields': 'name',
        'genres.name': genre,
        'limit': count,
        'sortField': 'budget.value',
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
        movie_data = f'{movie_number}. {movie_title}'
        res_list.append(movie_data)

    res_text = '\n'.join(res_list)
    return res_text


# def test() -> None:
#     """Тестировочная функция"""
#
#     user_genre = input('Введите жанр: ')
#     user_count = int(input('Количество фильмов в выборке: '))
#     text_to_user = get_low_budget_movies(user_genre, user_count)
#     print(text_to_user)
#
#
# test()
