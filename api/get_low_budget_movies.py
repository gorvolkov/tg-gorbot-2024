import requests
import json
from typing import List, Dict
from config_data.config import API_KEY, API_BASE_URL

headers = {"X-API-KEY": API_KEY}


def get_low_budget_movies(genre: str, count: int) -> str:
    """Функция поиска фильмов с высоким бюджетом в рамках заданного жанра"""
    pass