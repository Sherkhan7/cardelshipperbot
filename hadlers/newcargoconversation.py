from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove, ParseMode
from telegram.ext import (MessageHandler, ConversationHandler, CallbackQueryHandler, CallbackContext, Filters)
from inlinekeyboards import InlineKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from filters import phone_number_filter
from replykeyboards import ReplyKeyboard
from layouts import *
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def from_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)
    user_input_data = context.user_data
    # print('regions callback')
    # print(callback_query.data)
    region_id = int(data.replace("region_id_", ""))
    user_input_data[FROM_REGION] = region_id

    logger.info('new_cargo_info: %s', user_input_data)

    if data == BUTTONS_DATA_DICT['regions'][region_id]:

        if user['lang'] == LANGS[0]:
            text = "Tumaningizni tanlang:"

        if user['lang'] == LANGS[1]:
            text = "Выберите свой район:"

        inline_keyboard = InlineKeyboard('districts_keyboard', user['lang'], region_id)
        callback_query.edit_message_text(text, reply_markup=inline_keyboard.get_keyboard())

    user_input_data['state'] = FROM_DISTRICT
    return FROM_DISTRICT


def from_district_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())

    # print('district callback')

    if data == BUTTONS_DATA_DICT[6]:

        if user['lang'] == LANGS[0]:
            text = "Viloyatingizni tanlang:"

        if user['lang'] == LANGS[1]:
            text = "Выберите свой область:"

        inline_keyboard = InlineKeyboard('regions_keyboard', user['lang'])
        callback_query.edit_message_text(text, reply_markup=inline_keyboard.get_keyboard())

        user_input_data['state'] = FROM_REGION
        return FROM_REGION

    district_id = int(data.replace("district_id_", ""))
    user_input_data[FROM_DISTRICT] = district_id

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        edit_message_text = 'Geolokatsiyangizni yuboring:'
        button_text = "\U0001F4CD Geolokatsiyamni jo'natish"
        reply_text = "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

    if user['lang'] == LANGS[1]:
        edit_message_text = 'Отправьте свою геолокацию:'
        button_text = "\U0001F4CD Отправить мою геолокацию"
        reply_text = "Или нажмите «next», чтобы пропустить этот шаг"

    reply_keyboard = ReplyKeyboardMarkup([
        [KeyboardButton(button_text, request_location=True)],
        [KeyboardButton('«next»')]
    ], resize_keyboard=True)

    callback_query.edit_message_text(edit_message_text)
    callback_query.message.reply_text(reply_text, reply_markup=reply_keyboard)

    user_input_data['state'] = FROM_LOCATION
    return FROM_LOCATION


def from_location_callback(update: Update, context: CallbackContext):
    # print(location)
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if update.message.location:

        longitude = update.message.location.longitude
        latitude = update.message.location.latitude

        user_input_data['from_location'] = {
            'longitude': longitude,
            'latitude': latitude
        }

    elif update.message.text == '«next»':

        user_input_data['from_location'] = {
            'longitude': None,
            'latitude': None
        }
    else:
        if user['lang'] == LANGS[0]:
            text = 'Geolokatsiyangizni yuboring yoki «next» ni bosing:'

        if user['lang'] == LANGS[1]:
            text = 'Укажите свою геолокацию или нажмите «next»:'

        update.message.reply_text(text, quote=True)

        return FROM_LOCATION

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text_1 = '2-Bosqich.'
        text_2 = "Yukni jo'natish manzilini tanlang:"

    if user['lang'] == LANGS[1]:
        text_1 = 'Шаг 2'
        text_2 = "Выберите адрес доставки:"

    update.message.reply_text(text_1, reply_markup=ReplyKeyboardRemove())
    inline_keyboard = InlineKeyboard('regions_keyboard', user['lang'])
    update.message.reply_text(text_2, reply_markup=inline_keyboard.get_keyboard())

    user_input_data['state'] = TO_REGION
    return TO_REGION


