from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove, ParseMode
from telegram.ext import (MessageHandler, ConversationHandler, CallbackQueryHandler, CallbackContext, Filters)
from inlinekeyboards import InlineKeyboard
from DB.main import *
from buttonsdatadict import BUTTONS_DATA_DICT
from units import UNITS
from languages import LANGS
from filters import phone_number_filter
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

USER_ID, FROM_REGION, FROM_DISTRICT, FROM_LOCATION, TO_REGION, TO_DISTRICT, TO_LOCATION, \
WEIGHT_UNIT, WEIGHT, VOLUME_UNIT, VOLUME, DEFINITION, PHOTO, DATE, HOUR, MINUTE, \
RECEIVER_PHONE_NUMBER, CONFIRMATION = \
    ('user_id', 'from_region', 'from_district', 'from_location', 'to_region', 'to_district', 'to_location',
     'weight_unit', 'weight', 'volume_unit', 'volume', 'definition', 'photo',
     'date', 'hour', 'minute', 'receiver_phone_number', 'confirmation')


def get_caption(user_input_data, user, lang):
    from_point = get_region_and_district(user_input_data[FROM_REGION], user_input_data[FROM_DISTRICT])
    to_point = get_region_and_district(user_input_data[TO_REGION], user_input_data[TO_DISTRICT])

    if user_input_data[WEIGHT_UNIT] == 'kg':
        m = 0
    else:
        m = 1

    caption_uz = f"Qayerdan: {from_point[1]['nameUz']}, {from_point[0]['nameUz']}\n" \
                 f"Qayerga: {to_point[1]['nameUz']}, {to_point[0]['nameUz']}\n\n" \
                 f"Yuk og'irligi: {user_input_data[WEIGHT]}, {UNITS['uz'][m]}\n" \
                 f"Yuk hajmi: {user_input_data[VOLUME]}, {UNITS['uz'][2]}\n\n" \
                 f"Yuk tavsifi: {user_input_data[DEFINITION]}\n\n" \
                 f"Yukni jo'natish kuni: {user_input_data[DATE]}\n" \
                 f"Yukni jo'natish vaqti: {user_input_data['time']}\n\n" \
                 f"E'lon beruvchi: {user['name']} {user['surname']}\n" \
                 f"Tel nomer 1: {user['phone_number']}\n" \
                 f"Tel nomer 2: {user['phone_number2']}\n\n" \
                 f"Yukni qabul qiluvchi raqami: {user_input_data[RECEIVER_PHONE_NUMBER]}\n\n" \
                 f"\U0001F916 @cardelshipperbot \U000000A9"

    caption_ru = f"Откуда: {from_point[1]['nameRu']}, {from_point[0]['nameRu']}\n" \
                 f"Куда: {to_point[1]['nameRu']}, {to_point[0]['nameRu']}\n\n" \
                 f"Вес груза: {user_input_data[WEIGHT]}, {UNITS['ru'][m]}\n" \
                 f"Размер груза: {user_input_data[VOLUME]}, {UNITS['ru'][2]}\n\n" \
                 f"Описание груза: {user_input_data[DEFINITION]}\n\n" \
                 f"Дата отправки груза: {user_input_data[DATE]}\n" \
                 f"Время отправки груза: {user_input_data['time']}\n\n" \
                 f"Объявитель: {user['name']} {user['surname']}\n" \
                 f"Тел номер 1: {user['phone_number']}\n" \
                 f"Тел номер 2: {user['phone_number2']}\n\n" \
                 f"Тел номер получателя груза: {user_input_data[RECEIVER_PHONE_NUMBER]}\n\n" \
                 f"\U0001F916 @cardelshipperbot \U000000A9"

    if lang == LANGS[0]:
        return caption_uz

    if lang == LANGS[1]:
        return caption_ru


