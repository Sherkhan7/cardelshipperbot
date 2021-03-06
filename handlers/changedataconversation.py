from telegram import Update, ParseMode
from telegram.ext import (MessageHandler, ConversationHandler,
                          CallbackQueryHandler, CallbackContext, Filters, )
from inlinekeyboards import InlineKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from layouts import *
from filters import phone_number_filter
from helpers import set_user_data_in_bot_data
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

USER_ID, NEW_NAME, NEW_SURNAME, NEW_PHONE_NUMBER = \
    ('user_id', 'new_name', 'new_surname', 'new_phone_number')


def change_data_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    bot_data = context.bot_data

    # set bot_data[update.effective_user.id] -> dict
    set_user_data_in_bot_data(update.effective_user.id, bot_data)
    user = bot_data[update.effective_user.id]

    if data == BUTTONS_DATA_DICT[3] or data == BUTTONS_DATA_DICT[4]:

        if data == BUTTONS_DATA_DICT[3]:

            if user['lang'] == LANGS[0]:
                text = 'Ismni o\'zgartirish'
                reply_text = 'Ismningizni yuboring'

            if user['lang'] == LANGS[1]:
                text = 'Изменить имя'
                reply_text = 'Отправьте ваше имя'

            state = NEW_NAME

        if data == BUTTONS_DATA_DICT[4]:

            if user['lang'] == LANGS[0]:
                text = 'Familyani o\'zgartirish'
                reply_text = 'Familyangizni yuboring'

            if user['lang'] == LANGS[1]:
                text = 'Изменить фамилию'
                reply_text = 'Отправьте свою фамилию'

            state = NEW_SURNAME

    if data == BUTTONS_DATA_DICT[5]:

        if user['lang'] == LANGS[0]:
            text = 'Telefon raqamini o\'zgartirish'

        if user['lang'] == LANGS[1]:
            text = 'Изменить номер телефона'

        state = NEW_PHONE_NUMBER

        reply_text = get_phone_number_layout(user['lang'])

    text = f'<i>{text}</i>'
    callback_query.edit_message_text(text, parse_mode=ParseMode.HTML)
    callback_query.message.reply_html(reply_text + ' :')

    return state


def change_name_callback(update: Update, context: CallbackContext):
    name = update.message.text

    bot_data = context.bot_data
    user = context.bot_data[update.effective_user.id]

    if name == '/cancel' or name == '/menu' or name == '/start':

        if user['lang'] == LANGS[0]:
            text = 'Ismni o\'zgrtirish bekor qilindi'

        if user['lang'] == LANGS[1]:
            text = 'Смена имени отменена'

        text = f'\U0000274C {text}.'

    else:

        result = update_user_info(user['user_id'], name=name)

        if result == 'updated':

            bot_data[update.effective_user.id]['name'] = name

            if user['lang'] == LANGS[0]:
                text = 'Ismingiz o\'zgatirildi'

            if user['lang'] == LANGS[1]:
                text = 'Ваше имя изменено'

            text = f'\U00002705 {text}.'

        elif result == 'not updated':

            if user['lang'] == LANGS[0]:
                text = '\U000026A0 Ismingiz o\'zgartirilmadi'

            if user['lang'] == LANGS[1]:
                text = ' Ваше имя не было изменено'

            text = f'\U000026A0 {text} !'

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang']).get_keyboard()
    update.message.reply_html(get_user_info_layout(user), reply_markup=inline_keyboard)

    return ConversationHandler.END


def change_surname_callback(update: Update, context: CallbackContext):
    surname = update.message.text

    bot_data = context.bot_data
    user = context.bot_data[update.effective_user.id]

    if surname == '/cancel' or surname == '/menu' or surname == '/start':

        if user['lang'] == LANGS[0]:
            text = 'Familyani o\'zgartirish bekor qilindi'

        if user['lang'] == LANGS[1]:
            text = 'Смена фамилии отменена'

        text = f'\U0000274C {text}.'

    else:

        result = update_user_info(user['user_id'], surname=surname)

        if result == 'updated':

            bot_data[update.effective_user.id]['surname'] = surname

            if user['lang'] == LANGS[0]:
                text = 'Familyangiz o\'zgatrilildi'

            if user['lang'] == LANGS[1]:
                text = 'Ваша фамилия изменена'

            text = f'\U00002705 {text}.'

        elif result == 'not updated':

            if user['lang'] == LANGS[0]:
                text = '\U000026A0 Familyangiz o\'zgartirilmadi'

            if user['lang'] == LANGS[1]:
                text = 'Ваше фамилия не было изменено'

            text = f'\U000026A0 {text} !'

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang']).get_keyboard()
    update.message.reply_html(get_user_info_layout(user), reply_markup=inline_keyboard)

    return ConversationHandler.END


def change_phone_callback(update: Update, context: CallbackContext):
    phone_number = update.message.text

    bot_data = context.bot_data
    user = context.bot_data[update.effective_user.id]

    if phone_number == '/cancel' or phone_number == '/menu' or phone_number == '/start':

        if user['lang'] == LANGS[0]:
            text = 'Raqmni o\'zgartirish bekor qilindi'

        if user['lang'] == LANGS[1]:
            text = 'Смена номера отменена'

        text = f'\U0000274C {text}.'

    else:

        phone_number = phone_number_filter(phone_number)

        if phone_number and phone_number != user['phone_number']:

            update_user_info(user['user_id'], phone_number=phone_number)
            bot_data[update.effective_user.id]['phone_number'] = phone_number

            if user['lang'] == LANGS[0]:
                text = 'Telefon raqamingiz o\'zgatrilildi'

            if user['lang'] == LANGS[1]:
                text = 'Ваш номер телефона был изменен'

            text = f'\U00002705 {text}.'

        else:

            if phone_number == user['phone_number']:

                if user['lang'] == LANGS[0]:
                    text = 'Bu raqam ro\'yxatdan o\'tgan !\n\n' \
                           'Boshqa telefon raqamini yuboring.'

                if user['lang'] == LANGS[1]:
                    text = 'Этот номер зарегистрирован !\n\n' \
                           'Отправьте другой номер телефона'

                text = f'\U000026A0 {text}'

            else:

                if user['lang'] == LANGS[0]:
                    text = 'Xato telefon raqami yuborildi'

                if user['lang'] == LANGS[1]:
                    text = 'Отправлен неверный номер телефона'

                text = f'\U000026A0 {text} !'

            reply_text = get_phone_number_layout(user['lang'])

            update.message.reply_text(text, quote=True)
            update.message.reply_html(reply_text)

            return NEW_PHONE_NUMBER

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang']).get_keyboard()
    update.message.reply_html(get_user_info_layout(user), reply_markup=inline_keyboard)

    return ConversationHandler.END


changedataconversation_handler = ConversationHandler(

    entry_points=[CallbackQueryHandler(change_data_callback, pattern='^change')],

    states={

        NEW_NAME: [MessageHandler(Filters.text, change_name_callback)],

        NEW_SURNAME: [MessageHandler(Filters.text, change_surname_callback)],

        NEW_PHONE_NUMBER: [MessageHandler(Filters.text, change_phone_callback)]
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
