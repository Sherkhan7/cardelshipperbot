from telegram import Update, ParseMode
from telegram.ext import (MessageHandler, ConversationHandler,
                          CallbackQueryHandler, CallbackContext, Filters, )
from inlinekeyboards import InlineKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from layouts import *
from filters import phone_number_filter
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

USER_ID, NEW_NAME, NEW_SURNAME, NEW_PHONE_NUMBER = \
    ('user_id', 'new_name', 'new_surname', 'new_phone_number')


def change_name_callback(update: Update, context: CallbackContext):
    name = update.message.text

    user = get_user(update.effective_user.id)

    # print('change_name_callback')
    # logger.info('user_input_data: %s', user_input_data)

    # print('inside change name')

    if name == '/cancel' or name == '/menu' or name == '/start':

        if user['lang'] == LANGS[0]:
            text = 'Bekor qilindi.'

        if user['lang'] == LANGS[1]:
            text = 'Отменено.'

    else:

        result = update_user_info(user['user_id'], name=name)
        user = get_user(update.effective_user.id)

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

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang'])
    update.message.reply_text(get_user_info_layout(user), reply_markup=inline_keyboard.get_keyboard(),
                              parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def change_surname_callback(update: Update, context: CallbackContext):
    surname = update.message.text

    user = get_user(update.effective_user.id)

    # print('change_surname_callback')
    # logger.info('user_input_data: %s', user_input_data)

    if surname == '/cancel' or surname == '/menu' or surname == '/start':
        if user['lang'] == LANGS[0]:
            text = 'Bekor qilindi.'

        if user['lang'] == LANGS[1]:
            text = 'Отменено.'

    else:
        result = update_user_info(user['user_id'], surname=surname)
        user = get_user(update.effective_user.id)
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

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang'])
    update.message.reply_text(get_user_info_layout(user), reply_markup=inline_keyboard.get_keyboard(),
                              parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def change_phone_callback(update: Update, context: CallbackContext):
    phone_number = update.message.text

    user = get_user(update.effective_user.id)

    if phone_number == '/cancel' or phone_number == '/menu' or phone_number == '/start':
        if user['lang'] == LANGS[0]:
            text = 'Bekor qilindi.'

        if user['lang'] == LANGS[1]:
            text = 'Отменено.'

    else:

        phone_number = phone_number_filter(phone_number)

        if phone_number:

            result = update_user_info(user['user_id'], phone_number=phone_number)
            user = get_user(update.effective_user.id)

            if result == 'updated':
                if user['lang'] == LANGS[0]:
                    text = "Telefon raqamingiz o'zgatrilildi."

                if user['lang'] == LANGS[1]:
                    text = 'Ваш номер телефона был изменен.'

            elif result == 'not updated':
                if user['lang'] == LANGS[0]:
                    text = "Bu raqam ro'yxatdan o'tgan."

                if user['lang'] == LANGS[1]:
                    text = 'Этот номер зарегистрирован.'
        else:

            if user['lang'] == LANGS[0]:
                text = "Telefon raqami xato kiritildi !!!\n" \
                       "Qaytadan quyidagi shaklda kiriting:\n\n" \
                       "<b><i><u>Misol: 99 1234567</u></i></b>\nYoki\n" \
                       "<b><i><u>Misol: +998 99 1234567</u></i></b>\n"

            if user['lang'] == LANGS[1]:
                text = "Номер телефона введен неправильно !!!\n" \
                       "Введите еще раз в виде ниже:\n\n" \
                       "<b><i><u>Например: 99 1234567</u></i></b>\nИли\n" \
                       "<b><i><u>Например: +998 99 991234567</u></i></b>"

            update.message.reply_text(text, reply_to_message_id=update.message.message_id, parse_mode=ParseMode.HTML)

            return NEW_PHONE_NUMBER

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang'])
    update.message.reply_text(get_user_info_layout(user), reply_markup=inline_keyboard.get_keyboard(),
                              parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def change_data_callback(update: Update, context: CallbackContext):
    # print('changa data callback')
    callback_query = update.callback_query
    data = callback_query.data

    # print(data)
    user = get_user(update.effective_user.id)

    if data == BUTTONS_DATA_DICT[3] or data == BUTTONS_DATA_DICT[4]:

        if data == BUTTONS_DATA_DICT[3]:

            if user['lang'] == LANGS[0]:
                text = "<i>Ismni o'zgartirish</i>"
                reply_text = 'Ismningizni kiriting:'

            if user['lang'] == LANGS[1]:
                text = '<i>Изменить имя</i>'
                reply_text = 'Введите ваше имя:'

            return_value = NEW_NAME

        if data == BUTTONS_DATA_DICT[4]:

            if user['lang'] == LANGS[0]:
                text = "<i>Familyani o'zgartirish</i>"
                reply_text = 'Familyangizni kiriting:'

            if user['lang'] == LANGS[1]:
                text = '<i>Изменить фамилию</i>'
                reply_text = 'Введите свою фамилию:'

            return_value = NEW_SURNAME

    if data == BUTTONS_DATA_DICT[5]:

        if user['lang'] == LANGS[0]:
            text = "<i>Telefon raqamini o'zgartirish</i>"
            reply_text = "Telefon raqamni quyidagi shaklda yuboring:\n\n" \
                         "<b><i><u>Misol: 99 1234567</u></i></b>\nYoki\n" \
                         "<b><i><u>Misol: +998 99 1234567</u></i></b>\n\n"

        if user['lang'] == LANGS[1]:
            text = '<i>Изменить номер телефона</i>'
            reply_text = "Отправьте номер телефона в виде ниже:\n\n" \
                         "<b><i><u>Например: 99 1234567</u></i></b>\nYoki\n" \
                         "<b><i><u>Например: +998 99 1234567</u></i></b>\n\n"

        return_value = NEW_PHONE_NUMBER

    callback_query.edit_message_text(text, parse_mode=ParseMode.HTML)
    callback_query.message.reply_text(reply_text, parse_mode=ParseMode.HTML)

    return return_value


changedataconversation_handler = ConversationHandler(

    entry_points=[CallbackQueryHandler(change_data_callback, pattern='^change')],

    states={

        NEW_NAME: [MessageHandler(Filters.text, change_name_callback), ],

        NEW_SURNAME: [MessageHandler(Filters.text, change_surname_callback), ],

        NEW_PHONE_NUMBER: [MessageHandler(Filters.text, change_phone_callback)]
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
