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
    # print('change_name_callback')
    # logger.info('user_input_data: %s', user_input_data)

    if name == '/cancel' or name == '/menu' or name == '/start':
        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
            update.message.reply_text('Bekor qilindi.', reply_markup=inline_keyboard.get_keyboard())

        if user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
            update.message.reply_text('Отменено.', reply_markup=inline_keyboard.get_keyboard())

        return ConversationHandler.END

    else:
        result = update_user_info(user['user_id'], name=name)
        # print(result)

        if result == 'updated':
            if user['lang'] == LANGS[0]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
                update.message.reply_text("Ismingiz o'zgatirildi.", reply_markup=inline_keyboard.get_keyboard())

            elif user['lang'] == LANGS[1]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
                update.message.reply_text('Ваше имя изменено.', reply_markup=inline_keyboard.get_keyboard())

        elif result == 'not updated':
            if user['lang'] == LANGS[0]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
                update.message.reply_text("Ismingiz o'zgartirilmadi.", reply_markup=inline_keyboard.get_keyboard())

            elif user['lang'] == LANGS[1]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
                update.message.reply_text('Ваше имя не было изменено.', reply_markup=inline_keyboard.get_keyboard())

    return ConversationHandler.END


def change_surname_callback(update: Update, context: CallbackContext):
    user_input_data = context.user_data
    surname = update.message.text
    user_input_data[NEW_SURNAME] = surname
    user = get_user(update.effective_user.id)
    # print('change_surname_callback')
    # logger.info('user_input_data: %s', user_input_data)

    if surname == '/cancel' or surname == '/menu' or surname == '/start':
        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
            update.message.reply_text('Bekor qilindi.', reply_markup=inline_keyboard.get_keyboard())

        if user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
            update.message.reply_text('Отменено.', reply_markup=inline_keyboard.get_keyboard())

        return ConversationHandler.END

    else:
        result = update_user_info(user['user_id'], surname=surname)
        # print(result)

        if result == 'updated':
            if user['lang'] == LANGS[0]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
                update.message.reply_text("Familyangiz o'zgatrilildi.", reply_markup=inline_keyboard.get_keyboard())

            elif user['lang'] == LANGS[1]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
                update.message.reply_text('Ваша фамилия изменена', reply_markup=inline_keyboard.get_keyboard())

        elif result == 'not updated':
            if user['lang'] == LANGS[0]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
                update.message.reply_text("Familyangiz o'zgartirilmadi.", reply_markup=inline_keyboard.get_keyboard())

            elif user['lang'] == LANGS[1]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
                update.message.reply_text('Ваше фамилия не было изменено.', reply_markup=inline_keyboard.get_keyboard())

    return ConversationHandler.END


def change_lang_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)
    # print('inside change lang callback')

    if data == BUTTONS_DATA_DICT[7]:
        update_user_info(user['user_id'], lang=LANGS[0])

        if user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('langs_keyboard', LANGS[0])

            callback_query.edit_message_text('Tilni tanlang:', reply_markup=inline_keyboard.get_keyboard())

            context.bot.answer_callback_query(callback_query.id, "Til: O'zbekcha")

    elif data == BUTTONS_DATA_DICT[8]:
        update_user_info(user['user_id'], lang=LANGS[1])

        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('langs_keyboard', 'ru')

            callback_query.edit_message_text('Выберите язык:', reply_markup=inline_keyboard.get_keyboard())
            context.bot.answer_callback_query(callback_query.id, "Язык: русский")

    return ConversationHandler.END


def change_data_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)

    if data == BUTTONS_DATA_DICT[3]:

        if user['lang'] == LANGS[0]:

            callback_query.edit_message_text('Ismningizni kiriting:')

        elif user['lang'] == LANGS[1]:
            callback_query.edit_message_text('Введите ваше имя:')

        return NEW_NAME

    elif data == BUTTONS_DATA_DICT[4]:
        if user['lang'] == LANGS[0]:

            callback_query.edit_message_text('Familyangizni kiriting:')

        elif user['lang'] == LANGS[1]:
            callback_query.edit_message_text('Введите свою фамилию:')

        return NEW_SURNAME

    elif data == BUTTONS_DATA_DICT[5]:

        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('langs_keyboard', 'uz')

            callback_query.edit_message_text('Tilni tanlang:', reply_markup=inline_keyboard.get_keyboard())

        elif user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('langs_keyboard', 'ru')

            callback_query.edit_message_text('Выберите язык:', reply_markup=inline_keyboard.get_keyboard())

        return NEW_LANG


changedataconversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(change_data_callback, pattern='^change')],
    states={
        NEW_NAME: [MessageHandler(Filters.text, change_name_callback), ],
        NEW_SURNAME: [MessageHandler(Filters.text, change_surname_callback), ],
        NEW_LANG: [CallbackQueryHandler(change_lang_callback, pattern='^uz|ru|kr')]
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
