from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

from config_data.config import DB_PATH

db = SqliteDatabase(DB_PATH)


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
    user = ForeignKeyField(User, backref="movies")
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
        return ("Название: {title} ({title_orig})\n"
                "Описание: {description}\n"
                "Рейтинг Кинопоиска: {rating}\n"
                "Год производства: {year}\n"
                "Жанр: {genres}\n"
                "Возрастной рейтинг: {age_rating}\n"
                "Постер к фильму: {poster}").format(title=self.title,
                                                    title_orig=self.title_orig,
                                                    description=self.description,
                                                    rating=self.rating,
                                                    year=self.year,
                                                    genres=self.genres,
                                                    age_rating=self.age_rating,
                                                    poster=self.poster)


def create_models():
    db.create_tables(BaseModel.__subclasses__())