def get_skip_keyboard(state):
    # if lang == LANGS[0]:
    #     button_text = 'keyingisi'
    #
    # if lang == LANGS[1]:
    #     button_text = 'следующий'

    if state == TO_LOCATION:
        data = 'skip_to_location'

    if state == WEIGHT:
        data = 'skip_weight'

    if state == VOLUME:
        data = 'skip_volume'

    if state == DEFINITION:
        data = 'skip_definition'

    if state == PHOTO:
        data = 'skip_photo'

    if state == RECEIVER_PHONE_NUMBER:
        data = 'skip_receiver_phone'

    return InlineKeyboardMarkup([
        [InlineKeyboardButton('«next»', callback_data=data)]
    ])


def skip_callback_in_to_location(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if user_input_data['state'] == TO_LOCATION:
        user_input_data[TO_LOCATION] = {
            'longitude': None,
            'latitude': None
        }

        if user['lang'] == LANGS[0]:
            text = "3-Bosqich."
            reply_text = "Yuk og'irligini tanlang:"
            button1_text = UNITS['uz'][0]
            button2_text = UNITS['uz'][1]

        if user['lang'] == LANGS[1]:
            text = "Шаг 3."
            reply_text = "Выберите вес груза:"
            button1_text = UNITS['ru'][0]
            button2_text = UNITS['ru'][1]

        inline_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='kg'),
                InlineKeyboardButton(button2_text, callback_data='t')
            ]
        ])
        callback_query.edit_message_text(text)
        callback_query.message.reply_text(reply_text, reply_markup=inline_keyboard)

        user_input_data['state'] = WEIGHT_UNIT
        return WEIGHT_UNIT


