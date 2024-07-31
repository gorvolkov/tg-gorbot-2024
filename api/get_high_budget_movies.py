import requests
import json
from typing import List, Dict
from config_data.config import API_KEY, API_BASE_URL

headers = {"X-API-KEY": API_KEY}


def get_high_budget_movies(genre: str, count: int) -> str:
    """Функция поиска фильмов с низким бюджетом в рамках заданного жанра"""
    pass
