from src.schemas import PerevalReplaceSchema, PerevalSchema

ADD_PEREVAL_WITHOUT_IMAGES = PerevalSchema(
    **{
        'beauty_title': 'пер. ',
        'title': 'Пхия',
        'other_titles': 'Триев',
        'connect': '',
        'add_time': '2021-09-22 13:18:13',
        'user': {
            'email': 'qwerty@mail.ru',
            'fam': 'Пупкин',
            'name': 'Василий',
            'otc': 'Иванович',
            'phone': '+7 555 55 55',
        },
        'coords': {
            'latitude': '45.3842',
            'longitude': '7.1525',
            'height': '1200',
        },
        'level': {
            'winter': '',
            'summer': '1А',
            'autumn': '1А',
            'spring': '',
        },
    },
)

ADD_PEREVAL_WITH_IMAGES = PerevalSchema(
    **{
        'beauty_title': 'пер. ',
        'title': 'Простой пункт',
        'other_titles': 'Тест',
        'connect': '',
        'add_time': '2025-03-20 15:15:15',
        'user': {
            'email': 'qwerty1@mail.ru',
            'fam': 'Иванова',
            'name': 'Ирина',
        },
        'coords': {
            'latitude': '32.1829',
            'longitude': '5.15',
            'height': '900',
        },
        'level': {
            'winter': '2B',
            'summer': '',
            'autumn': '1А',
            'spring': '',
        },
        'images': [
            {'data': b'iVBORw0KGgoANGsrtG95HwlW1akBUYXUggg==', 'title': 'Седловина'},
            {'data': b'iVBORw0KGgoAAAANSUhEUgAAAKwAArkJggg==', 'title': 'Подъём'},
        ],
    },
)

ADD_PEREVAL_OTHER_USER = PerevalSchema(
    **{
        'beauty_title': 'пер. ',
        'title': 'Пхия',
        'other_titles': 'Триев',
        'connect': '',
        'add_time': '2021-09-22 13:18:13',
        'user': {
            'email': 'qwerty@mail.ru',
            'fam': 'Пупкин',
            'name': 'Василий',
            'otc': 'Иванович',
            'phone': '+7 555 55 55',
        },
        'coords': {
            'latitude': '45.3842',
            'longitude': '7.1525',
            'height': '1200',
        },
        'level': {
            'winter': '',
            'summer': '1А',
            'autumn': '1А',
            'spring': '',
        },
    },
)

UPDATE_PEREVAL_WITHOUT_IMAGES = PerevalReplaceSchema(
    **{
        'beauty_title': 'пер. ',
        'title': 'Пхия1',
        'other_titles': 'Триев',
        'connect': '',
        'add_time': '2021-09-22 13:18:13',
        'coords': {
            'latitude': '45.3842',
            'longitude': '7.1525',
            'height': '1200',
        },
        'level': {
            'winter': '',
            'summer': '1А',
            'autumn': '1А',
            'spring': '',
        },
    },
)

UPDATE_PEREVAL_WITH_IMAGES = PerevalReplaceSchema(
    **{
        'beauty_title': 'пер. ',
        'title': 'Алтай',
        'other_titles': 'Алтай Алтай',
        'connect': '',
        'add_time': '2025-03-25 15:05:55',
        'coords': {
            'latitude': '98.3546',
            'longitude': '14.1',
            'height': '3000',
        },
        'level': {
            'winter': '1А',
            'summer': '',
            'autumn': '',
            'spring': '1А',
        },
        'images': [
            {'data': b'G95HwlW1akBORw0KGgoANGUYXUiVBsrtgg==', 'title': 'Саяны'},
            {'data': b'iVBORw0KGgoAAAANSUhEDFFERFRUgAAAKwAArkJggg==', 'title': 'Высокий Алай'},
        ],
    },
)