def skip_callback_in_weight(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if user_input_data['state'] == WEIGHT:
        user_input_data[WEIGHT] = None

        if user['lang'] == LANGS[0]:
            weight = "noma'lum"
            weight_text = "Yuk og'irligi"
            reply_text = "Yuk hajmini kiriting (raqamda):\n\n" \
                         "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

        if user['lang'] == LANGS[1]:
            weight = "неизвестно"
            weight_text = "Вес груза"
            reply_text = "Введите объем груза (цифрами):\n\n" \
                         "Или нажмите «next», чтобы пропустить этот шаг."

        user_input_data['state'] = VOLUME

        callback_query.edit_message_text(f'{weight_text}: {weight}')
        callback_query.message.reply_text(reply_text, reply_markup=get_skip_keyboard(user_input_data['state']))

        return VOLUME


def skip_callback_in_volume(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if user_input_data['state'] == VOLUME:
        user_input_data[VOLUME] = None

        if user['lang'] == LANGS[0]:
            volume = "noma'lum"
            volume_text = 'Yuk hajmi'

            reply_text = "Yuk tavsifini kiriting:\n\n" \
                         "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

        if user['lang'] == LANGS[1]:
            volume = "неизвестно"
            volume_text = "Объем груза"
            reply_text = "Введите описание груза:\n\n" \
                         "Или нажмите «next», чтобы пропустить этот шаг."

        user_input_data['state'] = DEFINITION

        callback_query.edit_message_text(f'{volume_text}: {volume}')
        callback_query.message.reply_text(reply_text, reply_markup=get_skip_keyboard(user_input_data['state']))
        return DEFINITION


def skip_callback_in_definition(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if user_input_data['state'] == DEFINITION:
        user_input_data[DEFINITION] = None

        if user['lang'] == LANGS[0]:
            definition = "noma'lum"
            definition_text = 'Yuk tasnifi'
            reply_text = "Yuk rasmini yuboring:\n\n" \
                         "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

        if user['lang'] == LANGS[1]:
            definition = "неизвестно"
            definition_text = "Описание груза"
            reply_text = "Отправите фотография груза:\n\n" \
                         "Или нажмите «next», чтобы пропустить этот шаг."

        user_input_data['state'] = PHOTO

        callback_query.edit_message_text(f'{definition_text}: {definition}')
        callback_query.message.reply_text(reply_text, reply_markup=get_skip_keyboard(user_input_data['state']))

        return PHOTO


def skip_callback_in_photo(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if user_input_data['state'] == PHOTO:
        user_input_data[PHOTO] = None

        if user['lang'] == LANGS[0]:
            photo = "yuborilmagan"
            photo_text = "Yuk rasmi"
            text = '4-Bosqich.'
            reply_text = "Yukni jo'natish kunini tanlang:"

        if user['lang'] == LANGS[1]:
            photo = "не отправлено"
            photo_text = "Фотография груза"
            text = "Шаг 4."
            reply_text = "Выберите дату доставки:"

        inline_keyboard = InlineKeyboard('dates_keyboard', user['lang'])

        callback_query.edit_message_text(f'{photo_text}: {photo}')
        callback_query.message.reply_text(text)
        callback_query.message.reply_text(reply_text, reply_markup=inline_keyboard.get_keyboard())

        logger.info('use_input_data: %s', user_input_data)
        user_input_data['state'] = DATE
        return DATE


def skip_callback_in_receiver(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if user_input_data['state'] == RECEIVER_PHONE_NUMBER:
        user_input_data[RECEIVER_PHONE_NUMBER] = None

        if user['lang'] == LANGS[0]:
            text = 'Yakunlash:'
        if user['lang'] == LANGS[1]:
            text = 'Завершение:'

        callback_query.edit_message_text(text)

        layout = get_new_cargo_layout(user_input_data, user)
        inline_keyboard = InlineKeyboard('confirm_keyboard', user['lang'], data=user_input_data)

        if user_input_data[PHOTO]:
            callback_query.message.reply_photo(user_input_data[PHOTO].get('file_id'), layout,
                                               reply_markup=inline_keyboard.get_keyboard(),
                                               parse_mode=ParseMode.HTML
                                               )
        else:
            callback_query.message.reply_text(text=layout, reply_markup=inline_keyboard.get_keyboard(),
                                              parse_mode=ParseMode.HTML)

        user_input_data['state'] = CONFIRMATION
        return CONFIRMATION


def to_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)
    # print('regions callback')
    # print(callback_query.data)
    region_id = int(data.replace("region_id_", ""))
    user_input_data[TO_REGION] = region_id

    logger.info('new_cargo_info: %s', user_input_data)

    if data == BUTTONS_DATA_DICT['regions'][region_id]:

        if user['lang'] == LANGS[0]:
            text = "Tumanni tanlang:"

        elif user['lang'] == LANGS[1]:
            text = "Выберите район:"

        inline_keyboard = InlineKeyboard('districts_keyboard', user['lang'], region_id)
        callback_query.edit_message_text(text, reply_markup=inline_keyboard.get_keyboard())

    user_input_data['state'] = TO_DISTRICT
    return TO_DISTRICT


def to_district_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())

    # print('district callback')

    if data == BUTTONS_DATA_DICT[6]:

        if user['lang'] == LANGS[0]:
            text = "Yukni jo'natish manzilini tanlang:"

        if user['lang'] == LANGS[1]:
            text = "Выберите адрес доставки:"

        inline_keyboard = InlineKeyboard('regions_keyboard', user['lang'])
        callback_query.edit_message_text(text, reply_markup=inline_keyboard.get_keyboard())

        user_input_data['state'] = TO_REGION
        return TO_REGION

    district_id = int(data.replace("district_id_", ""))
    user_input_data[TO_DISTRICT] = district_id

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yukni jo'natish geolokatsiyasini yuboring.\n\n" \
               "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

    if user['lang'] == LANGS[1]:
        text = 'Отправите геолокацию доставки.\n\n' \
               'Или нажмите «next», чтобы пропустить этот шаг'

    user_input_data['state'] = TO_LOCATION

    callback_query.edit_message_text(text, reply_markup=get_skip_keyboard(user_input_data['state']))
    return TO_LOCATION


def to_location_callback(update: Update, context: CallbackContext):
    # print(location)
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    if update.message.location:

        longitude = update.message.location.longitude
        latitude = update.message.location.latitude

        user_input_data[TO_LOCATION] = {
            'longitude': longitude,
            'latitude': latitude
        }

    else:

        if user['lang'] == LANGS[0]:
            error = "Geolokatsiya noto'g'ri !!!"
            text = "Yukni jo'natish geolokatsiyasini yuboring yoki «next» ni bosing:"

        if user['lang'] == LANGS[1]:
            error = "Геолокация неправильная !!!"
            text = 'Отправите геолокацию доставки или нажмите «next» :'

        update.message.reply_text(error, quote=True)
        update.message.reply_text(text, reply_markup=get_skip_keyboard(user_input_data['state']))

        return TO_LOCATION

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text_1 = "3-Bosqich."
        text_2 = "Yuk og'irligini tanlang:"
        button1_text = UNITS['uz'][0]
        button2_text = UNITS['uz'][1]

    if user['lang'] == LANGS[1]:
        text_1 = "Шаг 3."
        text_2 = "Выберите вес груза:"
        button1_text = UNITS['ru'][0]
        button2_text = UNITS['ru'][1]

    inline_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(button1_text, callback_data='kg'),
            InlineKeyboardButton(button2_text, callback_data='t')
        ]
    ])
    update.message.reply_text(text_1)
    update.message.reply_text(text_2, reply_markup=inline_keyboard)

    user_input_data['state'] = WEIGHT_UNIT
    return WEIGHT_UNIT


