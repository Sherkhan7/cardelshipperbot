from telegram import ReplyKeyboardMarkup, KeyboardButton
from languages import LANGS


class ReplyKeyboard(object):

    def __init__(self, keyboard_type, lang=None):

        self.__type = keyboard_type
        self.__lang = lang

        self.__keyboard = self.__create_reply_keyboard(self.__type, self.__lang)

    def __create_reply_keyboard(self, keyb_type, lang):

        if keyb_type == 'phone_number_keyboard':
            return self.__get_phone_number_keyboard(lang)

        if keyb_type == 'menu_keyboard':

            return self.__get_menu_keyboard(lang)

        elif keyb_type == 'settings_keyboard':

            return self.__get_settings_keyboard(lang)

    @staticmethod
    def __get_menu_keyboard(lang):

        if lang == LANGS[0]:
            button_1_text = "Yuk e'lon qilish"
            button_2_text = "E'lonlar"
            button_3_text = "E'lonlar tarixi"
            button_4_text = "Sozlamalar"
            button_5_text = "Biz bilan bo'glanish"

        if lang == LANGS[1]:
            button_1_text = "Объявить груз"
            button_2_text = "Объявления"
            button_3_text = "История объявлений"
            button_4_text = "Настройки"
            button_5_text = "Связаться с нами"

        return ReplyKeyboardMarkup([

            [KeyboardButton(f'\U0001F4E6 {button_1_text}')],
            [
                KeyboardButton(f'\U0001F4DC	{button_2_text}'),
                KeyboardButton(f'\U0001F5C4 {button_3_text}')
            ],
            [
                KeyboardButton(f'\U00002699 {button_4_text}'),
                KeyboardButton(f'\U0001F4E9	{button_5_text}')
            ],
        ], resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def __get_settings_keyboard(lang):

        if lang == LANGS[0]:
            button_1_text = "Mening ma'lumotlarim"
            button_2_text = "Tilni o'zgartirish"
            button_3_text = 'Ortga'

        if lang == LANGS[1]:
            button_1_text = "Мои данные"
            button_2_text = "Изменить язык"
            button_3_text = "Назад"

        return ReplyKeyboardMarkup([

            [KeyboardButton(f'\U0001F4D4 {button_1_text}'), ],
            [KeyboardButton(f'\U0001F310 {button_2_text}'), ],
            [KeyboardButton(f'\U00002B05 {button_3_text}'), ],

        ], resize_keyboard=True)

    @staticmethod
    def __get_phone_number_keyboard(lang):

        if lang == LANGS[0]:
            button_text = 'Kontaktimni yuborish'

        if lang == LANGS[1]:
            button_text = 'Отправить мой контакт'

        return ReplyKeyboardMarkup([
            [
                KeyboardButton(f'\U0001F464 {button_text}', request_contact=True)]
        ], resize_keyboard=True)

    def get_keyboard(self):
        return self.__keyboard

# reply_keyboard = ReplyKeyboard('menu_keyboard', 'uz')
# print(reply_keyboard.get_keyboard())
