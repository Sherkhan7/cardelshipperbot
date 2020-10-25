from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from DB import *
import datetime
from languages import LANGS
from units import UNITS


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
                    [InlineKeyboardButton('\U0001F1FA\U0001F1FF UZB', callback_data='uz')],

                    [InlineKeyboardButton('\U0001F1F7\U0001F1FA RUS', callback_data='ru')]
                ]
            )

        elif keyb_type == 'user_data_keyboard':
            return self.__get_user_data_keyboard(lang)

        elif keyb_type == 'regions_keyboard':

            return self.__get_regions_keyboard(lang, select_all_regions())

        elif keyb_type == 'districts_keyboard':

            return self.__get_districts_keyboard(lang, select_all_districts(region_id))

        elif keyb_type == 'weights_keyboard':

            return self.__get_weights_keyboard(lang)

        elif keyb_type == 'dates_keyboard':

            return self.__get_dates_keyboard(lang)

        elif keyb_type == 'hours_keyboard':

            return self.__get_hours_keyboard(lang, begin, end)

        elif keyb_type == 'minutes_keyboard':

            return self.__get_minutes_keyboard(lang, data)

        elif keyb_type == 'confirm_keyboard':

            return self.__get_confirm_keyboard(lang, data)

        elif keyb_type == 'edit_keyboard':

            return self.__get_edit_keyboard(lang)

        elif keyb_type == 'edit_address_keyboard':

            return self.__get_edit_address_keyboard(lang)

        elif keyb_type == 'edit_cargo_info_keyboard':

            return self.__get_edit_cargo_info_keyboard(lang)

    @staticmethod
    def __get_user_data_keyboard(lang):

        if lang == LANGS[0]:
            button1_text = 'Ismni o\'zgartirish'
            button2_text = 'Familyani o\'zgartirish'
            button3_text = 'Telefon nomerini o\'zgartirish'

        if lang == LANGS[1]:
            button1_text = 'Изменить имя'
            button2_text = 'Изменить фамилию'
            button3_text = 'Изменить номер телефона'

        button1_text = f'\U0001F464 {button1_text}'
        button2_text = f'\U0001F465 {button2_text}'
        button3_text = f'\U0001F4F1 {button3_text}'

        button1_data = 'change_name_btn'
        button2_data = 'change_surname_btn'
        button3_data = 'change_phone_btn'

        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(button1_text, callback_data=button1_data)],

                [InlineKeyboardButton(button2_text, callback_data=button2_data)],

                [InlineKeyboardButton(button3_text, callback_data=button3_data)],
            ]
        )

    @staticmethod
    def __get_regions_keyboard(lang, regions):

        length = len(regions)

        if lang == LANGS[0]:
            region_name = 'nameUz'
            # back_btn_text = 'Orqaga'

        if lang == LANGS[1]:
            region_name = 'nameRu'
            # back_btn_text = 'Назад'

        # back_btn_text = f'« {back_btn_text}'

        if length % 2 == 0:
            keyboard = [
                [
                    InlineKeyboardButton(regions[i][region_name], callback_data=regions[i]['id']),

                    InlineKeyboardButton(regions[i + 1][region_name], callback_data=regions[i + 1]['id'])
                ]

                for i in range(0, length, 2)
            ]

        if length % 2 != 0:
            keyboard = [
                [
                    InlineKeyboardButton(regions[i][region_name], callback_data=regions[i]['id']),
                    # InlineKeyboardButton(back_btn_text, callback_data='back_btn')
                ]

                if i == length - 1 else

                [
                    InlineKeyboardButton(regions[i][region_name], callback_data=regions[i]['id']),

                    InlineKeyboardButton(regions[i + 1][region_name], callback_data=regions[i + 1]['id'])
                ] for i in range(0, length, 2)
            ]

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def __get_districts_keyboard(lang, districts):

        length = len(districts)

        if lang == LANGS[0]:
            district_name = 'nameUz'
            back_btn_text = 'Orqaga'

        if lang == LANGS[1]:
            district_name = 'nameRu'
            back_btn_text = 'Назад'

        back_btn_text = f'« {back_btn_text}'
        back_btn_data = 'back_btn'

        if length % 2 == 0:
            keyboard = [
                [
                    InlineKeyboardButton(districts[i][district_name], callback_data=districts[i]['id']),

                    InlineKeyboardButton(districts[i + 1][district_name], callback_data=districts[i + 1]['id'])
                ] for i in range(0, length, 2)
            ]

            keyboard.append([InlineKeyboardButton(back_btn_text, callback_data=back_btn_data)])

        if length % 2 != 0:
            keyboard = [
                [
                    InlineKeyboardButton(districts[i][district_name], callback_data=districts[i]['id']),

                    InlineKeyboardButton(back_btn_text, callback_data=back_btn_data)
                ]

                if i == length - 1 else

                [
                    InlineKeyboardButton(districts[i][district_name], callback_data=districts[i]['id']),
                    InlineKeyboardButton(districts[i + 1][district_name], callback_data=districts[i + 1]['id'])
                ] for i in range(0, length, 2)
            ]

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def __get_weights_keyboard(lang):

        button1_text = UNITS[lang][0]
        button2_text = UNITS[lang][1]

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='kg'),

                InlineKeyboardButton(button2_text, callback_data='t')
            ]
        ])

    @staticmethod
    def __get_dates_keyboard(lang):

        if lang == LANGS[0]:
            button1_text = 'Hozir'
            button2_text = 'Bugun'

        if lang == LANGS[1]:
            button1_text = 'Сейчас'
            button2_text = 'Cегодня'

        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        after_tomorrow = tomorrow + datetime.timedelta(days=1)

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

            if lang == LANGS[0]:
                button_text = 'Keyingisi'

            if lang == LANGS[1]:
                button_text = 'Следующий'

            button_data = 'next'

            inline_keyboard = [
                [
                    InlineKeyboardButton(f'{i}:00', callback_data=f'{i}'),

                    InlineKeyboardButton(f'{i + 1}:00', callback_data=f'{i + 1}'),

                    InlineKeyboardButton(f'{i + 2}:00', callback_data=f'{i + 2}'),
                ] for i in range(begin, end + 1, 3)
            ]

        elif begin == 18 and end == 29:

            if lang == LANGS[0]:
                button_text = 'Orqaga'

            if lang == LANGS[1]:
                button_text = 'Назад'

            button_data = 'back_btn'

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
            back_btn_text = 'Orqaga'

        if lang == LANGS[1]:
            back_btn_text = 'Назад'

        back_btn_data = 'back_btn'

        minutes = {
            1: ['00', '10', '20'],
            2: ['30', '40', '50']
        }

        inline_keyboard = [
            [InlineKeyboardButton(f'{data}:{minute}', callback_data=f'{data}:{minute}') for minute in minutes_list]

            for minutes_list in minutes.values()
        ]

        inline_keyboard.append([InlineKeyboardButton(back_btn_text, callback_data=back_btn_data)])

        return InlineKeyboardMarkup(inline_keyboard)

    @staticmethod
    def __get_confirm_keyboard(lang, data):

        inline_keyboard = []

        if data['from_location']:
            from_latitude = data['from_location']['latitude']
            from_longitude = data['from_location']['longitude']

            inline_keyboard.append(
                [InlineKeyboardButton('A',
                                      url=f'http://www.google.com/maps/place/{from_latitude},{from_longitude}/'
                                          f'@{from_latitude},{from_longitude},12z')])

        if data['to_location']:
            to_latitude = data['to_location']['latitude']
            to_longitude = data['to_location']['longitude']

            inline_keyboard.append(
                [InlineKeyboardButton('B',
                                      url=f'http://www.google.com/maps/place/{to_latitude},{to_longitude}/'
                                          f'@{to_latitude},{to_longitude},12z')])

        if data['from_location'] and data['to_location']:
            direction = f'https://www.google.com/maps/dir/{from_latitude},{from_longitude}/{to_latitude},{to_longitude}'
            inline_keyboard.append([InlineKeyboardButton('A->B', url=direction)])

        if lang == LANGS[0]:
            button1_text = 'Tasdiqlash'
            button2_text = 'Tahrirlash'

        if lang == LANGS[1]:
            button1_text = 'Подтвердить'
            button2_text = 'Редактировать'

        inline_keyboard.append([
            InlineKeyboardButton(button1_text, callback_data='confirm'),

            InlineKeyboardButton(button2_text, callback_data='edit')
        ])

        return InlineKeyboardMarkup(inline_keyboard)

    @staticmethod
    def __get_edit_keyboard(lang):

        if lang == LANGS[0]:
            button1_text = 'Manzilni tahrirlash'
            button2_text = 'Yuk ma\'lumotlarini tahrirlash'
            button3_text = 'Kun va vaqtni tahrirlash'
            button4_text = 'Tahrirni yakunlash'

        if lang == LANGS[1]:
            button1_text = 'Редактировать адрес'
            button2_text = 'Редактировать информацию о грузе'
            button3_text = 'Редактировать дату и время'
            button4_text = 'Закончить редактирование'

        button4_text = f'« {button4_text}'

        return InlineKeyboardMarkup([
            [InlineKeyboardButton(button1_text, callback_data='edit_address')],

            [InlineKeyboardButton(button2_text, callback_data='edit_cargo_info')],

            [InlineKeyboardButton(button3_text, callback_data='edit_date_and_time')],

            [InlineKeyboardButton(button4_text, callback_data='terminate_editing')]
        ])

    @staticmethod
    def __get_edit_address_keyboard(lang):

        if lang == LANGS[0]:
            button1_text = 'Yuboruvchi manzilini tahrirlash'
            button2_text = 'Yuboruvchi geolokatsiyasini tahrirlash'
            button3_text = 'Qabul qiluvchi manzilini tahrirlash'
            button4_text = 'Qabul qiluvchi geolokatsiyasini tahrirlash'
            button5_text = 'Ortga'

        if lang == LANGS[1]:
            button1_text = 'Редактировать адрес отправителя'
            button2_text = 'Редактировать геолокацию отправителя'
            button3_text = 'Редактировать адрес получателя'
            button4_text = 'Редактировать геолокацию получателя'
            button5_text = 'Назад'

        button5_text = f'« {button5_text}'

        return InlineKeyboardMarkup([
            [InlineKeyboardButton(button1_text, callback_data='edit_from_address')],

            [InlineKeyboardButton(button2_text, callback_data='edit_from_location')],

            [InlineKeyboardButton(button3_text, callback_data='edit_to_address')],

            [InlineKeyboardButton(button4_text, callback_data='edit_to_location')],

            [InlineKeyboardButton(button5_text, callback_data='back')],

        ])

    @staticmethod
    def __get_edit_cargo_info_keyboard(lang):

        if lang == LANGS[0]:
            button1_text = 'Og\'irlikni tahrirlash'
            button2_text = 'Hajmni tahrirlash'
            button3_text = 'Tavsifni tahrirlash'
            button4_text = 'Rasmni tahrirlash'
            button5_text = 'Qabul qiluvchi telefonini tahrirlash'
            button6_text = 'Ortga'

        if lang == LANGS[1]:
            button1_text = 'Изменить вес'
            button2_text = 'Изменить объем'
            button3_text = 'Изменить описание'
            button4_text = 'Изменить фотография'
            button5_text = 'Изменить телефон получателя'
            button6_text = 'Назад'

        button6_text = f'« {button6_text}'

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='edit_weight'),

                InlineKeyboardButton(button2_text, callback_data='edit_volume')
            ],

            [
                InlineKeyboardButton(button3_text, callback_data='edit_definition'),

                InlineKeyboardButton(button4_text, callback_data='edit_photo')
            ],

            [InlineKeyboardButton(button5_text, callback_data='edit_receiver_phone')],

            [InlineKeyboardButton(button6_text, callback_data='back')],

        ])

    def get_keyboard(self):

        return self.__keyboard
