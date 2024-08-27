from datetime import datetime, date
from database.models import Movie, Temp, User, db


def write_movie_to_temp(movie: Movie, user_id: int) -> None:
    """Функция, которая записывает новый фильм в базу данных"""

    Temp.create(
        user_id=user_id,
        due_date=datetime.today(),
        title=movie.title,
        title_orig=movie.title_orig,
        description=movie.description,
        rating=movie.rating,
        year=movie.year,
        genres=movie.genres,
        age_rating=movie.age_rating,
        poster=movie.poster,
    )


def write_selection_to_temp(movie_list: list, user_id: int) -> None:
    """Записывает целую выборку в таблицу Temp"""

    for movie in movie_list:
        write_movie_to_temp(movie=movie, user_id=user_id)


def merge_temp_to_movies() -> None:
    """
    Функция завершения работы с выборкой.
    Добавляет таблицу Temp к таблице Movie и очищает Temp.
    """

    # получаем все записи из temp
    temp_all = Temp.select()

    # Добавляем все записи из таблицы temp в таблицу movie
    with db.atomic():
        for temp_record in temp_all:
            Movie.create(
                user=temp_record.user,
                due_date=temp_record.due_date,
                title=temp_record.title,
                title_orig=temp_record.title_orig,
                description=temp_record.description,
                rating=temp_record.rating,
                year=temp_record.year,
                genres=temp_record.genres,
                age_rating=temp_record.age_rating,
                poster=temp_record.poster,
            )

    # очищаем временную таблицу
    Temp.delete().execute()


def get_history(user_id: int, query_date: date) -> list:
    """
    Производит выборку из общей истории поиска по пользователю и дате.
    Записывает результат во временную таблицу Temp
    """

    result = Movie.filter(user_id=user_id, due_date=query_date).order_by(
        -Movie.movie_id
    )

    return result


def drop_temp() -> None:
    """Функция, очищающая временную таблицу temp при выходе из работы с выборкой истории"""

    Temp.delete().execute()
