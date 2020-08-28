from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, CallbackContext, ConversationHandler, Filters, MessageHandler, \
    CommandHandler
from inlinekeyboards import InlineKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from DB.main import *
from languages import LANGS
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def main_inline_keyboard_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    user_input_data = context.user_data

    user = get_user(update.effective_user.id)

    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    #
    # with open('callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())
    # logger.info('user_input_data: %s', user_input_data)

    if data == BUTTONS_DATA_DICT[1]:
        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('user_data_keyboard', 'uz')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text(f"Ism: {user['name']}\n"
                                             f"Familya: {user['surname']}",
                                             reply_markup=inline_keyboard)
        elif user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('user_data_keyboard', 'ru')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text(f"Имя: {user['name']}\n"
                                             f"Фамиля: {user['surname']}",
                                             reply_markup=inline_keyboard)


    elif data == BUTTONS_DATA_DICT[6]:

        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('main_keyboard', 'uz')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text('MENU', reply_markup=inline_keyboard)

        elif user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('main_keyboard', 'ru')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text('MENU', reply_markup=inline_keyboard)


inline_keyboard_handler = CallbackQueryHandler(main_inline_keyboard_callback)