def cargo_weight_unit_callback(update: Update, context: CallbackContext):
    # print('cargo weight unit callback')
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)
    user_input_data[WEIGHT_UNIT] = data

    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        if data == 'kg':
            unit = 'kilogramm'
        if data == 't':
            unit = 'tonna'

        text = f"Og'irlik birligi: {unit}"

        reply_text = "Yuk og'irligini kiriting (raqamda):\n\n" \
                     "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

    if user['lang'] == LANGS[1]:
        if data == 'kg':
            unit = 'килограмм'
        if data == 't':
            unit = 'тонны'
        text = f"Единица веса: {unit}"

        reply_text = "Введите вес груза (цифрами):\n\n" \
                     "Или нажмите «next», чтобы пропустить этот шаг."

    user_input_data['state'] = WEIGHT

    callback_query.edit_message_text(text)
    callback_query.message.reply_text(reply_text, reply_markup=get_skip_keyboard(user_input_data['state']))
    return WEIGHT


def cargo_weight_callback(update: Update, context: CallbackContext):
    text = update.message.text

    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    if not text.isdigit():

        if user['lang'] == LANGS[0]:
            text = "Yuk og'irligini raqamda kiriting !!!\n\n" \
                   "Yoki «next» ni bosing."

        if user['lang'] == LANGS[1]:
            text = "Введите вес груза цифрами !!!\n\n" \
                   "Или нажмите «next»."

        update.message.reply_text(text, quote=True, reply_markup=get_skip_keyboard(user_input_data['state']))

        return WEIGHT

    else:
        user_input_data[WEIGHT] = text

    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text_1 = "Yuk hajmini kiriting (raqamda):\n\n" \
                 "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

    if user['lang'] == LANGS[1]:
        text_1 = "Введите объем груза (цифрами):\n" \
                 "Или нажмите «next», чтобы пропустить этот шаг."

    user_input_data['state'] = VOLUME

    update.message.reply_text(text_1, reply_markup=get_skip_keyboard(user_input_data['state']))
    return VOLUME


