from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from DB import *

regions_data_list = dict()
districts_data_list = []
j = 0


class InlineKeyboard(object):
    def __init__(self, keyboard_type, lang, region_id=None):
        self.type = keyboard_type
        self.lang = lang
        self.region_id = region_id
        self.__keyboard = self.create_inline_keyboard(self.type, self.lang, self.region_id)

    def create_inline_keyboard(self, keyb_type, lang, region_id):

        if lang == 'uz':
            if keyb_type == 'main_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Mening ma'lmotlarim",
                                              callback_data=self.__btn_data('user_data_btn')), ],

                        [InlineKeyboardButton("Yuk e'lon qilish",
                                              callback_data=self.__btn_data('new_cargo_btn')), ],

                    ]
                )
            elif keyb_type == 'user_data_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Ismni o'zgartirish",
                                              callback_data=self.__btn_data('change_name_btn')), ],

                        [InlineKeyboardButton("Familyani o'zgartirish",
                                              callback_data=self.__btn_data('change_surname_btn')), ],

                        [InlineKeyboardButton("Tilni o'zgartirish",
                                              callback_data=self.__btn_data('change_lang_btn')), ],

                        [InlineKeyboardButton("Orqaga", callback_data=self.__btn_data('back_btn')), ],
                    ]
                )
            elif keyb_type == 'langs_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("O'zbekcha",
                                              callback_data=self.__btn_data('uz_btn')), ],

                        [InlineKeyboardButton("Русский",
                                              callback_data=self.__btn_data('ru_btn')), ],

                        [InlineKeyboardButton("Orqaga", callback_data=self.__btn_data('back_btn')), ],
                    ]
                )
            elif keyb_type == 'regions_keyboard':
                regions = select_all_regions()
                return self.get_regions_keyboard(regions, lang)
            elif keyb_type == 'districts_keyboard':
                districts = select_all_districts(region_id)
                return self.get_districts_keyboard(districts, lang)

        if lang == 'ru':
            if keyb_type == 'main_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Мои данные", callback_data=self.__btn_data('user_data_btn')), ],
                        [InlineKeyboardButton("Объявить груз", callback_data=self.__btn_data('new_cargo_btn')), ],

                    ]
                )
            elif keyb_type == 'user_data_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Изменить имя",
                                              callback_data=self.__btn_data('change_name_btn')), ],

                        [InlineKeyboardButton("Изменить фамилию",
                                              callback_data=self.__btn_data('change_surname_btn')), ],

                        [InlineKeyboardButton("Изменить язык",
                                              callback_data=self.__btn_data('change_lang_btn')), ],

                        [InlineKeyboardButton("Назад", callback_data=self.__btn_data('back_btn')), ],

                    ]
                )
            elif keyb_type == 'langs_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("O'zbekcha",
                                              callback_data=self.__btn_data('uz_btn')), ],

                        [InlineKeyboardButton("Русский",
                                              callback_data=self.__btn_data('ru_btn')), ],

                        [InlineKeyboardButton("Hазад", callback_data=self.__btn_data('back_btn')), ],
                    ]
                )
            elif keyb_type == 'regions_keyboard':
                regions = select_all_regions()
                return self.get_regions_keyboard(regions, lang)
            elif keyb_type == 'districts_keyboard':
                districts = select_all_districts(region_id)
                return self.get_districts_keyboard(districts, lang)

        if lang == 'kr':
            pass
        return None

    def get_regions_keyboard(self, regions, lang):
        n = len(regions)
        if lang == 'uz':
            region_name = 'nameUz'
            odd_btn_text = 'Orqaga'
        else:
            region_name = 'nameRu'
            odd_btn_text = 'Назад'

        if n % 2 == 0:
            keyboard = [
                [
                    InlineKeyboardButton(regions[i][region_name],
                                         callback_data=self.__btn_data(f"region_id_{regions[i]['id']}")),

                    InlineKeyboardButton(regions[i + 1][region_name],
                                         callback_data=self.__btn_data(f"region_id_{regions[i + 1]['id']}"))
                ]

                for i in range(0, n, 2)
            ]

        if n % 2 != 0:
            keyboard = [
                [
                    InlineKeyboardButton(regions[i][region_name],
                                         callback_data=self.__btn_data(f"region_id_{regions[i]['id']}"))
                    , InlineKeyboardButton(odd_btn_text, callback_data='back_btn')
                ]
                if i == n - 1 else
                [
                    InlineKeyboardButton(regions[i][region_name],
                                         callback_data=self.__btn_data(f"region_id_{regions[i]['id']}")),
                    InlineKeyboardButton(regions[i + 1][region_name],
                                         callback_data=self.__btn_data(f"region_id_{regions[i + 1]['id']}"))
                ] for i in range(0, n, 2)
            ]

        return InlineKeyboardMarkup(keyboard)

    def get_districts_keyboard(self, districts, lang):
        n = len(districts)
        if lang == 'uz':
            district_name = 'nameUz'
            odd_btn_text = 'Orqaga'
        else:
            district_name = 'nameRu'
            odd_btn_text = 'Назад'

        if n % 2 == 0:
            keyboard = [
                [
                    InlineKeyboardButton(districts[i][district_name],
                                         callback_data=self.__btn_data(f"district_id_{districts[i]['id']}")),

                    InlineKeyboardButton(districts[i + 1][district_name],
                                         callback_data=self.__btn_data(f"district_id_{districts[i + 1]['id']}"))
                ]

                for i in range(0, n, 2)
            ]
            keyboard.append([InlineKeyboardButton(odd_btn_text, callback_data=self.__btn_data("back_btn"))])
        if n % 2 != 0:
            keyboard = [
                [
                    InlineKeyboardButton(districts[i][district_name],
                                         callback_data=self.__btn_data(f"district_id_{districts[i]['id']}"))
                    , InlineKeyboardButton(odd_btn_text, callback_data='back_btn')
                ]
                if i == n - 1 else
                [
                    InlineKeyboardButton(districts[i][district_name],
                                         callback_data=self.__btn_data(f"district_id_{districts[i]['id']}")),
                    InlineKeyboardButton(districts[i + 1][district_name],
                                         callback_data=self.__btn_data(f"district_id_{districts[i + 1]['id']}"))
                ] for i in range(0, n, 2)
            ]

        return InlineKeyboardMarkup(keyboard)

    def __btn_data(self, button_data):
        # global j
        # j += 1
        # id = button_data.replace('region_id_','')
        # regions_data_list.update({int(id): button_data})
        return button_data

    def get_keyboard(self):

        return self.__keyboard


# print(id(InlineKeyboard('main_keyboard', 'ru')))
# print(id(InlineKeyboard('user_data_keyboard', 'ru')))
# print(InlineKeyboard('main_keyboard', 'ru'))
# print(InlineKeyboard('user_data_keyboard', 'ru'))

# (InlineKeyboard('regions_keyboard', 'ru').get_keyboard())
# print(regions_data_list)
# print(InlineKeyboard('districts_keyboard', 'ru', 1).get_keyboard())
# InlineKeyboard('districts_keyboard', 'ru', 1).get_keyboard()
# print(len(regions_data_list))

# key1 = InlineKeyboard('main_keyboard', 'uz')
# key2 = InlineKeyboard('user_data_keyboard', 'uz')
# key3 = InlineKeyboard('user_data_keyboard', 'ru')
