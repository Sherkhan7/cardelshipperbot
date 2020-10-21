from telegram import Update
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler,
                          CallbackContext, Filters, CallbackQueryHandler)
from telegram import ReplyKeyboardRemove
from inlinekeyboards import InlineKeyboard
from filters import *
from replykeyboards import ReplyKeyboard
from DB import insert_user
from helpers import set_user_data_in_bot_data
from languages import LANGS
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

SPECIAL_CODE = {}

USER_ID, FIRST_NAME, LAST_NAME, FULL_NAME, LANG, PHONE_NUMBER, CODE, WHO_IS = \
    ('user_id', 'first_name', 'last_name', 'full_name', 'lang', 'phone_number', 'code', 'who_is')


def do_command(update: Update, context: CallbackContext):
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    command = update.message.text

    user_input_data = context.user_data
    bot_data = context.bot_data

    # set bot_data[update.effective_user.id] -> dict
    set_user_data_in_bot_data(update.effective_user.id, bot_data)
    user = bot_data[update.effective_user.id]

    # logger.info('user_input_data: %s', user_input_data)

    if command == '/start':

        if user:

            if user['lang'] == LANGS[0]:
                text = 'Siz ro\'yxatdan o\'tgansiz !'

            if user['lang'] == LANGS[1]:
                text = 'Вы зарегистрированы !'

            text = '\U000026A0 ' + text
            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang']).get_keyboard()

            update.message.reply_text(text, reply_markup=reply_keyboard)

            return ConversationHandler.END

        else:

            user_input_data[USER_ID] = update.effective_user.id
            user_input_data[FIRST_NAME] = update.effective_user.first_name
            user_input_data[LAST_NAME] = update.effective_user.last_name

            inline_keyboard = InlineKeyboard('langs_keyboard').get_keyboard()
            update.message.reply_text('Tilni tanlang. Выберите язык.', reply_markup=inline_keyboard)

        return LANG


def lang_callback(update: Update, context: CallbackContext):
    # with open('../update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    #
    # with open('../callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user_input_data[LANG] = data

    logger.info('user_input_data: %s', user_input_data)

    if data == LANGS[0]:
        edit_text = 'Til: \U0001F1FA\U0001F1FF'
        text = 'Salom !\n' \
               'Ism va familyangizni yuboring:\n\n' \
               '<b><i><u>Misol: Sherzod Esanov</u></i></b>'

    if data == LANGS[1]:
        edit_text = 'Язык: \U0001F1F7\U0001F1FA'
        text = 'Привет !\n' \
               'Отправьте свое имя и фамилию:\n\n' \
               '<b><i><u>Пример: Шерзод Эсанов</u></i></b>'

    text = '\U0001F44B ' + text

    callback_query.edit_message_text(edit_text)
    callback_query.message.reply_html(text)

    return FULL_NAME


def full_name_callback(update: Update, context: CallbackContext):
    # print('full_name_callback')
    # with open('../update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    text = update.message.text
    user_input_data = context.user_data

    logger.info('user_input_data: %s', user_input_data)

    full_name = full_name_filter(text)

    if full_name:

        user_input_data['name'] = full_name[0]
        user_input_data['surname'] = full_name[1]

        if user_input_data[LANG] == LANGS[0]:
            text = 'Davom etish uchun kontaktingizni yuboring:'

        if user_input_data[LANG] == LANGS[1]:
            text = 'Чтобы продолжить, отправьте свой контакт:'

        reply_keyboard = ReplyKeyboard('phone_number_keyboard', user_input_data[LANG]).get_keyboard()

        update.message.reply_text(text, reply_markup=reply_keyboard)

        return PHONE_NUMBER

    else:

        if user_input_data[LANG] == LANGS[0]:
            text = 'Ism va familya xato yuborildi !\n' \
                   'Qaytada quyidagi shaklda yuboring:\n\n' \
                   '<b><i><u>Misol: Sherzod Esanov</u></i></b>'

        if user_input_data[LANG] == LANGS[1]:
            text = 'Имя и фамилия введено неверное !\n' \
                   'Повторно введите имя и фамилия в следующем виде:\n\n' \
                   '<b><i><u>Пример: Шерзод Эсанов</u></i></b>'

        text = '\U000026A0 ' + text
        update.message.reply_html(text, quote=True)

        return FULL_NAME


