from datetime import datetime
from .models import Movie


def write_to_db(movie: Movie, user_id) -> None:
    """Функция, которая принимает объекты Movie и User и добавляет запись нового фильма в базу данных"""

    Movie.create(
        user_id=user_id,
        due_date=datetime.now(),
        title=movie.title,
        title_orig=movie.title_orig,
        description=movie.description,
        rating=movie.rating,
        year=movie.year,
        genres=movie.genres,
        age_rating=movie.age_rating,
        poster=movie.poster)