def cargo_volume_callback(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    if not text.isdigit():

        if user['lang'] == LANGS[0]:
            text = "Yuk hajmini raqamda kiriting !!!\n\n" \
                   "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

        if user['lang'] == LANGS[1]:
            text = "Введите объем груза цифрами !!!\n\n" \
                   "Или нажмите «next», чтобы пропустить этот шаг."

        update.message.reply_text(text, quote=True, reply_markup=get_skip_keyboard(user_input_data['state']))

        return VOLUME

    else:

        user_input_data[VOLUME] = text

    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk tavsifini kiriting:\n" \
               "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

    if user['lang'] == LANGS[1]:
        text = "Введите описание груза:\n" \
               "Или нажмите «next», чтобы пропустить этот шаг."

    user_input_data['state'] = DEFINITION

    update.message.reply_text(text, reply_markup=get_skip_keyboard(user_input_data['state']))
    return DEFINITION


def cargo_definition_callback(update: Update, context: CallbackContext):
    text = update.message.text
    user_input_data = context.user_data
    user_input_data[DEFINITION] = text

    user = get_user(update.effective_user.id)

    if text == '/cancel':

        if user['lang'] == LANGS[0]:
            text = "E'loningiz bekor qilindi !"

        if user['lang'] == LANGS[1]:
            text = "Ваше объявление было отменено !"

        update.message.reply_text(text, quote=True)

        user_input_data.clear()
        return ConversationHandler.END

    if text == '/menu' or text == '/start':

        if user['lang'] == LANGS[0]:
            text = "Sizda tugallanmagan e'lon mavjud.\n" \
                   "E'lonni bekor qilish uchun /cancel ni yuboring"

        if user['lang'] == LANGS[1]:
            text = "У вас есть незаконченное объявление.\n" \
                   "Отправите /cancel , чтобы отменить объявление"

        update.message.reply_text(text, quote=True)

        return DEFINITION

    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk rasmini yuboring:\n" \
               "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

    if user['lang'] == LANGS[1]:
        text = "Отправите фотография груза:\n" \
               "Или нажмите «next», чтобы пропустить этот шаг."

    user_input_data['state'] = PHOTO

    update.message.reply_text(text, reply_markup=get_skip_keyboard(user_input_data['state']))
    return PHOTO


def cargo_photo_callback(update: Update, context: CallbackContext):
    # print('cargo photo callback ')
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    text = update.message.text
    user_input_data = context.user_data
    cargo_photo = update.message.photo

    user = get_user(update.effective_user.id)

    if len(cargo_photo) > 0:

        user_input_data[PHOTO] = cargo_photo[-1].to_dict()

    else:

        if user['lang'] == LANGS[0]:
            error_text = "Yuk rasmi yuborilmadi !!!"
            text = "Yuk rasmini yuboring:\n" \
                   "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

        if user['lang'] == LANGS[1]:
            error_text = 'Фотография груза не отправлено !!!'
            text = "Отправите фотография груза:\n" \
                   "Или нажмите «next», чтобы пропустить этот шаг."

        update.message.reply_text(error_text, quote=True)
        update.message.reply_text(text, quote=True, reply_markup=get_skip_keyboard(user_input_data['state']))

        return PHOTO

    if user['lang'] == LANGS[0]:
        text_1 = '4-Bosqich:'
        text_2 = "Yukni jo'natish kunini tanlang:"

    if user['lang'] == LANGS[1]:
        text_1 = "Шаг 4:"
        text_2 = "Выберите дату доставки:"

    logger.info('use_input_data: %s', user_input_data)

    inline_keyboard = InlineKeyboard('dates_keyboard', user['lang'])

    update.message.reply_text(text_1)
    update.message.reply_text(text_2, reply_markup=inline_keyboard.get_keyboard())

    user_input_data['state'] = DATE
    return DATE


def date_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    # print(user_input_data[PHOTO])

    if data == 'now':

        user_input_data[DATE] = datetime.datetime.now().strftime('%d-%m-%Y')
        user_input_data['time'] = 'now'
        reply_text = get_phone_number_layout(user['lang'])

        if user['lang'] == LANGS[0]:
            text = "Yukni qabul qiluvchining telefon raqamini yuboring:"
            reply_text += "\nBu bosqichni o'tkazib yuborish uchun «next» ni bosing."

        if user['lang'] == LANGS[1]:
            text = "Отправьте номер телефона получателя груза:"
            reply_text += "\nИли нажмите «next», чтобы пропустить этот шаг."

        user_input_data['state'] = RECEIVER_PHONE_NUMBER

        callback_query.edit_message_text(text)
        callback_query.message.reply_html(reply_text, reply_markup=get_skip_keyboard(user_input_data['state']))
        return RECEIVER_PHONE_NUMBER

    if data == 'today' or data == 'tomorrow' or data == 'after_tomorrow':

        if data == 'today':
            user_input_data[DATE] = datetime.datetime.now().strftime('%d-%m-%Y')

        if data == 'tomorrow':
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            user_input_data[DATE] = tomorrow.strftime('%d-%m-%Y')

        if data == 'after_tomorrow':
            after_tomorrow = datetime.datetime.now() + datetime.timedelta(days=2)
            user_input_data[DATE] = after_tomorrow.strftime('%d-%m-%Y')

        if user['lang'] == LANGS[0]:
            text = 'Soatni belgilang:'

        if user['lang'] == LANGS[1]:
            text = 'Выберите время:'

        inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17)
        callback_query.edit_message_text(text, reply_markup=inline_keyboard.get_keyboard())

    user_input_data['state'] = HOUR
    return HOUR