def phone_number_callback(update: Update, context: CallbackContext):
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    global SPECIAL_CODE
    user_input_data = context.user_data

    if update.message.contact:

        phone_number = update.effective_message.contact.phone_number

        if not phone_number.startswith('+'):
            phone_number = phone_number.rjust(13, '+')

    else:

        if user_input_data[LANG] == LANGS[0]:
            text = 'Kontaktingizni yuboring'

        if user_input_data[LANG] == LANGS[1]:
            text = 'Отправьте свой контакт'

        text = f'\U000026A0 {text} !'
        update.message.reply_text(text, quote=True)

        return PHONE_NUMBER

    user_input_data[PHONE_NUMBER] = phone_number
    logger.info('user_input_data: %s', user_input_data)

    special_code = random.randint(100000, 999999)

    SPECIAL_CODE[update.effective_user.id] = special_code

    if user_input_data[LANG] == LANGS[0]:
        text = f'Maxsus kod: <pre><i>{special_code}</i></pre>\n' \
               f'Ushbu kodni menga yuboring.'

    if user_input_data[LANG] == LANGS[1]:
        text = f'Специальный код: <pre><i>{special_code}</i></pre>\n' \
               f'Отправьте мне этот код.'

    update.message.reply_html(text, reply_markup=ReplyKeyboardRemove())

    return CODE


def special_code_callback(update: Update, context: CallbackContext):
    # with open('../update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    special_code = update.effective_message.text

    user_input_data = context.user_data
    bot_data = context.bot_data

    user_input_data[CODE] = special_code
    logger.info('user_input_data: %s', user_input_data)
    logger.info('SPECIAL_CODE: %s', SPECIAL_CODE)

    special_code = special_code_filter(special_code)

    if special_code == SPECIAL_CODE[update.effective_user.id]:

        insert_user(user_input_data)
        set_user_data_in_bot_data(update.effective_user.id, bot_data)

        if user_input_data[LANG] == LANGS[0]:
            text = 'Tabriklaymiz !\n\n' \
                   'Siz registratsiyadan muvofaqqiyatli o\'tdingiz.'

        if user_input_data[LANG] == LANGS[1]:
            text = 'Поздравляем !\n\n' \
                   'Вы успешно зарегистрировались'

        text = '\U0001F44F\U0001F44F\U0001F44F ' + text
        reply_keyboard = ReplyKeyboard('menu_keyboard', user_input_data[LANG]).get_keyboard()

        update.message.reply_text(text, reply_markup=reply_keyboard)

        user_input_data.clear()
        return ConversationHandler.END

    else:

        if user_input_data[LANG] == LANGS[0]:
            text = 'Maxsus kodni xato kiritdingiz !\n\n' \
                   'Kodni qaytadan yuboring.'

        elif user_input_data[LANG] == LANGS[1]:
            text = 'Вы ввели специальный код по ошибке !\n\n' \
                   'Введите код еще раз.'

        text = '\U000026A0 ' + text
        update.message.reply_text(text, quote=True)

        return CODE


conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', do_command, filters=~Filters.update.edited_message),
    ],
    states={
        LANG: [CallbackQueryHandler(lang_callback)],

        FULL_NAME: [MessageHandler(Filters.text, full_name_callback)],

        PHONE_NUMBER: [MessageHandler(Filters.contact | Filters.text, phone_number_callback)],

        CODE: [MessageHandler(Filters.text, special_code_callback)],
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
