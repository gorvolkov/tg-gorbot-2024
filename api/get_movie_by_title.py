import requests
from config_data.config import API_KEY, API_BASE_URL
from database import Movie

headers = {"X-API-KEY": API_KEY}


def get_movie_by_title(title: str) -> Movie:
    """Функция, выполняющая поиск сведений о фильме в каталоге Кинопоиска"""
    # иногда возвращает фильмы, не строго соответствующие названию (ищет все возможные совпадения по подстрокам из запроса). Но работает
    params = {
        'query': title,
    }
    response = requests.get(
        'https://api.kinopoisk.dev/v1.4/movie/search',
        headers=headers,
        params=params
    )

    movie_data = response.json()
    new_movie = Movie()

    # проработать, как это сделать через json.dumps
    new_movie.title = movie_data['docs'][0]['name']
    new_movie.title_orig = movie_data['docs'][0]['alternativeName']
    new_movie.year = movie_data['docs'][0]['year']

    genre_list = []
    genres_parsed = movie_data['docs'][0]['genres']
    for genre in genres_parsed:
        genre_list.append(genre['name'])
    genre_str = ', '.join(genre_list)

    new_movie.genres = genre_str
    new_movie.description = movie_data['docs'][0]['description']
    new_movie.rating = movie_data['docs'][0]['rating']['kp']
    new_movie.age_rating = f'{movie_data['docs'][0]['ageRating']}+'
    new_movie.poster = movie_data['docs'][0]['poster']['previewUrl']
    # необходимо решить с добавлением постера к выдаче, пока добавляется просто ссылка на картинку
    # надо спарсить картинку и встроить ее в тело ответа

    return new_movie
