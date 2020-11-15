from telegram import ReplyKeyboardMarkup, KeyboardButton
from replykeyboards.replykeyboardtypes import *


class ReplyKeyboard(object):

    def __init__(self, keyb_type, lang):

        self.__type = keyb_type
        self.__lang = lang

        self.__keyboard = self.__create_reply_keyboard(self.__type, self.__lang)

    def __create_reply_keyboard(self, keyb_type, lang):

        if keyb_type == menu_keyboard:
            return self.__get_menu_keyboard(reply_keyboard_types[keyb_type][lang])

        elif keyb_type == settings_keyboard:

            return self.__get_settings_keyboard(reply_keyboard_types[keyb_type][lang])

        elif keyb_type == phone_number_keyboard:
            return self.__get_phone_number_keyboard(reply_keyboard_types[keyb_type][lang])

    @staticmethod
    def __get_menu_keyboard(lang):

        return ReplyKeyboardMarkup([

            [KeyboardButton(f'\U0001F4E6 {lang[1]}')],
            # [KeyboardButton(f'\U0001F4C4 {lang[2]}')],
            [KeyboardButton(f'\U0001F4C4 {lang[3]}')],
            [KeyboardButton(f'\U00002699 {lang[4]}')],

        ], resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def __get_settings_keyboard(lang):

        return ReplyKeyboardMarkup([

            [KeyboardButton(f'\U0001F4D4 {lang[1]}')],
            [KeyboardButton(f'\U0001F310 {lang[2]}')],
            [KeyboardButton(f'\U00002B05 {lang[3]}')],

        ], resize_keyboard=True)

    @staticmethod
    def __get_phone_number_keyboard(lang):
        return ReplyKeyboardMarkup([
            [
                KeyboardButton(f'\U0001F464 {lang[1]}', request_contact=True)]
        ], resize_keyboard=True)

    def get_keyboard(self):
        return self.__keyboard
