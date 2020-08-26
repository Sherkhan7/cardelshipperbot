from telegram import Update
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler,
                          CallbackContext, Filters, CallbackQueryHandler)
from telegram import ReplyKeyboardRemove, ParseMode
from inlinekeyboards import lang_inlinekeyboard
from inlinekeyboards import InlineKeyboard
from filters import *
from replykeyboards import replykeyboard_uz, replykeyboard_ru
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
    # logger.info('user: %s', user)
    # print('after', connection.is_connected())

    if command == '/start':

        if user:

            if user['lang'] == LANGS[0]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])

                update.message.reply_text("Siz ro'yxatdan o'tgansiz !",
                                          reply_markup=inline_keyboard.get_keyboard())
            elif user['lang'] == LANGS[1]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])

                update.message.reply_text("Вы зарегистрированы !",
                                          reply_markup=inline_keyboard.get_keyboard())

            return ConversationHandler.END

        update.message.reply_text('Tilni tanlang. Выберите язык.',
                                  reply_markup=lang_inlinekeyboard)
        return LANG


def text_callback(update: Update, context: CallbackContext):
    # print('inside text_callback')
    with open('../update.json', 'w') as update_file:
        update_file.write(update.to_json())

    text = update.message.text

    if text == '/start':
        update.message.reply_text('Tilni tanlang. Выберите язык.',
                                  reply_markup=lang_inlinekeyboard)

    elif text == '/menu':
        update.message.reply_text("Avval ro'yxatdan o'ting.\nСначала зарегистрируйтесь.")

        update.message.reply_text('Tilni tanlang. Выберите язык.',
                                  reply_markup=lang_inlinekeyboard)

    else:
        update.message.reply_text("Avval ro'yxatdan o'ting.\nСначала зарегистрируйтесь.")

        update.message.reply_text('Tilni tanlang. Выберите язык.',
                                  reply_markup=lang_inlinekeyboard)
    return LANG


def lang_callback(update: Update, context: CallbackContext):
    # print('inside lang callback')
    callback_query = update.callback_query

    with open('../update.json', 'w') as update_file:
        update_file.write(update.to_json())

    with open('../callback_query.json', 'w') as callback_query_file:
        callback_query_file.write(callback_query.to_json())

    data = callback_query.data

    user_input_data = context.user_data
    user_input_data[LANG] = data
    logger.info('user_input_data: %s', user_input_data)

    if data == LANGS[0]:

        callback_query.edit_message_text(f'\U0001F44B Salom \n'
                                         f"Ism va familyangizni kiriting:\n"
                                         f"*__Misol: Esanov Sherzod__*",
                                         parse_mode=ParseMode.MARKDOWN_V2)
    elif data == LANGS[1]:

        callback_query.edit_message_text(f'\U0001F44B  Привет \n'
                                         f'Ваше имя и фамилия:\n'
                                         f'*__Пример: Эсанов Шерзод__*',
                                         parse_mode=ParseMode.MARKDOWN_V2)
    return FULL_NAME


def full_name_callback(update: Update, context: CallbackContext):
    print('full_name_callback')
    with open('../update.json', 'w') as update_file:
        update_file.write(update.to_json())

    full_name = update.message.text
    user_input_data = context.user_data
    user_input_data[FULL_NAME] = full_name
    logger.info('user_input_data: %s', user_input_data)

    full_name = full_name_filter(full_name, user_input_data)

    if full_name == '/start' or full_name == '/menu':

        if user_input_data[LANG] == LANGS[0]:
            update.message.reply_text(f'Ism va familya xato kiritildi \n'
                                      f'Qaytada quyidagi shaklda kiriting:\n'
                                      f'*__Misol: Esanov Sherzod__*',
                                      parse_mode=ParseMode.MARKDOWN_V2,
                                      reply_to_message_id=update.message.message_id)

        elif user_input_data[LANG] == LANGS[1]:
            update.message.reply_text(f'Имя и фамилия введено неверное \n'
                                      f'Повторно введите имя и фамилия в следующем виде:\n'
                                      f'*__Пример: Эсанов Шерзод__*',
                                      parse_mode=ParseMode.MARKDOWN_V2,
                                      reply_to_message_id=update.message.message_id)

        return FULL_NAME

    elif full_name:
        user_input_data.update({'name': full_name[0]})
        user_input_data.update({'surname': full_name[1]})

        if user_input_data[LANG] == LANGS[0]:
            update.message.reply_text(f'Davom etish uchun kontaktingizni yuboring:',
                                      reply_markup=replykeyboard_uz)

        elif user_input_data[LANG] == LANGS[1]:
            update.message.reply_text(f'Чтобы продолжить, отправьте свой контакт:',
                                      reply_markup=replykeyboard_ru)

        return PHONE_NUMBER
    else:
        if user_input_data[LANG] == LANGS[0]:
            update.message.reply_text(f'Ism va familya xato kiritildi \n'
                                      f'Qaytada quyidagi shaklda kiriting:\n'
                                      f'*__Misol: Esanov Sherzod__*',
                                      parse_mode=ParseMode.MARKDOWN_V2,
                                      reply_to_message_id=update.message.message_id)

        elif user_input_data[LANG] == LANGS[1]:
            update.message.reply_text(f'Имя и фамилия введено неверное \n'
                                      f'Повторно введите имя и фамилия в следующем виде:\n'
                                      f'*__Пример: Эсанов Шерзод__*',
                                      parse_mode=ParseMode.MARKDOWN_V2,
                                      reply_to_message_id=update.message.message_id)
        return FULL_NAME


