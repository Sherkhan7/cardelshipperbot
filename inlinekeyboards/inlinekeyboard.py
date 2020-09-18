from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from DB import *
import datetime
from languages import LANGS


class InlineKeyboard(object):
    def __init__(self, keyboard_type, lang=None, region_id=None, begin=None, end=None, data=None):

        self.__type = keyboard_type
        self.__lang = lang
        self.__region_id = region_id
        self.__begin = begin
        self.__end = end
        self.__data = data

        self.__keyboard = self.__create_inline_keyboard(self.__type, self.__lang, self.__region_id,
                                                        self.__begin, self.__end, self.__data)

    def __create_inline_keyboard(self, keyb_type, lang, region_id, begin, end, data):

        if keyb_type == 'langs_keyboard':
            return InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("\U0001F1FA\U0001F1FF UZB",
                                             callback_data='uz'),
                    ],
                    [
                        InlineKeyboardButton("\U0001F1F7\U0001F1FA RUS",
                                             callback_data='ru'),
                    ]
                ]
            )

        elif keyb_type == 'user_data_keyboard':
            return self.__get_user_data_keyboard(lang)

        elif keyb_type == 'regions_keyboard':

            return self.__get_regions_keyboard(lang, select_all_regions())

        elif keyb_type == 'districts_keyboard':

            return self.__get_districts_keyboard(lang, select_all_districts(region_id))

        elif keyb_type == 'dates_keyboard':

            return self.__get_dates_keyboard(lang)

        elif keyb_type == 'hours_keyboard':

            return self.__get_hours_keyboard(lang, begin, end)

        elif keyb_type == 'minutes_keyboard':

            return self.__get_minutes_keyboard(lang, data)
        elif keyb_type == 'confirm_keyboard':

            return self.__get_confirm_keyboard(lang, data)

    @staticmethod
    def __get_user_data_keyboard(lang):
        if lang == LANGS[0]:
            button1_text = "Ismni o'zgartirish"
            button2_text = "Familyani o'zgartirish"
            button3_text = "Telefon nomerini o'zgartirish"

        if lang == LANGS[1]:
            button1_text = "Изменить имя"
            button2_text = "Изменить фамилию"
            button3_text = "Изменить номер телефона"

        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f'\U0001F464 {button1_text}', callback_data='change_name_btn'),
                ],

                [
                    InlineKeyboardButton(f'\U0001F465 {button2_text}', callback_data='change_surname_btn'),
                ],

                [
                    InlineKeyboardButton(f'\U0001F4F1 {button3_text}', callback_data='change_phone_btn'),
                ],
            ]
        )

    @staticmethod
    def __get_regions_keyboard(lang, regions):
        length = len(regions)

        if lang == LANGS[0]:
            region_name = 'nameUz'
            odd_btn_text = '« Orqaga'

        if lang == LANGS[1]:
            region_name = 'nameRu'
            odd_btn_text = '« Назад'

        if length % 2 == 0:
            keyboard = [
                [
                    InlineKeyboardButton(regions[i][region_name], callback_data=f"region_id_{regions[i]['id']}"),

                    InlineKeyboardButton(regions[i + 1][region_name], callback_data=f"region_id_{regions[i + 1]['id']}")
                ]

                for i in range(0, length, 2)
            ]

        if length % 2 != 0:
            keyboard = [
                [
                    InlineKeyboardButton(regions[i][region_name], callback_data=f"region_id_{regions[i]['id']}"),
                    InlineKeyboardButton(odd_btn_text, callback_data='back_btn')
                ]
                if i == length - 1 else
                [
                    InlineKeyboardButton(regions[i][region_name], callback_data=f"region_id_{regions[i]['id']}"),
                    InlineKeyboardButton(regions[i + 1][region_name], callback_data=f"region_id_{regions[i + 1]['id']}")
                ] for i in range(0, length, 2)
            ]

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def __get_districts_keyboard(lang, districts):
        length = len(districts)

        if lang == LANGS[0]:
            district_name = 'nameUz'
            odd_btn_text = '« Orqaga'

        if lang == LANGS[1]:
            district_name = 'nameRu'
            odd_btn_text = '« Назад'

        if length % 2 == 0:
            keyboard = [
                [
                    InlineKeyboardButton(districts[i][district_name],
                                         callback_data=f"district_id_{districts[i]['id']}"),

                    InlineKeyboardButton(districts[i + 1][district_name],
                                         callback_data=f"district_id_{districts[i + 1]['id']}")
                ]

                for i in range(0, length, 2)
            ]
            keyboard.append([InlineKeyboardButton(odd_btn_text, callback_data="back_btn")])

        if length % 2 != 0:
            keyboard = [
                [
                    InlineKeyboardButton(districts[i][district_name],
                                         callback_data=f"district_id_{districts[i]['id']}"),
                    InlineKeyboardButton(odd_btn_text, callback_data='back_btn')
                ]
                if i == length - 1 else
                [
                    InlineKeyboardButton(districts[i][district_name],
                                         callback_data=f"district_id_{districts[i]['id']}"),
                    InlineKeyboardButton(districts[i + 1][district_name],
                                         callback_data=f"district_id_{districts[i + 1]['id']}")
                ] for i in range(0, length, 2)
            ]

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def __get_dates_keyboard(lang):

        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        after_tomorrow = tomorrow + datetime.timedelta(days=1)

        if lang == LANGS[0]:
            button1_text = 'Hozir'
            button2_text = 'Bugun'

        if lang == LANGS[1]:
            button1_text = 'Сейчас'
            button2_text = 'Cегодня'

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='now'),
                InlineKeyboardButton(button2_text, callback_data='today')
            ],
            [
                InlineKeyboardButton(f'{tomorrow.strftime("%d-%m-%Y")}', callback_data='tomorrow'),
                InlineKeyboardButton(f'{after_tomorrow.strftime("%d-%m-%Y")}', callback_data='after_tomorrow')
            ]
        ])

    @staticmethod
    def __get_hours_keyboard(lang, begin, end):
        inline_keyboard = []

        if begin == 6 and end == 17:

            button_data = 'next'

            if lang == LANGS[0]:
                button_text = 'Keyingisi'

            if lang == LANGS[1]:
                button_text = 'Следующий'

            inline_keyboard = [
                [
                    InlineKeyboardButton(f'{i}:00', callback_data=f'{i}'),
                    InlineKeyboardButton(f'{i + 1}:00', callback_data=f'{i + 1}'),
                    InlineKeyboardButton(f'{i + 2}:00', callback_data=f'{i + 2}'),
                ] for i in range(begin, end + 1, 3)
            ]

        elif begin == 18 and end == 29:

            button_data = 'back'

            if lang == LANGS[0]:
                button_text = 'Orqaga'

            if lang == LANGS[1]:
                button_text = 'Назад'

            for i in range(begin, end + 1, 3):

                if i == 24:
                    i = 0
                if i == 27:
                    i = 3

                inline_keyboard.append([
                    InlineKeyboardButton(f'{i}:00', callback_data=f'{i}'),
                    InlineKeyboardButton(f'{i + 1}:00', callback_data=f'{i + 1}'),
                    InlineKeyboardButton(f'{i + 2}:00', callback_data=f'{i + 2}'),

                ])

        inline_keyboard.append([InlineKeyboardButton(button_text, callback_data=button_data)])

        return InlineKeyboardMarkup(inline_keyboard)

    @staticmethod
    def __get_minutes_keyboard(lang, data):

        if lang == LANGS[0]:
            button_text = 'Orqaga'

        if lang == LANGS[1]:
            button_text = 'Назад'

        inline_keyboard = [
            [
                InlineKeyboardButton(f'{data}:{i}', callback_data=f'{data}:{i}'),
                InlineKeyboardButton(f'{data}:{i + 10}', callback_data=f'{data}:{i + 10}'),
                InlineKeyboardButton(f'{data}:{i + 20}', callback_data=f'{data}:{i + 20}')
            ] for i in range(0, 60, 30)
        ]

        inline_keyboard.append(
            [InlineKeyboardButton(button_text, callback_data='back')]
        )

        return InlineKeyboardMarkup(inline_keyboard)

    @staticmethod
    def __get_confirm_keyboard(lang, data):

        from_latitude = data['from_location']['latitude']
        from_longitude = data['from_location']['longitude']
        to_latitude = data['to_location']['latitude']
        to_longitude = data['to_location']['longitude']

        inline_keyboard = []

        if from_latitude and from_longitude:
            inline_keyboard.append(
                [InlineKeyboardButton('A',
                                      url=f'http://www.google.com/maps/place/{from_latitude},{from_longitude}/'
                                          f'@{from_latitude},{from_longitude},12z')])

        if to_latitude and to_longitude:
            inline_keyboard.append(
                [InlineKeyboardButton('B',
                                      url=f'http://www.google.com/maps/place/{to_latitude},{to_longitude}/'
                                          f'@{to_latitude},{to_longitude},12z')])

        if from_latitude and from_longitude and to_latitude and to_longitude:
            direction = f'https://www.google.com/maps/dir/{from_latitude},{from_longitude}/{to_latitude},{to_longitude}'
            inline_keyboard.append([InlineKeyboardButton('A->B', url=direction)])

        if lang == LANGS[0]:
            button_text = 'Tasdiqlash'

        if lang == LANGS[1]:
            button_text = 'Подтвердить'

        inline_keyboard.append([InlineKeyboardButton(button_text, callback_data='confirm')])

        inline_keyboard = InlineKeyboardMarkup(inline_keyboard)

        return inline_keyboard

    def get_keyboard(self):

        return self.__keyboard

# z = InlineKeyboard('dates_keyboard', 'ru')
# x = InlineKeyboard('hours_keyboard', 'uz', begin=18, end=29)
# y = InlineKeyboard('minutes_keyboard', 'ru', data=13)
# print(y.get_keyboard())
