from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from DB import *
import datetime


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
                    [InlineKeyboardButton("\U0001F1FA\U0001F1FF O'zbekcha",
                                          callback_data=self.__btn_data('uz_btn')), ],

                    [InlineKeyboardButton("\U0001F1F7\U0001F1FA Русский",
                                          callback_data=self.__btn_data('ru_btn')), ],

                ]
            )

        elif keyb_type == 'main_keyboard':

            return self.__get_main_keyboard(lang)

        elif keyb_type == 'user_data_keyboard':
            return self.__get_user_data_keyboard(lang)

        elif keyb_type == 'regions_keyboard':

            return self.__get_regions_keyboard(select_all_regions(), lang)

        elif keyb_type == 'districts_keyboard':

            return self.__get_districts_keyboard(select_all_districts(region_id), lang)

        elif keyb_type == 'dates_keyboard':

            return self.__get_dates_keyboard(lang)

        elif keyb_type == 'hours_keyboard':

            return self.__get_hours_keyboard(begin, end, lang)

        elif keyb_type == 'minutes_keyboard':

            return self.__get_minutes_keyboard(data, lang)

    def __get_main_keyboard(self, lang):

        if lang == 'uz':
            button1_text = "Mening ma'lmotlarim"
            button2_text = "Yuk e'lon qilish"

        if lang == 'ru':
            button1_text = 'Мои данные'
            button2_text = 'Объявить груз'

        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('\U0001F4D4 ' + button1_text, callback_data=self.__btn_data('user_data_btn')), ],

                [InlineKeyboardButton('\U0001F4E6 ' + button2_text,
                                      callback_data=self.__btn_data('new_cargo_btn')), ],

            ]
        )

    def __get_user_data_keyboard(self, lang):
        if lang == 'uz':
            button1_text = "Ismni o'zgartirish"
            button2_text = "Familyani o'zgartirish"
            button3_text = "Tilni o'zgartirish"
            button4_text = "Orqaga"

        if lang == 'ru':
            button1_text = "Изменить имя"
            button2_text = "Изменить фамилию"
            button3_text = "Изменить язык"
            button4_text = "Назад"

        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(button1_text, callback_data=self.__btn_data('change_name_btn')), ],

                [InlineKeyboardButton(button2_text, callback_data=self.__btn_data('change_surname_btn')), ],

                [InlineKeyboardButton(button3_text, callback_data=self.__btn_data('change_lang_btn')), ],

                [InlineKeyboardButton(button4_text, callback_data=self.__btn_data('back_btn')), ],
            ]
        )

    def __get_regions_keyboard(self, regions, lang):
        length = len(regions)
        if lang == 'uz':
            region_name = 'nameUz'
            odd_btn_text = 'Orqaga'
        else:
            region_name = 'nameRu'
            odd_btn_text = 'Назад'

        if length % 2 == 0:
            keyboard = [
                [
                    InlineKeyboardButton(regions[i][region_name],
                                         callback_data=self.__btn_data(f"region_id_{regions[i]['id']}")),

                    InlineKeyboardButton(regions[i + 1][region_name],
                                         callback_data=self.__btn_data(f"region_id_{regions[i + 1]['id']}"))
                ]

                for i in range(0, length, 2)
            ]

        if length % 2 != 0:
            keyboard = [
                [
                    InlineKeyboardButton(regions[i][region_name],
                                         callback_data=self.__btn_data(f"region_id_{regions[i]['id']}")),
                    InlineKeyboardButton(odd_btn_text, callback_data='back_btn')
                ]
                if i == length - 1 else
                [
                    InlineKeyboardButton(regions[i][region_name],
                                         callback_data=self.__btn_data(f"region_id_{regions[i]['id']}")),
                    InlineKeyboardButton(regions[i + 1][region_name],
                                         callback_data=self.__btn_data(f"region_id_{regions[i + 1]['id']}"))
                ] for i in range(0, length, 2)
            ]

        return InlineKeyboardMarkup(keyboard)

    def __get_districts_keyboard(self, districts, lang):
        length = len(districts)
        if lang == 'uz':
            district_name = 'nameUz'
            odd_btn_text = 'Orqaga'
        else:
            district_name = 'nameRu'
            odd_btn_text = 'Назад'

        if length % 2 == 0:
            keyboard = [
                [
                    InlineKeyboardButton(districts[i][district_name],
                                         callback_data=self.__btn_data(f"district_id_{districts[i]['id']}")),

                    InlineKeyboardButton(districts[i + 1][district_name],
                                         callback_data=self.__btn_data(f"district_id_{districts[i + 1]['id']}"))
                ]

                for i in range(0, length, 2)
            ]
            keyboard.append([InlineKeyboardButton(odd_btn_text, callback_data=self.__btn_data("back_btn"))])
        if length % 2 != 0:
            keyboard = [
                [
                    InlineKeyboardButton(districts[i][district_name],
                                         callback_data=self.__btn_data(f"district_id_{districts[i]['id']}")),
                    InlineKeyboardButton(odd_btn_text, callback_data='back_btn')
                ]
                if i == length - 1 else
                [
                    InlineKeyboardButton(districts[i][district_name],
                                         callback_data=self.__btn_data(f"district_id_{districts[i]['id']}")),
                    InlineKeyboardButton(districts[i + 1][district_name],
                                         callback_data=self.__btn_data(f"district_id_{districts[i + 1]['id']}"))
                ] for i in range(0, length, 2)
            ]

        return InlineKeyboardMarkup(keyboard)

    def __get_dates_keyboard(self, lang):

        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        after_tomorrow = tomorrow + datetime.timedelta(days=1)

        if lang == 'uz':
            button1_text = 'Hozir'
            button2_text = 'Bugun'

        if lang == 'ru':
            button1_text = 'Сейчас'
            button2_text = 'Cегодня'

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data=self.__btn_data('now')),
                InlineKeyboardButton(button2_text, callback_data='today')
            ],
            [
                InlineKeyboardButton(f'{tomorrow.strftime("%d-%m-%Y")}', callback_data=self.__btn_data('tomorrow')),
                InlineKeyboardButton(f'{after_tomorrow.strftime("%d-%m-%Y")}',
                                     callback_data='after_tomorrow')
            ]
        ])

    def __get_hours_keyboard(self, begin, end, lang):
        inline_keyboard = []

        if begin == 6 and end == 17:

            button_data = 'next'

            if lang == 'uz':
                button_text = 'Keyingisi'

            if lang == 'ru':
                button_text = 'Следующий'

            inline_keyboard = [
                [
                    InlineKeyboardButton(f'{i}:00', callback_data=self.__btn_data(f'{i}')),
                    InlineKeyboardButton(f'{i + 1}:00', callback_data=self.__btn_data(f'{i + 1}')),
                    InlineKeyboardButton(f'{i + 2}:00', callback_data=self.__btn_data(f'{i + 2}')),
                ] for i in range(begin, end + 1, 3)
            ]

        elif begin == 18 and end == 29:

            button_data = 'back'

            if lang == 'uz':
                button_text = 'Orqaga'

            if lang == 'ru':
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

    def __get_minutes_keyboard(self, data, lang):

        if lang == 'uz':
            button_text = 'Orqaga'

        if lang == 'ru':
            button_text = 'Назад'

        inline_keyboard = [
            [
                InlineKeyboardButton(f'{data}:{i}', callback_data=self.__btn_data(f'{data}:{i}')),
                InlineKeyboardButton(f'{data}:{i + 10}', callback_data=self.__btn_data(f'{data}:{i + 10}')),
                InlineKeyboardButton(f'{data}:{i + 20}', callback_data=self.__btn_data(f'{data}:{i + 20}'))
            ] for i in range(0, 60, 30)
        ]

        inline_keyboard.append([InlineKeyboardButton(button_text, callback_data='back')])

        return InlineKeyboardMarkup(inline_keyboard)

    def __btn_data(self, button_data):
        # global j
        # j += 1
        # id = button_data.replace('region_id_','')
        # regions_data_list.update({int(id): button_data})
        return button_data

    def get_keyboard(self):

        return self.__keyboard


# z = InlineKeyboard('dates_keyboard', 'ru')
# x = InlineKeyboard('hours_keyboard', 'uz', begin=18, end=29)
# y = InlineKeyboard('minutes_keyboard', 'ru', data=13)
# print(y.get_keyboard())