def phone_number_callback(update: Update, context: CallbackContext):
    contact = update.effective_message.contact
    global SPECIAL_CODE

    user_input_data = context.user_data
    user_input_data[PHONE_NUMBER] = contact.phone_number
    logger.info('user_input_data: %s', user_input_data)

    with open('../update.json', 'w') as update_file:
        update_file.write(update.to_json())

    special_code = random.randint(100000, 999999)

    SPECIAL_CODE[update.effective_user.id] = special_code

    if user_input_data[LANG] == LANGS[0]:
        update.message.reply_text(f'Maxsus kod: *`{special_code}`*\n'
                                  f"Ushbu kodni botga jo'nating",
                                  reply_markup=ReplyKeyboardRemove(),
                                  parse_mode=ParseMode.MARKDOWN_V2)
        return CODE

    elif user_input_data[LANG] == LANGS[1]:
        update.message.reply_text(f'Специальный код: *`{special_code}`*\n'
                                  f'Отправьте этот код боту',
                                  reply_markup=ReplyKeyboardRemove(),
                                  parse_mode=ParseMode.MARKDOWN_V2)
        return CODE


def special_code_callback(update: Update, context: CallbackContext):
    special_code = update.effective_message.text

    user_input_data = context.user_data
    user_input_data[CODE] = special_code
    user_input_data[WHO_IS] = 2

    logger.info('user_input_data: %s', user_input_data)
    logger.info('SPECIAL_CODE: %s', SPECIAL_CODE)

    with open('../update.json', 'w') as update_file:
        update_file.write(update.to_json())

    special_code = special_code_filter(special_code)

    if special_code == SPECIAL_CODE[update.effective_user.id]:

        result = insert_user(user_input_data)

        if not result:
            update.message.reply_text('Error !!!')

            return ConversationHandler.END

        if user_input_data[LANG] == LANGS[0]:
            inline_keyboard = InlineKeyboard('main_keyboard', LANGS[0])

            update.message.reply_text(
                "Tabriklaymiz, siz registratsiyadan muvofaqqiyatli o'tdingiz\n\U0001F44F\U0001F44F\U0001F44F",
                reply_markup=inline_keyboard.get_keyboard())

            return ConversationHandler.END

        elif user_input_data[LANG] == LANGS[1]:
            inline_keyboard = InlineKeyboard('main_keyboard', LANGS[1])

            update.message.reply_text(
                "Поздравляем, вы успешно зарегистрировались\n\U0001F44F\U0001F44F\U0001F44F",
                reply_markup=inline_keyboard.get_keyboard())

            return ConversationHandler.END

    else:

        if user_input_data[LANG] == LANGS[0]:
            update.message.reply_text("Maxsus kodni xato kiritdingiz.\nKodni qaytadan kiriting !",
                                      reply_to_message_id=update.message.message_id)

        elif user_input_data[LANG] == LANGS[1]:
            update.message.reply_text("Вы ввели специальный код по ошибке.\nВведите код еще раз !",
                                      reply_to_message_id=update.message.message_id)

        return CODE


# def do_cancel(update: Update, context: CallbackContext):
#     update.message.reply_text('Bekor qilindi', reply_markup=ReplyKeyboardRemove())
#
#     return ConversationHandler.END


conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', do_command, filters=~Filters.update.edited_message),
    ],
    states={
        LANG: [CallbackQueryHandler(lang_callback), MessageHandler(Filters.text, text_callback)],

        FULL_NAME: [MessageHandler(Filters.text, full_name_callback)],

        PHONE_NUMBER: [MessageHandler(Filters.contact, phone_number_callback)],

        CODE: [MessageHandler(Filters.text, special_code_callback)],
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
