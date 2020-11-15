from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from DB import *
import datetime
from units import UNITS
from inlinekeyboards.inlinekeyboardtypes import *
from globalvariables import *
from layouts import NEW_CARGO_LAYOUT_DICT


class InlineKeyboard(object):
    def __init__(self, keyb_type, lang=None, region_id=None, begin=None, end=None, data=None, geolocation=None):

        self.__type = keyb_type
        self.__lang = lang
        self.__region_id = region_id
        self.__begin = begin
        self.__end = end
        self.__data = data
        self.__geolocation = geolocation
        self.__keyboard = self.__create_inline_keyboard(self.__type, self.__lang, self.__region_id,
                                                        self.__begin, self.__end, self.__data, self.__geolocation)

    def __create_inline_keyboard(self, keyb_type, lang, region_id, begin, end, data, geolocation):

        if keyb_type == langs_keyboard:

            return self.__get_langs_keyboard()

        elif keyb_type == user_data_keyboard:

            return self.__get_user_data_keyboard(lang, keyb_type)

        elif keyb_type == regions_keyboard:
            regions = select_all_regions()

            return self.__get_regions_keyboard(lang, keyb_type, regions)

        elif keyb_type == districts_keyboard:
            districts = select_all_districts(region_id)

            return self.__get_regions_keyboard(lang, keyb_type, districts)

        elif keyb_type == weights_keyboard:

            return self.__get_weights_keyboard(lang)

        elif keyb_type == dates_keyboard:

            return self.__get_dates_keyboard(lang)

        elif keyb_type == hours_keyboard:

            return self.__get_hours_keyboard(lang, begin, end)

        elif keyb_type == minutes_keyboard:

            return self.__get_minutes_keyboard(lang, data)

        elif keyb_type == confirm_keyboard:

            return self.__get_confirm_keyboard(lang, data, geolocation)

        elif keyb_type == edit_keyboard:

            return self.__get_edit_keyboard(lang)

        elif keyb_type == edit_address_keyboard:

            return self.__get_edit_address_keyboard(lang)

        elif keyb_type == edit_cargo_info_keyboard:

            return self.__get_edit_cargo_info_keyboard(lang)

        elif keyb_type == paginate_keyboard:

            return self.__get_paginate_keyboard(lang, data)

    @staticmethod
    def __get_langs_keyboard():

        return InlineKeyboardMarkup([
            [InlineKeyboardButton('\U0001F1FA\U0001F1FF UZB', callback_data='uz')],
            [InlineKeyboardButton('\U0001F1F7\U0001F1FA RUS', callback_data='ru')],
            [InlineKeyboardButton('\U0001F1FA\U0001F1FF УЗБ', callback_data='cy')],
        ])

    @staticmethod
    def __get_user_data_keyboard(lang, keyb_type):

        button1_text = f'\U0001F464 {inline_keyboard_types[keyb_type][lang][1]}'
        button2_text = f'\U0001F465 {inline_keyboard_types[keyb_type][lang][2]}'

        button1_data = 'change_name_btn'
        button2_data = 'change_surname_btn'

        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(button1_text, callback_data=button1_data)],

                [InlineKeyboardButton(button2_text, callback_data=button2_data)],
            ]
        )

    @staticmethod
    def __get_regions_keyboard(lang, keyb_type, regions):

        length = len(regions)

        region_name = inline_keyboard_types[regions_keyboard][lang][1]
        back_btn_text = f'« {inline_keyboard_types[regions_keyboard][lang]["back_btn_text"]}'
        back_btn_data = 'back_btn'

        if length % 2 == 0:

            keyboard = [
                [
                    InlineKeyboardButton(regions[i][region_name], callback_data=regions[i]['id']),

                    InlineKeyboardButton(regions[i + 1][region_name], callback_data=regions[i + 1]['id'])
                ]

                for i in range(0, length, 2)
            ]

            if keyb_type == districts_keyboard:
                keyboard.append([InlineKeyboardButton(back_btn_text, callback_data=back_btn_data)])

        if length % 2 != 0:
            keyboard = [
                [
                    InlineKeyboardButton(regions[i][region_name], callback_data=regions[i]['id']),
                    InlineKeyboardButton(back_btn_text, callback_data=back_btn_data)
                ]

                if i == length - 1 else

                [
                    InlineKeyboardButton(regions[i][region_name], callback_data=regions[i]['id']),

                    InlineKeyboardButton(regions[i + 1][region_name], callback_data=regions[i + 1]['id'])
                ] for i in range(0, length, 2)
            ]

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def __get_weights_keyboard(lang):

        button1_text = UNITS[lang]['kg']
        button2_text = UNITS[lang]['t']

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='kg'),

                InlineKeyboardButton(button2_text, callback_data='t')
            ]
        ])

    @staticmethod
    def __get_dates_keyboard(lang):

        button1_text = inline_keyboard_types[dates_keyboard][lang][0]
        button2_text = inline_keyboard_types[dates_keyboard][lang][1]

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
            button_text = inline_keyboard_types[hours_keyboard][lang]['next_btn_text']
            button_data = 'next_btn'

            inline_keyboard = [
                [
                    InlineKeyboardButton(f'{i}:00', callback_data=f'{i}:00'),

                    InlineKeyboardButton(f'{i + 1}:00', callback_data=f'{i + 1}:00'),

                    InlineKeyboardButton(f'{i + 2}:00', callback_data=f'{i + 2}:00'),
                ] for i in range(begin, end + 1, 3)
            ]

        elif begin == 18 and end == 29:
            button_text = inline_keyboard_types[hours_keyboard][lang]['back_btn_text']
            button_data = 'back_btn'

            for i in range(begin, end + 1, 3):

                if i == 24:
                    i = 0

                if i == 27:
                    i = 3

                inline_keyboard.append([

                    InlineKeyboardButton(f'{i}:00', callback_data=f'{i}:00'),

                    InlineKeyboardButton(f'{i + 1}:00', callback_data=f'{i + 1}:00'),

                    InlineKeyboardButton(f'{i + 2}:00', callback_data=f'{i + 2}:00'),

                ])

        inline_keyboard.append([InlineKeyboardButton(button_text, callback_data=button_data)])

        return InlineKeyboardMarkup(inline_keyboard)

    @staticmethod
    def __get_minutes_keyboard(lang, data):
        back_btn_text = inline_keyboard_types[hours_keyboard][lang]['back_btn_text']
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
    def __get_confirm_keyboard(lang, data, geolocation=None):

        inline_keyboard = []

        button1_text = NEW_CARGO_LAYOUT_DICT[lang][FROM_TEXT]
        button2_text = NEW_CARGO_LAYOUT_DICT[lang][TO_TEXT]

        button1_text = f'\U0001F4CD {button1_text}'
        button2_text = f'\U0001F3C1 {button2_text}'
        button3_text = f'\U0001F4CD -> \U0001F3C1'

        if data[FROM_LOCATION]:
            from_latitude = data[FROM_LOCATION]['latitude']
            from_longitude = data[FROM_LOCATION]['longitude']

            inline_keyboard.append(
                [InlineKeyboardButton(button1_text,
                                      url=f'http://www.google.com/maps/place/{from_latitude},{from_longitude}/'
                                          f'@{from_latitude},{from_longitude},12z')])

        if data[TO_LOCATION]:
            to_latitude = data[TO_LOCATION]['latitude']
            to_longitude = data[TO_LOCATION]['longitude']

            inline_keyboard.append(
                [InlineKeyboardButton(button2_text,
                                      url=f'http://www.google.com/maps/place/{to_latitude},{to_longitude}/'
                                          f'@{to_latitude},{to_longitude},12z')])

        if data[FROM_LOCATION] and data[TO_LOCATION]:
            direction = f'https://www.google.com/maps/dir/{from_latitude},{from_longitude}/{to_latitude},{to_longitude}'
            inline_keyboard.append([InlineKeyboardButton(button3_text, url=direction)])

        if geolocation:
            return InlineKeyboardMarkup(inline_keyboard)

        button1_text = inline_keyboard_types[confirm_keyboard][lang][0]
        button2_text = inline_keyboard_types[confirm_keyboard][lang][1]

        inline_keyboard.append([
            InlineKeyboardButton(button1_text, callback_data='confirm'),

            InlineKeyboardButton(button2_text, callback_data='edit')
        ])

        return InlineKeyboardMarkup(inline_keyboard)

    @staticmethod
    def __get_edit_keyboard(lang):

        button1_text = inline_keyboard_types[edit_keyboard][lang][1]
        button2_text = inline_keyboard_types[edit_keyboard][lang][2]
        button3_text = inline_keyboard_types[edit_keyboard][lang][3]
        button4_text = inline_keyboard_types[edit_keyboard][lang][4]
        button4_text = f'« {button4_text}'

        return InlineKeyboardMarkup([

            [InlineKeyboardButton(button1_text, callback_data='edit_address')],

            [InlineKeyboardButton(button2_text, callback_data='edit_cargo_info')],

            [InlineKeyboardButton(button3_text, callback_data='edit_date_and_time')],

            [InlineKeyboardButton(button4_text, callback_data='terminate_editing')]
        ])

    @staticmethod
    def __get_edit_address_keyboard(lang):

        button1_text = inline_keyboard_types[edit_address_keyboard][lang][1]
        button2_text = inline_keyboard_types[edit_address_keyboard][lang][2]
        button3_text = inline_keyboard_types[edit_address_keyboard][lang][3]
        button4_text = inline_keyboard_types[edit_address_keyboard][lang][4]
        button5_text = inline_keyboard_types[edit_address_keyboard][lang][5]
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

        button1_text = inline_keyboard_types[edit_cargo_info_keyboard][lang][1]
        button2_text = inline_keyboard_types[edit_cargo_info_keyboard][lang][2]
        button3_text = inline_keyboard_types[edit_cargo_info_keyboard][lang][3]
        button4_text = inline_keyboard_types[edit_cargo_info_keyboard][lang][4]
        button5_text = inline_keyboard_types[edit_cargo_info_keyboard][lang][5]
        button6_text = inline_keyboard_types[edit_cargo_info_keyboard][lang][6]
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

            [InlineKeyboardButton(button5_text, callback_data='edit_client_phone')],

            [InlineKeyboardButton(button6_text, callback_data='back')],

        ])

    @staticmethod
    def __get_paginate_keyboard(lang, data):

        wanted, length, client_cargoes = data
        wanted_cargo_data = client_cargoes[wanted - 1]

        close_text = inline_keyboard_types[paginate_keyboard][lang][0]
        open_text = inline_keyboard_types[paginate_keyboard][lang][1]

        if wanted_cargo_data['state'] == 'opened':
            button4_text = f'\U0001F534 {close_text}'
            button4_data = f'{wanted_cargo_data["id"]}_closed'

        elif wanted_cargo_data['state'] == 'closed':
            button4_text = f'{open_text}'
            button4_data = f'{wanted_cargo_data["id"]}_opened'

        if wanted == 1 and length == 1:
            button1_text = '.'
            button1_data = 'dot_1'

            button3_text = '.'
            button3_data = 'dot_2'

        elif wanted == 1 and length > 1:
            button1_text = '.'
            button1_data = 'dot'

            button3_text = '\U000023E9'
            button3_data = f'w_{wanted + 1}'

        elif wanted == length:
            button1_text = '\U000023EA'
            button1_data = f'w_{wanted - 1}'

            button3_text = '.'
            button3_data = 'dot'

        else:
            button1_text = '\U000023EA'
            button1_data = f'w_{wanted - 1}'

            button3_text = '\U000023E9'
            button3_data = f'w_{wanted + 1}'

        button2_text = f'{wanted}/{length}'
        button2_data = 'None'

        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data=button1_data),
                InlineKeyboardButton(button2_text, callback_data=button2_data),
                InlineKeyboardButton(button3_text, callback_data=button3_data),
            ],
            [
                InlineKeyboardButton(button4_text, callback_data=button4_data),
            ]
        ])

    def get_keyboard(self):

        return self.__keyboard
