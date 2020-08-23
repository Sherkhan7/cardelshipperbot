from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler,
                          CallbackQueryHandler, CallbackContext, Filters, )
from DB.main import *
import json

menu_uz = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Yuk e'lon qilish", callback_data='new_cargo_button'), ],
        [InlineKeyboardButton("Mening ma'lmotlarim", callback_data='my_data_button'), ]
    ]
)

menu_ru = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Объявить груз", callback_data='new_cargo_button'), ],
        [InlineKeyboardButton("Мои данные", callback_data='my_data_button'), ]
    ]
)
user_data_menu_uz = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Ismni o'zgartirish", callback_data='change_name_button'), ],
        [InlineKeyboardButton("Familyani o'zgartirish", callback_data='change_surname_button'), ],
        [InlineKeyboardButton("Tilni o'zgartirish", callback_data='change_lang_button'), ],
        [InlineKeyboardButton("Orqaga", callback_data='back_button'), ]
    ]
)

user_data_menu_ru = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Изменить имя", callback_data='change_name_button'), ],
        [InlineKeyboardButton("Изменить фамилию", callback_data='change_surname_button'), ],
        [InlineKeyboardButton("Изменить язык", callback_data='change_lang_button'), ],
        [InlineKeyboardButton("Назад", callback_data='back_button'), ]
    ]
)


def menu_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)
    user = json.loads(user)

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    with open('callback_query.json', 'w') as callback_query_file:
        callback_query_file.write(callback_query.to_json())

    if data == 'my_data_button':

        # callback_query.edit_message_reply_markup(
        # InlineKeyboardMarkup([[InlineKeyboardButton('test', callback_data='test_data')]])
        # )
        # callback_query.message.reply_text(f'Davom etish uchun menga kontaktingizni yuboring \U0001F60A',
        #                                   reply_markup=reply_button_markup)

        if user['lang'] == 'uzbek':
            callback_query.edit_message_text(f"Ism: {user['name']}\n"
                                             f"Familya: {user['surname']}",
                                             reply_markup=user_data_menu_uz)
        elif user['lang'] == 'russian':
            callback_query.edit_message_text(f"Имя: {user['name']}\n"
                                             f"Фамиля: {user['surname']}",
                                             reply_markup=user_data_menu_ru)

    elif data == 'new_cargo_button':
        pass

    elif data == 'back_button':

        if user['lang'] == 'uzbek':
            callback_query.edit_message_text('MENU', reply_markup=menu_uz)
            # callback_query.edit_message_reply_markup(reply_markup=menu_uz)
        elif user['lang'] == 'russian':
            callback_query.edit_message_text('MENU', reply_markup=menu_ru)
            # callback_query.edit_message_reply_markup(reply_markup=menu_ru)


def user_data_menu_callback(update: Update, context: CallbackContext):
    print('Inside func')
    callback_query = update.callback_query
    data = callback_query.data

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    with open('callback_query.json', 'w') as callback_query_file:
        callback_query_file.write(callback_query.to_json())

    if data == 'back_button':
        print('Inside if ')
        user = get_user(update.effective_user.id)
        user = json.loads(user)

        # callback_query.edit_message_reply_markup(
        # InlineKeyboardMarkup([[InlineKeyboardButton('test', callback_data='test_data')]])
        # )
        # callback_query.message.reply_text(f'Davom etish uchun menga kontaktingizni yuboring \U0001F60A',
        #                                   reply_markup=reply_button_markup)

        if user['lang'] == 'uzbek':
            callback_query.edit_message_text('MENU', reply_markup=menu_uz)
            # callback_query.edit_message_reply_markup(reply_markup=menu_uz)
        elif user['lang'] == 'russian':
            callback_query.edit_message_text('MENU', reply_markup=menu_ru)
            # callback_query.edit_message_reply_markup(reply_markup=menu_ru)


menu_handler = CallbackQueryHandler(menu_callback)
# user_data_menu_hadler = CallbackQueryHandler(user_data_menu_callback)
