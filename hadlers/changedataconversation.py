from telegram import Update
from telegram.ext import (MessageHandler, ConversationHandler,
                          CallbackQueryHandler, CallbackContext, Filters, )
from inlinekeyboards import InlineKeyboard
from DB.main import *
from buttonsdatadict import BUTTONS_DATA_DICT
from languages import LANGS
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

USER_ID, NEW_NAME, NEW_SURNAME, NEW_LANG = \
    ('user_id', 'new_name', 'new_surname', 'new_lang')


def change_name_callback(update: Update, context: CallbackContext):
    user_input_data = context.user_data
    name = update.message.text
    user_input_data[NEW_NAME] = name

    user = get_user(update.effective_user.id)
    inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])

    # print('change_name_callback')
    # logger.info('user_input_data: %s', user_input_data)

    if name == '/cancel' or name == '/menu' or name == '/start':

        if user['lang'] == LANGS[0]:
            text = 'Bekor qilindi.'

        if user['lang'] == LANGS[1]:
            text = 'Отменено.'

    else:
        result = update_user_info(user['user_id'], name=name)
        # print(result)

        if result == 'updated':

            if user['lang'] == LANGS[0]:
                text = "Ismingiz o'zgatirildi."

            if user['lang'] == LANGS[1]:
                text = 'Ваше имя изменено.'

        elif result == 'not updated':

            if user['lang'] == LANGS[0]:
                text = "Ismingiz o'zgartirilmadi."

            if user['lang'] == LANGS[1]:
                text = 'Ваше имя не было изменено.'

    update.message.reply_text(text, reply_markup=inline_keyboard.get_keyboard())

    return ConversationHandler.END


def change_surname_callback(update: Update, context: CallbackContext):
    user_input_data = context.user_data
    surname = update.message.text
    user_input_data[NEW_SURNAME] = surname

    user = get_user(update.effective_user.id)
    inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
    # print('change_surname_callback')
    # logger.info('user_input_data: %s', user_input_data)

    if surname == '/cancel' or surname == '/menu' or surname == '/start':
        if user['lang'] == LANGS[0]:
            text = 'Bekor qilindi.'

        if user['lang'] == LANGS[1]:
            text = 'Отменено.'

    else:
        result = update_user_info(user['user_id'], surname=surname)
        # print(result)

        if result == 'updated':
            if user['lang'] == LANGS[0]:
                text = "Familyangiz o'zgatrilildi."

            if user['lang'] == LANGS[1]:
                text = 'Ваша фамилия изменена'

        elif result == 'not updated':
            if user['lang'] == LANGS[0]:
                text = "Familyangiz o'zgartirilmadi."

            if user['lang'] == LANGS[1]:
                text = 'Ваше фамилия не было изменено.'

    update.message.reply_text(text, reply_markup=inline_keyboard.get_keyboard())

    return ConversationHandler.END


def change_lang_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)
    # print('inside change lang callback')

    if data == BUTTONS_DATA_DICT[7]:

        lang = LANGS[0]
        text = "Til: O'zbekcha"

    elif data == BUTTONS_DATA_DICT[8]:

        lang = LANGS[1]
        text = "Язык: русский"

    context.bot.answer_callback_query(callback_query.id, text)
    inline_keyboard = InlineKeyboard('main_keyboard', lang)
    callback_query.edit_message_text('MENU:', reply_markup=inline_keyboard.get_keyboard())

    update_user_info(user['user_id'], lang=lang)
    return ConversationHandler.END


def txt_in_lang_callback(update: Update, context: CallbackContext):
    text = update.message.text

    user = get_user(update.effective_user.id)

    if user['lang'] == LANGS[0]:
        text = 'Bekor qilindi.'

    if user['lang'] == LANGS[1]:
        text = 'Отменено.'

    inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])

    update.message.reply_text(text, reply_markup=inline_keyboard.get_keyboard())
    return ConversationHandler.END


def change_data_callback(update: Update, context: CallbackContext):
    # print('changa data callback')
    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)

    if data == BUTTONS_DATA_DICT[3] or data == BUTTONS_DATA_DICT[4]:

        if data == BUTTONS_DATA_DICT[3]:

            if user['lang'] == LANGS[0]:
                text = 'Ismningizni kiriting:'

            if user['lang'] == LANGS[1]:
                text = 'Введите ваше имя:'

            return_value = NEW_NAME

        if data == BUTTONS_DATA_DICT[4]:

            if user['lang'] == LANGS[0]:
                text = 'Familyangizni kiriting:'

            if user['lang'] == LANGS[1]:
                text = 'Введите свою фамилию:'

            return_value = NEW_SURNAME

        callback_query.edit_message_text(text)

        return return_value

    elif data == BUTTONS_DATA_DICT[5]:

        inline_keyboard = InlineKeyboard('langs_keyboard')

        if user['lang'] == LANGS[0]:
            text = 'Tilni tanlang:'

        if user['lang'] == LANGS[1]:
            text = 'Выберите язык:'

        callback_query.edit_message_text(text, reply_markup=inline_keyboard.get_keyboard())

        return NEW_LANG


changedataconversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(change_data_callback, pattern='^change')],
    states={
        NEW_NAME: [MessageHandler(Filters.text, change_name_callback), ],
        NEW_SURNAME: [MessageHandler(Filters.text, change_surname_callback), ],
        NEW_LANG: [CallbackQueryHandler(change_lang_callback, pattern='^uz|ru|kr'),
                   MessageHandler(Filters.text, txt_in_lang_callback)]
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
