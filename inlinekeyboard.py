from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from telegram import Update
from replykeyboards import *

inlinekeyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("O'zbekcha", callback_data='uzbek'),
    InlineKeyboardButton("Русский", callback_data='russian')
]])


def keyboard_callback_handler(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_data = context.user_data
    user_data['LANG'] = data
    # logger.info('user_data: %s', user_data)

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    with open('callback_query.json', 'w') as callback_query_file:
        callback_query_file.write(callback_query.to_json())

    if data == 'uzbek':
        reply_keyboard_markup = replykeyboard

        # callback_query.edit_message_reply_markup(
        # InlineKeyboardMarkup([[InlineKeyboardButton('test', callback_data='test_data')]])
        # )

        callback_query.edit_message_text(f'\U0001F44B Salom, {update.effective_user.first_name}')

        callback_query.message.reply_text(f'Davom etish uchun menga kontaktingizni yuboring \U0001F60A',
                                          reply_markup=reply_keyboard_markup)

    else:
        reply_keyboard_markup = replykeyboard_russ

        callback_query.edit_message_text(f'\U0001F44B  Привет, {update.effective_user.first_name}')

        callback_query.message.reply_text(f'Чтобы продолжить, отправьте мне свой контакт \U0001F60A',
                                          reply_markup=reply_keyboard_markup)
