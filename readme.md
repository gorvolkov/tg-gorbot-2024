# Телеграм-бот, реализующий возможность поиска фильмов или сериалов. 

Реализованы следующие сценарии поиска:
- поиск по названию фильма
- поиск по рейтингу
- поиск фильмов с низким и высоким бюджетом
- возможность просмотра истории поиска за конкретную дату

При запуске бота с помощью команды /start открывается главное меню, в котором пользователь может выбрать 6 вариантов:

![](https://github.com/gorvolkov/tg-gorbot-2024/blob/main/screenshots/1%20main_menu.jpg)

## **1. Поиск по названию фильма**

При запуске поиска по названию бот запрашивает у пользователя:
- название фильма или сериала
- количество результатов в выборке (реализовано, т.к. с одним и тем же названием может быть несколько фильмов)

![](https://github.com/gorvolkov/tg-gorbot-2024/blob/main/screenshots/2%20search_by_name.jpg)

Далее пользователь получает выборку страниц, на которых отображены название фильма, оригинальное название (при наличии), описание, рейтинг фильма в базе Кинопоиска, возрастные ограничения и постер (в виде URL).
В случае отсутствия какого-то из параметров он отмечается как не указанный или отсутствующий.
Пользователь может осуществлять навигацию по выборке при помощи пагинации. 
Под кнопками перемещения по выборке находятся кнопки, позволяющие вернуться продолжить поиск по прежнему сценарию (например, запустить новый поиск по названию), завершить работу с ботом или вернуться в главное меню.

![](https://github.com/gorvolkov/tg-gorbot-2024/blob/main/screenshots/3%20search_by_name_result.jpg)

## **2. Поиск по рейтингу**

При запуске поиска по рейтингу бот запрашивает у пользователя:
- жанр (при запросе жанра производится проверка наличия жанра в базе Кинопоиска; если жанр указан некорректно, бот просит повторить ввод жанра)
- рейтинг (число от 1 до 10)
- количество результатов в выборке

![](https://github.com/gorvolkov/tg-gorbot-2024/blob/main/screenshots/4%20search_by_rating_start.jpg)

Вывод аналогичен выводу, реализованному в сценарии поиска по названию.

## **3, 4 поиск фильмов/сериалов с высоким или низким бюджетом**

При поиске по бюджету у пользователя запрашиваются:
- жанр
- количество результатов в выборке

![](https://github.com/gorvolkov/tg-gorbot-2024/blob/main/screenshots/5%20search_by_budget_start.jpg)

## **5. Поиск по истории**

Бот позволяет вывести историю поиска за конкретную дату. 
Для выбора даты используется интерактивное меню выбора даты:

![](https://github.com/gorvolkov/tg-gorbot-2024/blob/main/screenshots/6%20history_year.jpg)

![](https://github.com/gorvolkov/tg-gorbot-2024/blob/main/screenshots/7%20history_month.jpg)

![](https://github.com/gorvolkov/tg-gorbot-2024/blob/main/screenshots/8%20history_day.jpg)

Выборка истории поиска даётся в обратном порядке (т.е. первым отображается фильм, который был найден последним).

При разработке бота использовано API Кинопоиска: https://api.kinopoisk.dev
