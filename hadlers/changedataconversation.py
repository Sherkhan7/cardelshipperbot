from telegram import Update
from telegram.ext import (MessageHandler, ConversationHandler,
                          CallbackQueryHandler, CallbackContext, Filters, )
from inlinekeyboards import InlineKeyboard
from DB.main import *
from languages import LANGS
from hadlers.inlinekeyboardhandler import inline_keyboard_callback
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

USER_ID, NEW_NAME, NEW_SURNAME = \
    ('user_id', 'new_name', 'new_surname',)


def change_name_callback(update: Update, context: CallbackContext):
    user_input_data = context.user_data
    name = update.message.text
    user_input_data[NEW_NAME] = name
    user = get_user(update.effective_user.id)

    # logger.info('user_input_data: %s', user_input_data)

    if name == '/cancel' or name == '/menu' or name == '/start':
        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
            update.message.reply_text('Bekor qilindi.', reply_markup=inline_keyboard.get_keyboard())

        if user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
            update.message.reply_text('Отменено.', reply_markup=inline_keyboard.get_keyboard())

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
    # logger.info('user_input_data: %s', user_input_data)

    if surname == '/cancel' or surname == '/menu' or surname == '/start':
        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
            update.message.reply_text('Bekor qilindi.', reply_markup=inline_keyboard.get_keyboard())

        if user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
            update.message.reply_text('Отменено.', reply_markup=inline_keyboard.get_keyboard())

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


def do_menu(update, context):
    print('inside do_menU')
    return NEW_NAME


# new_handler = CallbackQueryHandler(inline_keyboard_callback)
changedataconversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(inline_keyboard_callback)],
    states={
        NEW_NAME: [MessageHandler(Filters.text, change_name_callback), ],
        NEW_SURNAME: [MessageHandler(Filters.text, change_surname_callback), ],
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