def get_layout_keyboard(user_input_data, user):
    from_latitude = user_input_data['from_location']['latitude']
    from_longitude = user_input_data['from_location']['longitude']
    to_latitude = user_input_data[TO_LOCATION]['latitude']
    to_longitude = user_input_data[TO_LOCATION]['longitude']

    inline_keyboard = []

    if from_latitude and from_longitude:
        inline_keyboard.append(
            [InlineKeyboardButton('A',
                                  url=f'http://www.google.com/maps/place/{from_latitude},{from_longitude}/'
                                      f'@{from_latitude},{from_longitude},12z')])

    if to_latitude and to_longitude:
        inline_keyboard.append(
            [InlineKeyboardButton('B',
                                  url=f'http://www.google.com/maps/place/{to_latitude},{to_longitude}/'
                                      f'@{to_latitude},{to_longitude},12z')])

    if from_latitude and from_longitude and to_latitude and to_longitude:
        direction = f'https://www.google.com/maps/dir/{from_latitude},{from_longitude}/{to_latitude},{to_longitude}'
        inline_keyboard.append([InlineKeyboardButton('A->B', url=direction)])

    if user['lang'] == LANGS[0]:
        button_text = 'Tasdiqlash'

    if user['lang'] == LANGS[1]:
        button_text = 'Подтвердить'

    inline_keyboard.append([InlineKeyboardButton(button_text, callback_data='confirm')])

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard)

    return inline_keyboard


def from_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    user_input_data = context.user_data

    data = callback_query.data

    user = get_user(update.effective_user.id)
    # print('regions callback')
    # print(callback_query.data)
    region_id = int(data.replace("region_id_", ""))
    user_input_data[FROM_REGION] = region_id

    logger.info('new_cargo_info: %s', user_input_data)

    if data == BUTTONS_DATA_DICT['regions'][region_id]:

        if user['lang'] == LANGS[0]:
            text = "Tumaningizni tanlang:"

        elif user['lang'] == LANGS[1]:
            text = "Выберите свой район:"

        inline_keyboard = InlineKeyboard('districts_keyboard', user['lang'], region_id)
        callback_query.edit_message_text(text)
        callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

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
        callback_query.edit_message_text(text)
        callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

        user_input_data['state'] = FROM_REGION
        return FROM_REGION

    district_id = int(data.replace("district_id_", ""))
    user_input_data[FROM_DISTRICT] = district_id

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        edit_message_text = 'Lokatsiyangizni yuboring:'
        button_text = "\U0001F4CD Lokatsiyamni jo'natish"
        reply_text = "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        edit_message_text = 'Отправите местоположение:'
        button_text = "\U0001F4CD Отправить мое местоположение"
        reply_text = "Или нажмите /skip, чтобы пропустить этот шаг"

    callback_query.edit_message_text(edit_message_text)
    reply_keyboard = ReplyKeyboardMarkup([[KeyboardButton(button_text, request_location=True)]], resize_keyboard=True)
    callback_query.message.reply_text(reply_text, reply_markup=reply_keyboard)

    user_input_data['state'] = FROM_LOCATION
    return FROM_LOCATION


def from_location_callback(update: Update, context: CallbackContext):
    user = get_user(update.effective_user.id)
    # print(location)
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_input_data = context.user_data

    if update.message.location:
        longitude = update.message.location.longitude
        latitude = update.message.location.latitude

        user_input_data['from_location'] = {
            'longitude': longitude,
            'latitude': latitude
        }
    else:

        if update.message.text == '/skip':
            user_input_data['from_location'] = {
                'longitude': None,
                'latitude': None
            }

        else:

            if user['lang'] == LANGS[0]:
                text = 'Lokatsiyangizni yuboring yoki /skip ni bosing:'

            if user['lang'] == LANGS[1]:
                text = 'Укажите свое местоположение или нажмите /skip:'

            update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

            return FROM_LOCATION

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text_1 = '2-Bosqich'
        text_2 = "Yukni jo'natish manzilini tanlang:"

    if user['lang'] == LANGS[1]:
        text_1 = 'Шаг 2'
        text_2 = "Выберите адрес доставки:"

    update.message.reply_text(text_1, reply_markup=ReplyKeyboardRemove())
    inline_keyboard = InlineKeyboard('regions_keyboard', user['lang'])
    update.message.reply_text(text_2, reply_markup=inline_keyboard.get_keyboard())

    user_input_data['state'] = TO_REGION
    return TO_REGION


