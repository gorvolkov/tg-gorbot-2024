parsed_genres_list = [
  {
    "name": "аниме",
    "slug": "anime"
  },
  {
    "name": "биография",
    "slug": "biografiya"
  },
  {
    "name": "боевик",
    "slug": "boevik"
  },
  {
    "name": "вестерн",
    "slug": "vestern"
  },
  {
    "name": "военный",
    "slug": "voennyy"
  },
  {
    "name": "детектив",
    "slug": "detektiv"
  },
  {
    "name": "детский",
    "slug": "detskiy"
  },
  {
    "name": "для взрослых",
    "slug": "dlya-vzroslyh"
  },
  {
    "name": "документальный",
    "slug": "dokumentalnyy"
  },
  {
    "name": "драма",
    "slug": "drama"
  },
  {
    "name": "игра",
    "slug": "igra"
  },
  {
    "name": "история",
    "slug": "istoriya"
  },
  {
    "name": "комедия",
    "slug": "komediya"
  },
  {
    "name": "концерт",
    "slug": "koncert"
  },
  {
    "name": "короткометражка",
    "slug": "korotkometrazhka"
  },
  {
    "name": "криминал",
    "slug": "kriminal"
  },
  {
    "name": "мелодрама",
    "slug": "melodrama"
  },
  {
    "name": "музыка",
    "slug": "muzyka"
  },
  {
    "name": "мультфильм",
    "slug": "multfilm"
  },
  {
    "name": "мюзикл",
    "slug": "myuzikl"
  },
  {
    "name": "новости",
    "slug": "novosti"
  },
  {
    "name": "приключения",
    "slug": "priklyucheniya"
  },
  {
    "name": "реальное ТВ",
    "slug": "realnoe-TV"
  },
  {
    "name": "семейный",
    "slug": "semeynyy"
  },
  {
    "name": "спорт",
    "slug": "sport"
  },
  {
    "name": "ток-шоу",
    "slug": "tok-shou"
  },
  {
    "name": "триллер",
    "slug": "triller"
  },
  {
    "name": "ужасы",
    "slug": "uzhasy"
  },
  {
    "name": "фантастика",
    "slug": "fantastika"
  },
  {
    "name": "фильм-нуар",
    "slug": "film-nuar"
  },
  {
    "name": "фэнтези",
    "slug": "fentezi"
  },
  {
    "name": "церемония",
    "slug": "ceremoniya"
  }
]

genres_set = set()
for genre in parsed_genres_list:
    genre_rus, genre_en = genre["name"], genre["slug"]
    genres_set.add(genre_rus)

print(genres_set)