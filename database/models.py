import peewee
from peewee import (
    AutoField,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    Model,
)

from config_data.config import DB_PATH

db = peewee.SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    DoesNotExist = None
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)


class Movie(BaseModel):
    movie_id = AutoField()
    user = ForeignKeyField(User)
    due_date = DateField()
    title = CharField()
    title_orig = CharField()
    description = CharField()
    rating = CharField()
    year = CharField()
    genres = CharField()
    age_rating = CharField()
    poster = CharField()

    def __str__(self):
        return (
            f"<b>Название:</b> {self.title} {self.title_orig}\n\n"
            f"<b>Описание:</b> {self.description}\n\n"
            f"<b>Рейтинг Кинопоиска:</b> {self.rating}\n\n"
            f"<b>Год производства:</b> {self.year}\n\n"
            f"<b>Жанр:</b> {self.genres}\n\n"
            f"<b>Возрастной рейтинг:</b> {self.age_rating}\n\n"
            f"<b>Постер к фильму:</b> {self.poster}"
        )


class Temp(BaseModel):
    movie_id = AutoField()
    user = ForeignKeyField(User)
    due_date = DateField()
    title = CharField()
    title_orig = CharField()
    description = CharField()
    rating = CharField()
    year = CharField()
    genres = CharField()
    age_rating = CharField()
    poster = CharField()

    def __str__(self):
        return (
            f"<b>Название:</b> {self.title} {self.title_orig}\n\n"
            f"<b>Описание:</b> {self.description}\n\n"
            f"<b>Рейтинг Кинопоиска:</b> {self.rating}\n\n"
            f"<b>Год производства:</b> {self.year}\n\n"
            f"<b>Жанр:</b> {self.genres}\n\n"
            f"<b>Возрастной рейтинг:</b> {self.age_rating}\n\n"
            f"<b>Постер к фильму:</b> {self.poster}"
        )


def create_models():
    db.create_tables(BaseModel.__subclasses__())
