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

    bot_data = context.bot_data
    user = bot_data['user_data']

    # print('change_name_callback')
    # logger.info('user_input_data: %s', user_input_data)

    # print('inside change name')

    if name == '/cancel' or name == '/menu' or name == '/start':

        if user['lang'] == LANGS[0]:
            text = '\U0000274C Ismni o\'zgrtirish bekor qilindi.'

        if user['lang'] == LANGS[1]:
            text = '\U0000274C Смена имени отменена.'

    else:

        result = update_user_info(user['user_id'], name=name)

        if result == 'updated':
            bot_data['user_data']['name'] = name

            if user['lang'] == LANGS[0]:
                text = '\U00002705 Ismingiz o\'zgatirildi.'

            if user['lang'] == LANGS[1]:
                text = '\U00002705 Ваше имя изменено.'

        elif result == 'not updated':

            if user['lang'] == LANGS[0]:
                text = '\U000026A0 Ismingiz o\'zgartirilmadi !'

            if user['lang'] == LANGS[1]:
                text = '\U000026A0 Ваше имя не было изменено !'

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang']).get_keyboard()
    update.message.reply_html(get_user_info_layout(user), reply_markup=inline_keyboard)

    return ConversationHandler.END


def change_surname_callback(update: Update, context: CallbackContext):
    surname = update.message.text

    bot_data = context.bot_data
    user = bot_data['user_data']

    # print('change_surname_callback')
    # logger.info('user_input_data: %s', user_input_data)

    if surname == '/cancel' or surname == '/menu' or surname == '/start':
        if user['lang'] == LANGS[0]:
            text = '\U0000274C Familyani o\'zgartirish bekor qilindi.'

        if user['lang'] == LANGS[1]:
            text = '\U0000274C Смена фамилии отменена'

    else:
        result = update_user_info(user['user_id'], surname=surname)

        if result == 'updated':
            bot_data['user_data']['surname'] = surname

            if user['lang'] == LANGS[0]:
                text = '\U00002705 Familyangiz o\'zgatrilildi.'

            if user['lang'] == LANGS[1]:
                text = '\U00002705 Ваша фамилия изменена.'

        elif result == 'not updated':
            if user['lang'] == LANGS[0]:
                text = '\U000026A0 Familyangiz o\'zgartirilmadi !'

            if user['lang'] == LANGS[1]:
                text = '\U000026A0 Ваше фамилия не было изменено !'

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang']).get_keyboard()
    update.message.reply_html(get_user_info_layout(user), reply_markup=inline_keyboard)

    return ConversationHandler.END


def change_phone_callback(update: Update, context: CallbackContext):
    phone_number = update.message.text

    bot_data = context.bot_data
    user = bot_data['user_data']

    if phone_number == '/cancel' or phone_number == '/menu' or phone_number == '/start':

        if user['lang'] == LANGS[0]:
            text = '\U0000274C Raqmni o\'zgartirish bekor qilindi.'

        if user['lang'] == LANGS[1]:
            text = '\U0000274C Смена номера отменена.'

    else:

        phone_number = phone_number_filter(phone_number)

        if phone_number and phone_number != user['phone_number']:

            update_user_info(user['user_id'], phone_number=phone_number)
            bot_data['user_data']['phone_number'] = phone_number

            if user['lang'] == LANGS[0]:
                text = '\U00002705 Telefon raqamingiz o\'zgatrilildi.'

            if user['lang'] == LANGS[1]:
                text = '\U00002705 Ваш номер телефона был изменен.'

        else:

            if phone_number == user['phone_number']:

                if user['lang'] == LANGS[0]:
                    text = '\U000026A0 Bu raqam ro\'yxatdan o\'tgan !\n\n' \
                           'Boshqa telefon raqamini yuboring.'

                if user['lang'] == LANGS[1]:
                    text = '\U000026A0 Этот номер зарегистрирован !\n\n' \
                           'Отправьте другой номер телефона.'

            else:
                if user['lang'] == LANGS[0]:
                    text = '\U000026A0 Xato telefon raqami yuborildi !'

                if user['lang'] == LANGS[1]:
                    text = '\U000026A0 Отправлен неверный номер телефона !'

            phone_number_layout = get_phone_number_layout(user['lang'])

            update.message.reply_text(text, quote=True)
            update.message.reply_html(phone_number_layout)

            return NEW_PHONE_NUMBER

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang']).get_keyboard()
    update.message.reply_html(get_user_info_layout(user), reply_markup=inline_keyboard)

    return ConversationHandler.END


def change_data_callback(update: Update, context: CallbackContext):
    # print('changa data callback')
    callback_query = update.callback_query
    data = callback_query.data

    bot_data = context.bot_data

    if not bot_data:
        user_data = get_user(update.effective_user.id)
        bot_data['user_data'] = user_data

    user = bot_data['user_data']

    if data == BUTTONS_DATA_DICT[3] or data == BUTTONS_DATA_DICT[4]:

        if data == BUTTONS_DATA_DICT[3]:

            if user['lang'] == LANGS[0]:
                text = '<i>Ismni o\'zgartirish</i>'
                phone_number_layout = 'Ismningizni yuboring:'

            if user['lang'] == LANGS[1]:
                text = '<i>Изменить имя</i>'
                phone_number_layout = 'Отправьте ваше имя:'

            state = NEW_NAME

        if data == BUTTONS_DATA_DICT[4]:

            if user['lang'] == LANGS[0]:
                text = '<i>Familyani o\'zgartirish</i>'
                phone_number_layout = 'Familyangizni yuboring:'

            if user['lang'] == LANGS[1]:
                text = '<i>Изменить фамилию</i>'
                phone_number_layout = 'Отправьте свою фамилию:'

            state = NEW_SURNAME

    if data == BUTTONS_DATA_DICT[5]:

        if user['lang'] == LANGS[0]:
            text = '<i>Telefon raqamini o\'zgartirish</i>'

        if user['lang'] == LANGS[1]:
            text = '<i>Изменить номер телефона</i>'

        state = NEW_PHONE_NUMBER

        phone_number_layout = get_phone_number_layout(user['lang'])

    callback_query.edit_message_text(text, parse_mode=ParseMode.HTML)
    callback_query.message.reply_html(phone_number_layout)

    return state


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