def to_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    user_input_data = context.user_data

    data = callback_query.data

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
        callback_query.edit_message_text(text)
        callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

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
        callback_query.edit_message_text(text)
        callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

        user_input_data['state'] = TO_REGION
        return TO_REGION

    district_id = int(data.replace("district_id_", ""))
    user_input_data[TO_DISTRICT] = district_id

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yukni jo'natish lokatsiyasini yuborish:\n" \
               "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        text = 'Отправите местоположение доставки:\n' \
               "Или нажмите /skip, чтобы пропустить этот шаг"

    callback_query.edit_message_text(text)

    user_input_data['state'] = TO_LOCATION
    return TO_LOCATION


def to_location_callback(update: Update, context: CallbackContext):
    user = get_user(update.effective_user.id)
    # print(location)
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_input_data = context.user_data

    if update.message.location:

        longitude = update.message.location.longitude
        latitude = update.message.location.latitude

        user_input_data[TO_LOCATION] = {
            'longitude': longitude,
            'latitude': latitude
        }

    else:

        if update.message.text == '/skip':
            user_input_data[TO_LOCATION] = {
                'longitude': None,
                'latitude': None
            }

        else:

            if user['lang'] == LANGS[0]:
                text = "Yukni jo'natish lokatsiyasini yuboring yoki /skip ni bosing:"

            if user['lang'] == LANGS[1]:
                text = 'Укажите местоположение доставки или нажмите /skip :'

            update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

            return TO_LOCATION

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "3-Bosqich\n" \
               "Yuk og'irligini tanlang:"
        button1_text = UNITS['uz'][0]
        button2_text = UNITS['uz'][1]

    if user['lang'] == LANGS[1]:
        text = "Шаг 3\n" \
               "Выберите вес груза:"
        button1_text = UNITS['ru'][0]
        button2_text = UNITS['ru'][1]

    inline_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(button1_text, callback_data='kg'),
            InlineKeyboardButton(button2_text, callback_data='t')
        ]
    ])

    update.message.reply_text(text, reply_markup=inline_keyboard)

    user_input_data['state'] = WEIGHT_UNIT
    return WEIGHT_UNIT


def cargo_weight_unit_callback(update: Update, context: CallbackContext):
    # print('cargo weight unit callback')
    callback_query = update.callback_query
    user_input_data = context.user_data
    data = callback_query.data

    user = get_user(update.effective_user.id)

    user_input_data[WEIGHT_UNIT] = data

    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk og'irligini kiriting (raqamda):\n" \
               "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        text = "Введите вес груза (цифрами):\n" \
               "Или нажмите /skip, чтобы пропустить этот шаг."

    callback_query.edit_message_text(text)

    user_input_data['state'] = WEIGHT
    return WEIGHT


def cargo_weight_callback(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    if text == '/skip':
        user_input_data[WEIGHT] = None

    elif not text.isdigit():

        if user['lang'] == LANGS[0]:
            text = "Yuk og'irligini raqamda kiriting !!!"

        if user['lang'] == LANGS[1]:
            text = "Введите вес груза цифрами !!!"

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return WEIGHT

    else:
        user_input_data[WEIGHT] = text

    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk hajmini tanlang:"
        button_text = UNITS['uz'][2]

    if user['lang'] == LANGS[1]:
        text = "Выберите размер груза:"
        button_text = UNITS['ru'][2]

    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(button_text, callback_data='m3')]
    ])

    update.message.reply_text(text, reply_markup=inline_keyboard)

    user_input_data['state'] = VOLUME_UNIT
    return VOLUME_UNIT


def cargo_volume_unit_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    user_input_data = context.user_data

    user = get_user(update.effective_user.id)
    user_input_data[VOLUME_UNIT] = data
    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk hajmini kiriting (raqamda):\n" \
               "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        text = "Введите размер груза (цифрами):\n" \
               "Или нажмите /skip, чтобы пропустить этот шаг."

    callback_query.edit_message_text(text)

    user_input_data['state'] = VOLUME
    return VOLUME


