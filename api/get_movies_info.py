import requests
from config_data.config import API_KEY, API_BASE_URL

from database.models import Movie

headers = {"X-API-KEY": API_KEY}


def _format_movie_data(movie_data: dict) -> Movie:
    """Функция, приводящая данные по каждому фильму в нужный формат"""

    new_movie = Movie()

    new_movie.title = movie_data["name"]

    title_orig = ""
    try:
        # блоки с if добавлены в обертку try / except,
        # потому что в некоторых случаях API возвращает None, а в других случаях возникает KeyError (например, при отсутствии постера).
        # Конструкции получились несколько громоздкие, но зато получилось предусмотреть больше случаев неполных ответов
        if movie_data["alternativeName"]:
            title_orig = f"({movie_data["alternativeName"]})"
    except Exception:
        pass
    finally:
        new_movie.title_orig = title_orig

    year = "не найден"
    try:
        if movie_data["year"]:
            year = movie_data["year"]
    except Exception:
        pass
    finally:
        new_movie.year = year

    genres = "жанр не указан"
    try:
        genres_parsed = movie_data["genres"]
        genre_list = []
        for genre in genres_parsed:
            genre_list.append(genre["name"])
        genres = ", ".join(genre_list)
    except Exception:
        pass
    finally:
        new_movie.genres = genres

    description = "отсутствует"
    try:
        if movie_data["description"]:
            description = movie_data["description"]
    except Exception:
        pass
    finally:
        new_movie.description = description

    rating = "не указан"
    try:
        if movie_data["rating"]["kp"]:
            rating = movie_data["rating"]["kp"]
    except Exception:
        pass
    finally:
        new_movie.rating = rating

    age_rating = "не указан"
    try:
        if movie_data["ageRating"]:
            age_rating = f"{movie_data['ageRating']}+"
    except Exception:
        pass
    finally:
        new_movie.age_rating = age_rating

    poster = "не найден"
    try:
        if movie_data["poster"]["previewUrl"]:
            poster = movie_data["poster"]["previewUrl"]
    except Exception:
        pass
    finally:
        new_movie.poster = poster

    return new_movie


def _get_selection(resp_data) -> list:
    """Функция, принимающая данные в виде json-объекта, полученные по запросу к API Кинопоиска.
    Возвращает список данных по найденным фильмам"""

    # получаем список с данными по каждому найденному фильму
    selection = resp_data.json()["docs"]
    movie_list = []

    for index, movie in enumerate(selection):
        new_movie = _format_movie_data(movie_data=movie)
        movie_list.append(new_movie)

    return movie_list


def get_by_name(name: str, count: str) -> list:
    """Функция, реализующая поиск фильмов по названию.
    Принимает название и заданное число фильмов в выборке,
    отдаёт список с текстами по фильмам"""

    params = {"notNullFields": "name", "query": name, "limit": count}
    response = requests.get(f"{API_BASE_URL}/search", headers=headers, params=params)

    result = _get_selection(resp_data=response)
    return result


def get_by_rating(genre: str, count: str, rating: str) -> list:
    """Функция поиска фильмов по рейтингу в рамках заданного жанра"""

    if rating == "10":
        rating_query = "10-10"
    else:
        rating_query = f"{rating}-{rating}.9"

    params = {
        "notNullFields": "name",
        # добавлено, чтобы убрать из выборки фильмы, которые не выходили на русском языке
        # и результат был сопоставим с выборкой, которую дает приложение Кинопоиска
        "genres.name": genre,
        "limit": count,
        "rating.kp": rating_query,
        "sortField": "rating.kp",
        "sortType": "1",
    }

    response = requests.get(f"{API_BASE_URL}", headers=headers, params=params)

    result = _get_selection(resp_data=response)
    return result


def get_by_budget(genre: str, count: str, low=None) -> list:
    """Функция поиска фильмов с высоким или низким бюджетом в рамках заданного жанра"""

    sort_type = "-1"
    if low:
        sort_type = "1"

    params = {
        "notNullFields": "name",
        "genres.name": genre,
        "limit": count,
        "sortField": "budget.value",
        "sortType": sort_type,
    }

    response = requests.get(f"{API_BASE_URL}", headers=headers, params=params)

    result = _get_selection(resp_data=response)
    return result
