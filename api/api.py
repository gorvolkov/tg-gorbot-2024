import requests
import json
from typing import List, Dict
from config_data.config import API_KEY, API_BASE_URL

headers = {"X-API-KEY": API_KEY}


# образец

def api_request(endpoint: str, params={}) -> requests.Response:
    params['key'] = API_KEY
    return requests.get(
        f'{API_BASE_URL}/{endpoint}',
        params=params
    )
    return


def get_langs() -> List[str]:
    response = api_request('getLangs');
    return response.json()


def lookup(lang: str, text: str, ui: str = 'ru') -> Dict:
    response = api_request('lookup', params={
        'lang': lang,
        'text': text,
        'ui': ui
    })

    return response.json().get('def', {})













def get_history():
    pass


