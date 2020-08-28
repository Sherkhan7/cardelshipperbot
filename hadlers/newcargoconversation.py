from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from telegram.ext import (MessageHandler, ConversationHandler,
                          CallbackQueryHandler, CallbackContext, Filters, )
from inlinekeyboards import InlineKeyboard
from DB.main import *
from languages import LANGS
from buttonsdatadict import BUTTONS_DATA_DICT
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

USER_ID, REGION, DISTRICT, LOCATION = \
    ('user_id', 'region', 'district', 'location')


def region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    user_input_data = context.user_data

    data = callback_query.data
    user_input_data['region'] = data

    user = get_user(update.effective_user.id)
    # print('regions callback')
    # print(callback_query.data)
    region_id = int(data.replace("region_id_", ""))

    if data == BUTTONS_DATA_DICT['regions'][region_id]:
        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('districts_keyboard', LANGS[0], region_id)
            callback_query.edit_message_text("Tumaningizni tanlang:")
            callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())
        elif user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('districts_keyboard', LANGS[1], region_id)
            callback_query.edit_message_text("Выберите свой район:")
            callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

    return DISTRICT


def district_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    user_input_data = context.user_data
    user_input_data['district'] = data

    user = get_user(update.effective_user.id)
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())

    # print('district callback')
    # print(callback_query.data)
    if user['lang'] == LANGS[0]:
        callback_query.edit_message_text('Lokatsiyani yuborish:')

        reply_keyboard = ReplyKeyboardMarkup([
            [KeyboardButton("\U0001F4CD Lokatsiyamni jo'natish", request_location=True)]],
            resize_keyboard=True)
        callback_query.message.reply_text("Bu bosqichni o'tkazib yuborish uchun /skip ni bosing.",
                                          reply_markup=reply_keyboard)

    if user['lang'] == LANGS[1]:
        callback_query.edit_message_text('Отправить местоположение:')

        reply_keyboard = ReplyKeyboardMarkup([
            [KeyboardButton("\U0001F4CD Отправить мое местоположение", request_location=True)]],
            resize_keyboard=True)
        callback_query.message.reply_text("Нажмите /skip, чтобы пропустить этот шаг",
                                          reply_markup=reply_keyboard)

    return LOCATION


def location_callback(update: Update, context: CallbackContext):
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())

    print('location_callback')
    update.message.reply_text('Tugatildi', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def text_callback(update: Update, context: CallbackContext):
    print('text callback text callback text callback')


def new_cargo_conversation_callback(update: Update, context: CallbackContext):
    # print('new caro conversation starter')
    user = get_user(update.effective_user.id)

    callback_query = update.callback_query
    data = callback_query.data

    if data == BUTTONS_DATA_DICT[2]:

        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('regions_keyboard', LANGS[0])

            callback_query.edit_message_text("Viloyatingizni tanlang:")
            callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

        if user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('regions_keyboard', LANGS[1])

            callback_query.edit_message_text("Выберите свой область:")
            callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

    return REGION


def text_callback_in_region(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)

    if text == '/start' or text == '/menu':

        if user['lang'] == LANGS[0]:
            inlinekeyboard = InlineKeyboard('main_keyboard', LANGS[0])
            update.message.reply_text('Bekor qilindi!', reply_markup=inlinekeyboard.get_keyboard())

        if user['lang'] == LANGS[1]:
            inlinekeyboard = InlineKeyboard('main_keyboard', LANGS[1])
            update.message.reply_text('Отменено!', reply_markup=inlinekeyboard.get_keyboard())

    else:

        if user['lang'] == LANGS[0]:
            inlinekeyboard = InlineKeyboard('main_keyboard', LANGS[0])
            update.message.reply_text('Bekor qilindi !', reply_markup=inlinekeyboard.get_keyboard(),
                                      reply_to_message_id=update.message.message_id)

        if user['lang'] == LANGS[1]:
            inlinekeyboard = InlineKeyboard('main_keyboard', LANGS[1])
            update.message.reply_text('Отменено!', reply_markup=inlinekeyboard.get_keyboard(),
                                      reply_to_message_id=update.message.message_id)

    return ConversationHandler.END


new_cargo_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(new_cargo_conversation_callback, pattern='^new')],
    states={
        REGION: [CallbackQueryHandler(region_callback, '^region'),
                 MessageHandler(Filters.text, text_callback_in_region)],
        DISTRICT: [CallbackQueryHandler(district_callback, '^district'),
                   MessageHandler(Filters.text, text_callback_in_district)],
        LOCATION: [MessageHandler(Filters.location | Filters.text, location_callback)],
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
