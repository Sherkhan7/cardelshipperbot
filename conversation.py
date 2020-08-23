from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler,
                          CallbackQueryHandler, CallbackContext, Filters, )
from inlinekeyboard import inlinekeyboard
from DB.main import *
from replykeyboard import *
from menu import *
import logging
import random
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

SPECIAL_CODE = {}

USER_ID, FIRST_NAME, LAST_NAME, LANG, NAME, SURNAME, PHONE_NUMBER, CODE, WHO_IS = \
    ('user_id', 'first_name', 'last_name', 'lang', 'name', 'surname', 'phone_number', 'code', 'who_is')


def do_command(update: Update, context: CallbackContext):
    command = update.message.text

    user_input_data = context.user_data
    user_input_data[USER_ID] = update.effective_user.id
    user_input_data[FIRST_NAME] = update.effective_user.first_name
    user_input_data[LAST_NAME] = update.effective_user.last_name
    logger.info('user_input_data: %s', user_input_data)

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    # print('pre', conn.is_connected())
    user = get_user(update.effective_user.id)
    # print('after', conn.is_connected())

    if command == '/start':

        if user:
            update.message.reply_text("Siz ro'yxatdan o'tgansiz !.\nВы зарегистрированы !")

            return ConversationHandler.END

        update.message.reply_text('Tilni tanlang. Выберите язык.',
                                  reply_markup=inlinekeyboard)

        return LANG

    if command == '/menu':
        if user:
            user = get_user(update.effective_user.id)
            user = json.loads(user)
            if user['lang'] == 'uzbek':
                update.message.reply_text("MENU", reply_markup=menu_uz)
                return ConversationHandler.END
            elif user['lang'] == 'russian':
                update.message.reply_text("MENU", reply_markup=menu_ru)
                return ConversationHandler.END
        else:
            update.message.reply_text("MENU_ERROR")
            return ConversationHandler.END


def lang_callback_handler(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user_input_data[LANG] = data
    logger.info('user_input_data: %s', user_input_data)

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    with open('callback_query.json', 'w') as callback_query_file:
        callback_query_file.write(callback_query.to_json())

    if data == 'uzbek':

        # callback_query.edit_message_reply_markup(
        # InlineKeyboardMarkup([[InlineKeyboardButton('test', callback_data='test_data')]])
        # )
        # callback_query.message.reply_text(f'Davom etish uchun menga kontaktingizni yuboring \U0001F60A',
        #                                   reply_markup=reply_keyboard_markup)

        callback_query.edit_message_text(f'\U0001F44B Salom, {update.effective_user.first_name}\n'
                                         f"To'liq Ismingiz: \U0001F60A")

        return NAME
    elif data == 'russian':
        callback_query.edit_message_text(f'\U0001F44B  Привет, {update.effective_user.first_name}\n'
                                         f'Ваше полное имя:  \U0001F60A')

        return NAME


def name_handler_callback(update: Update, context: CallbackContext):
    name = update.effective_message.text

    if update.message.text == '/star':
        return LANG

    user_input_data = context.user_data
    user_input_data[NAME] = name
    logger.info('user_input_data: %s', user_input_data)

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    if user_input_data[LANG] == 'uzbek':
        update.message.reply_text(f'Familyangiz:')

        return SURNAME
    elif user_input_data[LANG] == 'russian':
        update.message.reply_text(f'Ваше фамилия:')

        return SURNAME


def surname_handler_callback(update: Update, context: CallbackContext):
    surname = update.effective_message.text

    user_input_data = context.user_data
    user_input_data[SURNAME] = surname
    logger.info('user_input_data: %s', user_input_data)

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    if user_input_data[LANG] == 'uzbek':
        update.message.reply_text(f'Davom etish uchun kontaktingizni yuboring:',
                                  reply_markup=replykeyboard_uzb)

        return PHONE_NUMBER

    elif user_input_data[LANG] == 'russian':
        update.message.reply_text(f'Чтобы продолжить, отправьте свой контакт:',
                                  reply_markup=replykeyboard_russ)

        return PHONE_NUMBER


def phone_number_callback(update: Update, context: CallbackContext):
    contact = update.effective_message.contact
    global SPECIAL_CODE

    user_input_data = context.user_data
    user_input_data[PHONE_NUMBER] = contact.phone_number
    logger.info('user_input_data: %s', user_input_data)

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    special_code = random.randint(100000, 999999)

    SPECIAL_CODE[update.effective_user.id] = special_code

    if user_input_data[LANG] == 'uzbek':
        update.message.reply_text(f'Maxsus kod: {special_code}\n'
                                  f"Ushbu kodni botga jo'nating",
                                  reply_markup=ReplyKeyboardRemove())

        return CODE

    elif user_input_data[LANG] == 'russian':
        update.message.reply_text(f'Специальный код: {special_code}\n'
                                  f'Отправьте этот код боту',
                                  reply_markup=ReplyKeyboardRemove()
                                  )

        return CODE


def secret_code_callback(update: Update, context: CallbackContext):
    special_code = update.effective_message.text

    user_input_data = context.user_data
    user_input_data[CODE] = special_code
    user_input_data[WHO_IS] = 's'

    logger.info('user_input_data: %s', user_input_data)
    logger.info('SPECIAL_CODE: %s', SPECIAL_CODE)

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    if int(special_code) == SPECIAL_CODE[update.effective_user.id]:

        result = insert(user_input_data)

        if not result:
            update.message.reply_text('Error !!!')

            return ConversationHandler.END

        if user_input_data[LANG] == 'uzbek':

            update.message.reply_text(
                "Tabriklaymiz, siz registratsiyadan muvofaqqiyatli o'tdingiz\n\U0001F44F\U0001F44F\U0001F44F",
                reply_markup=menu_uz)

            return ConversationHandler.END

        elif user_input_data[LANG] == 'russian':
            update.message.reply_text(
                "Поздравляем, вы успешно зарегистрировались\n\U0001F44F\U0001F44F\U0001F44F",
                reply_markup=menu_ru)

            return ConversationHandler.END
    else:
        if user_input_data[LANG] == 'uzbek':
            update.message.reply_text("Maxsus kodni xato kiritdingiz.\nKodni qaytadan kiriting !")
            return CODE

        elif user_input_data[LANG] == 'russian':
            update.message.reply_text("Вы ввели специальный код по ошибке.\nВведите код еще раз !")
            return CODE


def do_cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Bekor qilindi', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler(['start', 'menu'], do_command, filters=~Filters.update.edited_message)
    ],
    states={
        LANG: [CallbackQueryHandler(lang_callback_handler)],
        NAME: [MessageHandler(Filters.text & ~Filters.command, name_handler_callback)],
        SURNAME: [MessageHandler(Filters.text & ~Filters.command, surname_handler_callback)],
        PHONE_NUMBER: [MessageHandler(Filters.contact, phone_number_callback)],
        CODE: [MessageHandler(Filters.text & ~Filters.command, secret_code_callback)],
    },
    fallbacks=[
        CommandHandler('cancel', do_cancel)
    ]
)
