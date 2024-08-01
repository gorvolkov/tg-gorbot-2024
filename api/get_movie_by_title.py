import requests
from config_data.config import API_KEY, API_BASE_URL

headers = {"X-API-KEY": API_KEY}


def get_movie_by_title(title: str) -> str:
    """Функция, выполняющая поиск сведений о фильме в каталоге Кинопоиска"""

    params = {
        'query': title,
    }
    response = requests.get(
        'https://api.kinopoisk.dev/v1.4/movie/search',
        headers=headers,
        params=params
    )

    movie_data = response.json()

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



def test_movie_search():
    """Тестировочная функция"""

    user_movie_title = input("Введите название фильма: ")
    user_movie_data = get_movie_by_title(user_movie_title)
    print(user_movie_data)


test_movie_search()