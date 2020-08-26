from telegram import InlineKeyboardButton, InlineKeyboardMarkup

BUTTONS_DATA_DICT = {
    1: 'user_data_button',
    2: 'new_cargo_button',
    3: 'change_name_button',
    4: 'change_surname_button',
    5: 'change_lang_button',
    7: 'uz_button',
    8: 'ru_button',
    9: 'kr_button',
    6: 'back_button',
}


class InlineKeyboard(object):
    def __init__(self, keyboard_type, lang):
        self.type = keyboard_type
        self.lang = lang

        self.__keyboard = self.create_inline_keyboard(self.lang, self.type)

    def create_inline_keyboard(self, lang, keyb_type):
        if lang == 'uz':
            if keyb_type == 'main_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Mening ma'lmotlarim",
                                              callback_data=self.__button_data('user_data_button')), ],

                        [InlineKeyboardButton("Yuk e'lon qilish",
                                              callback_data=self.__button_data('new_cargo_button')), ],

                    ]
                )
            elif keyb_type == 'user_data_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Ismni o'zgartirish",
                                              callback_data=self.__button_data('change_name_button')), ],

                        [InlineKeyboardButton("Familyani o'zgartirish",
                                              callback_data=self.__button_data('change_surname_button')), ],

                        [InlineKeyboardButton("Tilni o'zgartirish",
                                              callback_data=self.__button_data('change_lang_button')), ],

                        [InlineKeyboardButton("Orqaga", callback_data=self.__button_data('back_button')), ],
                    ]
                )
            elif keyb_type == 'langs_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("O'zbekcha",
                                              callback_data=self.__button_data('uz_button')), ],

                        [InlineKeyboardButton("Русский",
                                              callback_data=self.__button_data('ru_button')), ],

                        [InlineKeyboardButton("Orqaga", callback_data=self.__button_data('back_button')), ],
                    ]
                )

        if lang == 'ru':
            if keyb_type == 'main_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Мои данные", callback_data=self.__button_data('user_data_button')), ],
                        [InlineKeyboardButton("Объявить груз", callback_data=self.__button_data('new_cargo_button')), ],

                    ]
                )
            elif keyb_type == 'user_data_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Изменить имя",
                                              callback_data=self.__button_data('change_name_button')), ],

                        [InlineKeyboardButton("Изменить фамилию",
                                              callback_data=self.__button_data('change_surname_button')), ],

                        [InlineKeyboardButton("Изменить язык",
                                              callback_data=self.__button_data('change_lang_button')), ],

                        [InlineKeyboardButton("Назад", callback_data=self.__button_data('back_button')), ],

                    ]
                )
            elif keyb_type == 'langs_keyboard':
                return InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("O'zbekcha",
                                              callback_data=self.__button_data('uz_button')), ],

                        [InlineKeyboardButton("Русский",
                                              callback_data=self.__button_data('ru_button')), ],

                        [InlineKeyboardButton("Hазад", callback_data=self.__button_data('back_button')), ],
                    ]
                )

        if lang == 'kr':
            pass

        return None

    def __button_data(self, button_data):
        return button_data

    def get_keyboard(self):

        return self.__keyboard

# print(id(InlineKeyboard('main_keyboard', 'ru')))
# print(id(InlineKeyboard('user_data_keyboard', 'ru')))
# print(InlineKeyboard('main_keyboard', 'ru'))
# print(InlineKeyboard('user_data_keyboard', 'ru'))

# print(InlineKeyboard('main_keyboard', 'ru').get_keyboard())
# print(InlineKeyboard('user_data_keyboard', 'ru').get_keyboard())

# key1 = InlineKeyboard('main_keyboard', 'uz')
# key2 = InlineKeyboard('user_data_keyboard', 'uz')
# key3 = InlineKeyboard('user_data_keyboard', 'ru')