def cargo_volume_callback(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    if text == '/skip':
        user_input_data[VOLUME] = None

    elif not text.isdigit():

        if user['lang'] == LANGS[0]:
            text = "Yuk hajmini raqamda kiriting !!!"

        if user['lang'] == LANGS[1]:
            text = "Введите размер груза цифрами !!!"

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return VOLUME

    else:
        user_input_data[VOLUME] = text

    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk tavsifini kiriting:\n" \
               "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        text = "Введите описание груза:\n" \
               "Или нажмите /skip, чтобы пропустить этот шаг."

    update.message.reply_text(text)

    user_input_data['state'] = DEFINITION
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

        update.message.reply_text(text, reply_to_message_id=update.message.message_id)

        user_input_data.clear()
        return ConversationHandler.END

    if text == '/skip':
        user_input_data[DEFINITION] = None

    if text == '/menu' or text == '/start':

        if user['lang'] == LANGS[0]:
            text = "Sizda tugallanmagan e'lon mavjud.\n" \
                   "E'lonni bekor qilish uchun /cancel ni yuboring"

        if user['lang'] == LANGS[1]:
            text = "У вас есть незаконченное объявление.\n" \
                   "Отправите /cancel , чтобы отменить объявление"

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return DEFINITION

    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk rasmini yuboring:\n" \
               "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        text = "Отправите фотография груза:\n" \
               "Или нажмите /skip, чтобы пропустить этот шаг."

    update.message.reply_text(text)

    user_input_data['state'] = PHOTO
    return PHOTO


def cargo_photo_callback(update: Update, context: CallbackContext):
    # print('cargo photo callback ')
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    text = update.message.text
    user_input_data = context.user_data
    cargo_photo = update.message.photo

    user = get_user(update.effective_user.id)

    if text == '/skip' or len(cargo_photo) > 0:

        if text == '/skip':
            user_input_data[PHOTO] = None

        if len(cargo_photo) > 0:
            user_input_data[PHOTO] = cargo_photo[-1].to_dict()

        if user['lang'] == LANGS[0]:
            text = "Yukni jo'natish kunini tanlang:"

        if user['lang'] == LANGS[1]:
            text = "Выберите дату доставки:"

        inline_keyboard = InlineKeyboard('dates_keyboard', user['lang'])

        update.message.reply_text(text, reply_markup=inline_keyboard.get_keyboard())

        logger.info('use_input_data: %s', user_input_data)
        user_input_data['state'] = DATE
        return DATE

    else:

        if user['lang'] == LANGS[0]:
            text = "Yuk rasmini yuboring:\n" \
                   "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

        if user['lang'] == LANGS[1]:
            text = "Отправите фотография груза:\n" \
                   "Или нажмите /skip, чтобы пропустить этот шаг."

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return PHOTO


def date_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    # print(user_input_data[PHOTO])

    if data == 'now':
        user_input_data[DATE] = datetime.datetime.now().strftime('%d-%m-%Y')
        user_input_data['time'] = datetime.datetime.now().strftime('%H:%M')

        if user['lang'] == LANGS[0]:
            text = "Yukni qabul qiluvchining telefon raqamini yuboring:\n" \
                   "Raqamni quyidagi shaklda kiriting:\n\n" \
                   "<b><i><u>Misol: 99 1234567</u></i></b>\nYoki\n" \
                   "<b><i><u>Misol: +998 99 1234567</u></i></b>\n\n" \
                   "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

        if user['lang'] == LANGS[1]:
            text = "Отправьте номер телефона получателя груза:\n" \
                   "Введите номер в виде ниже:\n\n" \
                   "<b><i><u>Пример: 99 1234567</u></i></b>\nYoki\n" \
                   "<b><i><u>Пример: +998 99 1234567</u></i></b>\n\n" \
                   "Или нажмите /skip, чтобы пропустить этот шаг."

        callback_query.edit_message_text(text, parse_mode=ParseMode.HTML)

        user_input_data['state'] = RECEIVER_PHONE_NUMBER
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

        inline_keyboard = InlineKeyboard('minutes_keyboard', user['lang'], data=data)

        if user['lang'] == LANGS[0]:
            text = "Daqiqani belgilang:"

        if user['lang'] == LANGS[1]:
            text = "Выберите минуту:"

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

        if user['lang'] == LANGS[0]:
            text = "Yukni qabul qiluvchining telefon raqamini yuboring:\n" \
                   "Raqamni quyidagi shaklda kiriting:\n\n" \
                   "<b><i><u>Misol: 99 1234567</u></i></b>\nYoki\n" \
                   "<b><i><u>Misol: +998 99 1234567</u></i></b>\n\n" \
                   "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

        if user['lang'] == LANGS[1]:
            text = "Отправьте номер телефона получателя груза:\n" \
                   "Введите номер в виде ниже:\n\n" \
                   "<b><i><u>Misol: 99 1234567</u></i></b>\nYoki\n" \
                   "<b><i><u>Misol: +998 99 1234567</u></i></b>\n\n" \
                   "Или нажмите /skip, чтобы пропустить этот шаг."

        callback_query.edit_message_text(text, parse_mode=ParseMode.HTML)

        user_input_data['state'] = RECEIVER_PHONE_NUMBER
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

    if phone_number or text == '/skip':

        if text == '/skip':
            user_input_data[RECEIVER_PHONE_NUMBER] = None

        user_input_data[RECEIVER_PHONE_NUMBER] = phone_number

        if user['lang'] == LANGS[0]:
            caption = get_caption(user_input_data, user, LANGS[0])

        if user['lang'] == LANGS[1]:
            caption = get_caption(user_input_data, user, LANGS[1])

        inline_keyboard = get_layout_keyboard(user_input_data, user)

        if user_input_data[PHOTO]:
            update.message.reply_photo(user_input_data[PHOTO].get('file_id'),
                                       caption=get_caption(user_input_data, user, user['lang']),
                                       reply_markup=inline_keyboard
                                       )
        else:
            update.message.reply_text(text=caption, reply_markup=inline_keyboard)

        user_input_data['state'] = CONFIRMATION
        return CONFIRMATION

    else:

        if user['lang'] == LANGS[0]:
            text = "Telefon raqami xato kiritildi !!!\n" \
                   "Qaytadan quyidagi shaklda kiriting:\n\n" \
                   "<b><i><u>Misol: 99 1234567</u></i></b>\nYoki\n" \
                   "<b><i><u>Misol: +998 99 1234567</u></i></b>\n"

        if user['lang'] == LANGS[1]:
            text = "Номер телефона введен неправильно !!!\n" \
                   "Введите еще раз в виде ниже:\n\n" \
                   "<b><i><u>Пример: 99 1234567</u></i></b>\nИли\n" \
                   "<b><i><u>Пример: +998 99 991234567</u></i></b>"

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id,
                                  parse_mode=ParseMode.HTML)

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

        callback_query.message.reply_text(text)

        if user_input_data['receiver_phone_number']:
            receiver = get_user(phone_number=user_input_data['receiver_phone_number'])
        else:
            receiver = False

        if receiver:

            if receiver['lang'] == LANGS[0]:
                text = "Sizga yuk jo'natildi:"

            if receiver['lang'] == LANGS[1]:
                text = 'Вам груз отправлен:'

            context.bot.send_message(receiver['user_id'], text)

            if user_input_data[PHOTO]:
                context.bot.send_photo(receiver['user_id'], user_input_data[PHOTO].get('file_id'),
                                       caption=get_caption(user_input_data, user, receiver['lang']))
            else:
                context.bot.send_message(receiver['user_id'], get_caption(user_input_data, user, receiver['lang']))

    # user_input_data.clear()

    insert_cargo(user_input_data)

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

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return user_input_data['state']