def hour_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    if data == 'next' or data == 'back':

        if data == 'next':
            inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=18, end=29)

        if data == 'back':
            inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17)

        callback_query.edit_message_reply_markup(inline_keyboard.get_keyboard())

        return HOUR

    else:

        if user['lang'] == LANGS[0]:
            text = "Daqiqani belgilang:"

        if user['lang'] == LANGS[1]:
            text = "Выберите минуту:"

        inline_keyboard = InlineKeyboard('minutes_keyboard', user['lang'], data=data)
        callback_query.edit_message_text(text, reply_markup=inline_keyboard.get_keyboard())

        user_input_data['state'] = MINUTE
        return MINUTE


def minute_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'back':

        if user['lang']:
            text = 'Soatni belgilang'

        if user['lang'] == LANGS[1]:
            text = 'Выберите время:'

        inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17)

        callback_query.edit_message_text(text, reply_markup=inline_keyboard.get_keyboard())

        user_input_data['state'] = HOUR
        return HOUR

    else:

        user_input_data['time'] = data

        reply_text = get_phone_number_layout(user['lang'])

        if user['lang'] == LANGS[0]:
            text = "Yukni qabul qiluvchining telefon raqamini yuboring:"
            reply_text += "\nBu bosqichni o'tkazib yuborish uchun «next» ni bosing."

        if user['lang'] == LANGS[1]:
            text = "Отправьте номер телефона получателя груза:"
            reply_text += "\nИли нажмите «next», чтобы пропустить этот шаг."

        user_input_data['state'] = RECEIVER_PHONE_NUMBER

        callback_query.edit_message_text(text)
        callback_query.message.reply_html(reply_text, reply_markup=get_skip_keyboard(user_input_data['state']))

        return RECEIVER_PHONE_NUMBER


def receiver_callback(update: Update, context: CallbackContext):
    text = update.message.text
    contact = update.message.contact

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if contact:
        phone_number = phone_number_filter(contact.phone_number)

    else:
        phone_number = phone_number_filter(text)

    if phone_number and phone_number != user['phone_number']:

        user_input_data[RECEIVER_PHONE_NUMBER] = phone_number
        logger.info('use_input_data: %s', user_input_data)

        layout = get_new_cargo_layout(user_input_data, user)

        inline_keyboard = InlineKeyboard('confirm_keyboard', user['lang'], data=user_input_data)

        if user_input_data[PHOTO]:
            update.message.reply_photo(user_input_data[PHOTO].get('file_id'), layout,
                                       reply_markup=inline_keyboard.get_keyboard(), parse_mode=ParseMode.HTML
                                       )
        else:
            update.message.reply_html(text=layout, reply_markup=inline_keyboard.get_keyboard())

        user_input_data['state'] = CONFIRMATION
        return CONFIRMATION

    else:

        reply_text = get_phone_number_layout(user['lang'])

        if user['lang'] == LANGS[0]:
            text = "Xato telefon raqami yuborildi !!!"
            reply_text += "\nBu bosqichni o'tkazib yuborish uchun «next» ni bosing."
            error_text = "Siz o'z telefon raqmingizni yubordingiz !!!\n\n" \
                         "Yukni qabul qiluvchining telefon raqamini yuboring:"

        if user['lang'] == LANGS[1]:
            text = "Номер телефона с ошибкой отправлен !!!"
            reply_text += "\nИли нажмите «next», чтобы пропустить этот шаг."
            error_text = 'Вы отправили свой номер телефона !!!\n\n' \
                         'Отправьте номер телефона получателя груза:'

        if phone_number == user['phone_number']:
            text = error_text

        update.message.reply_text(text, quote=True)
        update.message.reply_html(reply_text, reply_markup=get_skip_keyboard(user_input_data['state']))

        return RECEIVER_PHONE_NUMBER


