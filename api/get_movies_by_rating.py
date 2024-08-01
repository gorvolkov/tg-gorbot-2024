import requests
from config_data.config import API_KEY, API_BASE_URL

headers = {"X-API-KEY": API_KEY}


def get_movies_by_rating(genre: str, count: int) -> str:
    """Функция поиска фильмов по рейтингу в рамках заданного жанра"""

    params = {
        'notNullFields': 'name',
        # добавлено, чтобы отфильтровать фильмы, которые не выходили на русском языке
        # и выборка была более релевантной выборке приложения Кинопоиска

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
        movie_rating_kp = result[index]['rating']['kp']
        movie_data = f'{movie_number}. {movie_title}, {movie_rating_kp}'
        res_list.append(movie_data)

    res_text = '\n'.join(res_list)
    return res_text


# def test() -> None:
#     """Тестировочная функция"""
#
#     user_genre = input('Введите жанр: ')
#     user_count = int(input('Количество фильмов в выборке: '))
#     text_to_user = get_movies_by_rating(user_genre, user_count)
#     print(text_to_user)
#
#
# test()