# def txt_callback_in_cargo_weight_unit(update: Update, context: CallbackContext):
#     else:
#
#         if user['lang'] == LANGS[0]:
#             text = "Yuk og'irligini tanlang:"
#             button1_text = UNITS['uz'][0]
#             button2_text = UNITS['uz'][1]
#
#         if user['lang'] == LANGS[1]:
#             text = "Выберите вес груза:"
#             button1_text = UNITS['ru'][0]
#             button2_text = UNITS['ru'][1]
#
#         inline_keyboard = InlineKeyboardMarkup([
#             [
#                 InlineKeyboardButton(button1_text, callback_data='kilogramgramm'),
#                 InlineKeyboardButton(button2_text, callback_data='tonna')
#             ]
#         ])
#
#         update.message.reply_text(text, reply_markup=inline_keyboard,
#                                   reply_to_message_id=update.effective_message.message_id)
#
#     return WEIGHT_UNIT


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

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return CONFIRMATION
    else:

        if user['lang'] == LANGS[0]:
            text = "Tasdiqlandi"

        if user['lang'] == LANGS[1]:
            text = 'Подтверждено !'

        update.message.reply_text(text)

        if user_input_data['receiver_phone_number']:
            receiver = get_user(phone_number=user_input_data['receiver_phone_number'])
        else:
            receiver = False

        if receiver:

            if receiver['lang'] == LANGS[0]:
                text = "Sizga yuk jo'natildi:"

            if receiver['lang'] == LANGS[1]:
                text = 'Вам груз отправлен:'

            context.bot.send_message(receiver['user_id'], text)

            if user_input_data[PHOTO]:
                context.bot.send_photo(receiver['user_id'], user_input_data[PHOTO].get('file_id'),
                                       caption=get_caption(user_input_data, user, receiver['lang']))
            else:
                context.bot.send_message(receiver['user_id'], get_caption(user_input_data, user, receiver['lang']))
        # user_input_data.clear()

        insert_cargo(user_input_data)

        user_input_data.clear()
        return ConversationHandler.END