def confirmation_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    logger.info('user_input_data: %s', user_input_data)

    if data == 'confirm':

        if user['lang'] == LANGS[0]:
            text = 'Tasdiqlandi !'

        if user['lang'] == LANGS[1]:
            text = 'Подтверждено !'

        user_input_data['state'] = 'confirmed'

        reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang'])
        callback_query.message.reply_text(text, reply_markup=reply_keyboard.get_keyboard())

        lastrow_id = insert_cargo(dict(user_input_data))

        if user_input_data['receiver_phone_number']:

            receiver = get_user(phone_number=user_input_data['receiver_phone_number'])

            if receiver:

                if receiver['lang'] == LANGS[0]:
                    text_1 = "Sizga yuk jo'natildi:"
                    text_2 = "Yukni qabul qildim"

                if receiver['lang'] == LANGS[1]:
                    text_1 = 'Вам груз отправлен:'
                    text_2 = 'Я получил груз'

                context.bot.send_message(receiver['user_id'], text_1)

                inline_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text_2, callback_data=f"received_{user['user_id']}_{lastrow_id}")]
                ])

                layout = get_new_cargo_layout(user_input_data, user)
                if user_input_data[PHOTO]:
                    context.bot.send_photo(receiver['user_id'], user_input_data[PHOTO].get('file_id'), layout,
                                           reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
                else:
                    context.bot.send_message(receiver['user_id'], layout, reply_markup=inline_keyboard,
                                             parse_mode=ParseMode.HTML)

    user_input_data.clear()
    return ConversationHandler.END


def txt_callback(update: Update, context: CallbackContext):
    text = update.message.text
    user_input_data = context.user_data
    logger.info('user_inpt_data: %s', user_input_data)
    user = get_user(update.effective_user.id)

    # print(ConversationHandler.check_update(update))

    # print('text callback')
    if text == '/cancel':

        if user['lang'] == LANGS[0]:
            text = 'Bekor qilindi!'

        if user['lang'] == LANGS[1]:
            text = 'Отменено!'

        inlinekeyboard = InlineKeyboard('main_keyboard', user['lang'])
        update.message.reply_text(text, reply_markup=inlinekeyboard.get_keyboard())

        user_input_data.clear()
        return ConversationHandler.END

    else:

        if user['lang'] == LANGS[0]:
            text = "Sizda tugallanmagan e'lon mavjud.\n" \
                   "E'lonni bekor qilish uchun /cancel ni yuboring"

        if user['lang'] == LANGS[1]:
            text = "У вас есть незаконченное объявление.\n" \
                   "Отправите /cancel , чтобы отменить объявление"

        update.message.reply_text(text, quote=True)

        return user_input_data['state']


def txt_callback_in_confirmation(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)

    user_input_data = context.user_data

    if text != '/done':

        if user['lang'] == LANGS[0]:
            text = 'Sizda tasdiqlanmagan yuk bor !\n' \
                   'Tasdiqlash uchun /done ni bosing'

        if user['lang'] == LANGS[1]:
            text = 'У вас есть неподтвержденная груз !\n' \
                   'Нажмите /done для подтверждения'

        update.message.reply_text(text, quote=True)

        return CONFIRMATION
    else:

        if user['lang'] == LANGS[0]:
            text = 'Tasdiqlandi !'

        if user['lang'] == LANGS[1]:
            text = 'Подтверждено !'

        user_input_data['state'] = 'confirmed'

        reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang'])
        update.message.reply_text(text, reply_markup=reply_keyboard.get_keyboard())

        lastrow_id = insert_cargo(dict(user_input_data))

        if user_input_data['receiver_phone_number']:

            receiver = get_user(phone_number=user_input_data['receiver_phone_number'])

            if receiver:

                if receiver['lang'] == LANGS[0]:
                    text_1 = "Sizga yuk jo'natildi:"
                    text_2 = "Yukni qabul qildim"

                if receiver['lang'] == LANGS[1]:
                    text_1 = 'Вам груз отправлен:'
                    text_2 = 'Я получил груз'

                context.bot.send_message(receiver['user_id'], text_1)

                inline_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text_2, callback_data=f"received_{user['user_id']}_{lastrow_id}")]
                ])

                layout = get_new_cargo_layout(user_input_data, user)
                if user_input_data[PHOTO]:
                    context.bot.send_photo(receiver['user_id'], user_input_data[PHOTO].get('file_id'), layout,
                                           reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
                else:
                    context.bot.send_message(receiver['user_id'], layout, reply_markup=inline_keyboard,
                                             parse_mode=ParseMode.HTML)

        user_input_data.clear()
        return ConversationHandler.END


def new_cargo_callback(update: Update, context: CallbackContext):
    text = update.message.text.split(' ', 1)[-1]

    # print('New cargo')
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if text == "Yuk e'lon qilish" or text == "Объявить груз":

        if user['lang'] == LANGS[0]:
            text = "Viloyatingizni tanlang:"

        if user['lang'] == LANGS[1]:
            text = "Выберите свой область:"

        inline_keyboard = InlineKeyboard('regions_keyboard', user['lang'])

        update.message.reply_text(text, reply_markup=inline_keyboard.get_keyboard())

        user_input_data['state'] = FROM_REGION
        user_input_data['sender_id'] = user['id']
        user_input_data['sender_user_id'] = user['user_id']
        user_input_data['sender_phone_number'] = user['phone_number']
        user_input_data['sender_phone_number2'] = user['phone_number2']

        return FROM_REGION


new_cargo_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r'Yuk|Объявить'), new_cargo_callback)],
    states={
        FROM_REGION: [CallbackQueryHandler(from_region_callback), MessageHandler(Filters.text, txt_callback)],

        FROM_DISTRICT: [CallbackQueryHandler(from_district_callback), MessageHandler(Filters.text, txt_callback)],

        FROM_LOCATION: [MessageHandler(Filters.location | Filters.text, from_location_callback)],

        TO_REGION: [CallbackQueryHandler(to_region_callback), MessageHandler(Filters.text, txt_callback)],

        TO_DISTRICT: [CallbackQueryHandler(to_district_callback), MessageHandler(Filters.text, txt_callback)],

        TO_LOCATION: [CallbackQueryHandler(skip_callback_in_to_location, pattern='.*location$'),
                      MessageHandler(Filters.location | Filters.text, to_location_callback)],

        WEIGHT_UNIT: [CallbackQueryHandler(cargo_weight_unit_callback, pattern='kg|t'),
                      MessageHandler(Filters.text, txt_callback)],

        WEIGHT: [CallbackQueryHandler(skip_callback_in_weight, pattern='.*weight$'),
                 MessageHandler(Filters.text, cargo_weight_callback)],

        VOLUME: [CallbackQueryHandler(skip_callback_in_volume, pattern='.*volume$'),
                 MessageHandler(Filters.text, cargo_volume_callback)],

        DEFINITION: [CallbackQueryHandler(skip_callback_in_definition, pattern='.*definition$'),
                     MessageHandler(Filters.text, cargo_definition_callback)],

        PHOTO: [CallbackQueryHandler(skip_callback_in_photo, pattern='.*photo$'),
                MessageHandler(Filters.photo | Filters.text, cargo_photo_callback)],

        DATE: [CallbackQueryHandler(date_callback, pattern='now|today|tomorrow|after_tomorrow'),
               MessageHandler(Filters.text, txt_callback)],

        HOUR: [CallbackQueryHandler(hour_callback, pattern=r'(?!\bskip)'), MessageHandler(Filters.text, txt_callback)],

        MINUTE: [CallbackQueryHandler(minute_callback, pattern=r'(?!\bskip)'),
                 MessageHandler(Filters.text, txt_callback)],

        RECEIVER_PHONE_NUMBER: [CallbackQueryHandler(skip_callback_in_receiver, pattern='.*receiver_phone$'),
                                MessageHandler(Filters.text | Filters.contact, receiver_callback)],

        CONFIRMATION: [CallbackQueryHandler(confirmation_callback, pattern='confirm'),
                       MessageHandler(Filters.text, txt_callback_in_confirmation)]
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
