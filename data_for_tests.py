from src.schemas import PerevalAddSchema, PerevalReplaceSchema, UserSchema

ADD_PEREVAL_WITHOUT_IMAGES = PerevalAddSchema(
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

ADD_PEREVAL_WITH_IMAGES = PerevalAddSchema(
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

ADD_PEREVAL_OTHER_USER = PerevalAddSchema(
    **{
        'beauty_title': 'пер. ',
        'title': 'Хребет Цаган-Шибэту',
        'other_titles': 'Триев',
        'connect': '',
        'add_time': '2021-09-22 13:18:13',
        'user': {
            'email': 'other_user@mail.ru',
            'fam': 'Пупкин',
            'name': 'Василий',
            'otc': 'Иванович',
            'phone': '+7 245 75 52',
        },
        'coords': {
            'latitude': '50.20',
            'longitude': '91.00',
            'height': '3577',
        },
        'level': {
            'winter': '',
            'summer': '1А',
            'autumn': '1А',
            'spring': '',
        },
    },
)

ADD_PEREVAL_CAT_USER = PerevalAddSchema(
    **{
        'beauty_title': 'пер. ',
        'title': 'Горный узел Такали',
        'other_titles': 'test',
        'connect': '',
        'add_time': '2023-12-03 03:54:09',
        'user': {
            'email': 'cat_user@mail.ru',
            'fam': 'Котеевич',
            'name': 'Кот',
        },
        'coords': {
            'latitude': '0.123',
            'longitude': '19.25',
            'height': '790',
        },
        'level': {
            'winter': '2B',
            'summer': '',
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

USER_CAT = UserSchema(
    email='cat_user@mail.ru',
    fam='Test',
    name='Test',
)

OTHER_USER = UserSchema(
    email='other_user@mail.ru',
    fam='Test',
    name='Test',
)