def new_cargo_conversation_callback(update: Update, context: CallbackContext):
    # print('new caro conversation starter')
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    callback_query = update.callback_query
    data = callback_query.data

    if data == BUTTONS_DATA_DICT[2]:

        if user['lang'] == LANGS[0]:
            text = "Viloyatingizni tanlang:"

        if user['lang'] == LANGS[1]:
            text = "Выберите свой область:"

    inline_keyboard = InlineKeyboard('regions_keyboard', user['lang'])

    callback_query.edit_message_text(text, reply_markup=inline_keyboard.get_keyboard())

    user_input_data['state'] = FROM_REGION

    user_input_data['sender_id'] = user['id']
    user_input_data['sender_user_id'] = user['user_id']
    user_input_data['sender_phone_number'] = user['phone_number']
    user_input_data['sender_phone_number2'] = user['phone_number2']

    return FROM_REGION
    # return PHOTO


new_cargo_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(new_cargo_conversation_callback, pattern='^new')],
    states={
        FROM_REGION: [CallbackQueryHandler(from_region_callback),
                      MessageHandler(Filters.text, txt_callback)],

        FROM_DISTRICT: [CallbackQueryHandler(from_district_callback),
                        MessageHandler(Filters.text, txt_callback)],

        FROM_LOCATION: [MessageHandler(Filters.location | Filters.text, from_location_callback)],

        TO_REGION: [CallbackQueryHandler(to_region_callback),
                    MessageHandler(Filters.text, txt_callback)],

        TO_DISTRICT: [CallbackQueryHandler(to_district_callback),
                      MessageHandler(Filters.text, txt_callback)],

        TO_LOCATION: [MessageHandler(Filters.location | Filters.text, to_location_callback)],

        WEIGHT_UNIT: [CallbackQueryHandler(cargo_weight_unit_callback),
                      MessageHandler(Filters.text, txt_callback)],

        WEIGHT: [MessageHandler(Filters.text, cargo_weight_callback)],

        VOLUME_UNIT: [CallbackQueryHandler(cargo_volume_unit_callback),
                      MessageHandler(Filters.text, txt_callback)],

        VOLUME: [MessageHandler(Filters.text, cargo_volume_callback)],

        DEFINITION: [MessageHandler(Filters.text, cargo_definition_callback)],

        PHOTO: [MessageHandler(Filters.photo | Filters.text, cargo_photo_callback)],

        DATE: [CallbackQueryHandler(date_callback), MessageHandler(Filters.text, txt_callback)],

        HOUR: [CallbackQueryHandler(hour_callback), MessageHandler(Filters.text, txt_callback)],

        MINUTE: [CallbackQueryHandler(minute_callback), MessageHandler(Filters.text, txt_callback)],

        RECEIVER_PHONE_NUMBER: [MessageHandler(Filters.text | Filters.contact, receiver_callback)],

        CONFIRMATION: [CallbackQueryHandler(confirmation_callback),
                       MessageHandler(Filters.text, txt_callback_in_confirmation)]
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
