from telegram import Update
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler,
                          CallbackContext, Filters, CallbackQueryHandler)
from telegram import ReplyKeyboardRemove, ParseMode
from inlinekeyboards import InlineKeyboard
from filters import *
from replykeyboards import ReplyKeyboard
from DB.main import *
from languages import LANGS
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

SPECIAL_CODE = {}

USER_ID, FIRST_NAME, LAST_NAME, FULL_NAME, LANG, PHONE_NUMBER, CODE, WHO_IS = \
    ('user_id', 'first_name', 'last_name', 'full_name', 'lang', 'phone_number', 'code', 'who_is')


def do_command(update: Update, context: CallbackContext):
    command = update.message.text
    user_input_data = context.user_data

    user_input_data[USER_ID] = update.effective_user.id
    user_input_data[FIRST_NAME] = update.effective_user.first_name
    user_input_data[LAST_NAME] = update.effective_user.last_name

    # logger.info('user_input_data: %s', user_input_data)

    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())

    # print('inside do command')

    user = get_user(update.effective_user.id)

    if command == '/start':

        if user:

            if user['lang'] == LANGS[0]:
                text = "Siz ro'yxatdan o'tgansiz !"

            if user['lang'] == LANGS[1]:
                text = "Вы зарегистрированы !"

            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang'])

            update.message.reply_text(text, reply_markup=reply_keyboard.get_keyboard())

            user_input_data.clear()
            return ConversationHandler.END

        else:

            inline_keyboard = InlineKeyboard('langs_keyboard')
            update.message.reply_text('Tilni tanlang. Выберите язык.', reply_markup=inline_keyboard.get_keyboard())

        return LANG


def text_callback(update: Update, context: CallbackContext):
    # print('inside text_callback')

    # with open('../update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    inline_keyboard = InlineKeyboard('langs_keyboard')

    update.message.reply_text("Avval ro'yxatdan o'ting.\nСначала зарегистрируйтесь.")

    update.message.reply_text('Tilni tanlang. Выберите язык.',
                              reply_markup=inline_keyboard.get_keyboard(),
                              reply_to_message_id=update.message.message_id)

    return LANG


def lang_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    # with open('../update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    #
    # with open('../callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())

    # print('inside lang callback')

    user_input_data = context.user_data
    user_input_data[LANG] = data

    logger.info('user_input_data: %s', user_input_data)

    if data == LANGS[0]:
        text = f'\U0001F44B Salom \n' \
               f"Ism va familyangizni kiriting:\n" \
               f"_*__Misol: Sherzod Esanov__*_"

    if data == LANGS[1]:
        text = f'\U0001F44B Привет \n' \
               f'Ваше имя и фамилия:\n' \
               f'_*__Пример: Шерзод Эсанов__*_'

    callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN_V2)

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

        user_input_data.update({'name': full_name[0]})
        user_input_data.update({'surname': full_name[1]})

        if user_input_data[LANG] == LANGS[0]:
            text = 'Davom etish uchun kontaktingizni yuboring:'

        if user_input_data[LANG] == LANGS[1]:
            text = 'Чтобы продолжить, отправьте свой контакт:'

        reply_keyboard = ReplyKeyboard('phone_number_keyboard', user_input_data[LANG])

        update.message.reply_text(text, reply_markup=reply_keyboard.get_keyboard())

        return PHONE_NUMBER

    else:

        if user_input_data[LANG] == LANGS[0]:
            text = f'Ism va familya xato kiritildi \n' \
                   f'Qaytada quyidagi shaklda kiriting:\n' \
                   f'_*__Misol: Sherzod Esanov__*_'

        if user_input_data[LANG] == LANGS[1]:
            text = f'Имя и фамилия введено неверное \n' \
                   f'Повторно введите имя и фамилия в следующем виде:\n' \
                   f'_*__Пример: Шерзод Эсанов__*_'

        update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_to_message_id=update.message.message_id)

        return FULL_NAME


def phone_number_callback(update: Update, context: CallbackContext):
    global SPECIAL_CODE
    user_input_data = context.user_data

    if update.message.contact:

        phone_number = update.effective_message.contact.phone_number

    else:

        if user_input_data[LANG] == LANGS[0]:
            text = 'Kontaktingizni yuboring !!!'

        if user_input_data[LANG] == LANGS[1]:
            text = 'Отправьте свой контакт !!!'

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return PHONE_NUMBER

    if not phone_number.startswith('+'):
        phone_number = phone_number.rjust(13, '+')

    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())

    user_input_data[PHONE_NUMBER] = phone_number
    # print(user_input_data[PHONE_NUMBER])
    logger.info('user_input_data: %s', user_input_data)

    special_code = random.randint(100000, 999999)

    SPECIAL_CODE[update.effective_user.id] = special_code

    if user_input_data[LANG] == LANGS[0]:
        text = f"Maxsus kod: *`{special_code}`*\n" \
               f"Ushbu kodni botga jo'nating"

    if user_input_data[LANG] == LANGS[1]:
        text = f'Специальный код: *`{special_code}`*\n' \
               f'Отправьте этот код боту'

    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN_V2)

    return CODE


def special_code_callback(update: Update, context: CallbackContext):
    special_code = update.effective_message.text

    user_input_data = context.user_data
    user_input_data[CODE] = special_code
    user_input_data[WHO_IS] = 2

    logger.info('user_input_data: %s', user_input_data)
    logger.info('SPECIAL_CODE: %s', SPECIAL_CODE)

    # with open('../update.json', 'w') as update_file:
    #     update_file.write(update.to_json())

    special_code = special_code_filter(special_code)

    if special_code == SPECIAL_CODE[update.effective_user.id]:

        insert_user(user_input_data)

        if user_input_data[LANG] == LANGS[0]:
            text = "\U0001F44F\U0001F44F\U0001F44F Tabriklaymiz\nSiz registratsiyadan muvofaqqiyatli o'tdingiz"

        if user_input_data[LANG] == LANGS[1]:
            text = "\U0001F44F\U0001F44F\U0001F44F Поздравляем\nВы успешно зарегистрировались"

        reply_keyboard = ReplyKeyboard('menu_keyboard', user_input_data[LANG])

        update.message.reply_text(text, reply_markup=reply_keyboard.get_keyboard())

        user_input_data.clear()
        return ConversationHandler.END

    else:

        if user_input_data[LANG] == LANGS[0]:
            text = "Maxsus kodni xato kiritdingiz.\nKodni qaytadan kiriting !"

        elif user_input_data[LANG] == LANGS[1]:
            text = "Вы ввели специальный код по ошибке.\nВведите код еще раз !"

        update.message.reply_text(text, reply_to_message_id=update.message.message_id)

        return CODE


conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', do_command, filters=~Filters.update.edited_message),
    ],
    states={
        LANG: [CallbackQueryHandler(lang_callback), MessageHandler(Filters.text, text_callback)],

        FULL_NAME: [MessageHandler(Filters.text, full_name_callback)],

        PHONE_NUMBER: [MessageHandler(Filters.contact | Filters.text, phone_number_callback)],

        CODE: [MessageHandler(Filters.text, special_code_callback)],
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
