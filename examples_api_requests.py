import requests

from src.core.config import app_settings

class PerevalAPI:
    BASE_URL = f'http://{app_settings.app_host}:{app_settings.app_port}/submitData'

    def add_pereval(self, data_pereval: dict) -> dict:
        return requests.post(url=self.BASE_URL, json=data_pereval).json()

    def get_pereval_by_id(self, pereval_id: int) -> dict:
        return requests.get(url=f'{self.BASE_URL}/{pereval_id}').json()

    def edit_pereval_by_id(self, pereval_id: int, data_to_update: dict):
        return requests.patch(url=f'{self.BASE_URL}/{pereval_id}', json=data_to_update).json()

    def get_perevals_by_email_user(self, email_user: str) -> list:
        return requests.get(url=f'{self.BASE_URL}', params={'user__email': email_user}).json()


pereval_api = PerevalAPI()
data = {
    'beauty_title': 'пер. ',
    'title': 'Пхия',
    'other_titles': 'Триев',
    'connect': '',
    'add_time': '2021-09-22 13:18:13',
    'coords': {'latitude': 45.3842, 'longitude': 7.1525, 'height': 1200},
    'level': {'winter': '', 'summer': '1А', 'autumn': '1А', 'spring': ''},
    'images': [
        {'data': 'iVBORw0KGgoANGsrtG95HwlW1akBUYXUggg==', 'title': 'Пхия'},
    ],
    'user': {'email': 'user@email.tld', 'fam': 'Пупкин', 'name': 'Василий', 'otc': 'Иванович', 'phone': '79031234567'},
}

# Добавить перевал
pereval = pereval_api.add_pereval(data)

# Получить перевал по id
info_pereval = pereval_api.get_pereval_by_id(10)

data_to_update = {
    'beauty_title': 'пер. ',
    'title': 'Пхия1',
    'other_titles': 'Триев',
    'connect': '',
    'add_time': '2021-09-22 13:18:13',
    'coords': {'latitude': 45.3842, 'longitude': 7.1525, 'height': 1200},
    'level': {'winter': '', 'summer': '1А', 'autumn': '1А', 'spring': ''},
    'images': [],
}

# Изменить данные перевале
pereval_api.edit_pereval_by_id(10, data_to_update)

# Получить спискок перевалов, добавленных конкретным пользователем
pereval_api.get_perevals_by_email_user(info_pereval['user']['email'])
