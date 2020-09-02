from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from telegram.ext import (MessageHandler, ConversationHandler, CallbackQueryHandler, CallbackContext, Filters)
from inlinekeyboards import InlineKeyboard
from DB.main import *
from languages import LANGS
from buttonsdatadict import BUTTONS_DATA_DICT
from units import UNITS
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

USER_ID, FROM_REGION, FROM_DISTRICT, FROM_LOCATION, TO_REGION, TO_DISTRICT, TO_LOCATION, \
CARGO_WEIGHT_UNIT, CARGO_WEIGHT, CARGO_VOLUME_UNIT, CARGO_VOLUME, CARGO_DEFINITION, CARGO_PHOTO, CONFIRMATION = \
    ('user_id', 'from_region', 'from_district', 'from_location', 'to_region', 'to_district', 'to_location',
     'cargo_weight_unit', 'cargo_weight', 'cargo_volume_unit', 'cargo_volume', 'cargo_definition', 'cargo_photo',
     'confirmation')


def from_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    user_input_data = context.user_data

    data = callback_query.data

    user = get_user(update.effective_user.id)
    # print('regions callback')
    # print(callback_query.data)
    region_id = int(data.replace("region_id_", ""))
    user_input_data['from_region_id'] = region_id

    logger.info('new_cargo_info: %s', user_input_data)

    if data == BUTTONS_DATA_DICT['regions'][region_id]:

        if user['lang'] == LANGS[0]:
            text = "Tumaningizni tanlang:"

        elif user['lang'] == LANGS[1]:
            text = "Выберите свой район:"

        inline_keyboard = InlineKeyboard('districts_keyboard', user['lang'], region_id)
        callback_query.edit_message_text(text)
        callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

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

        return FROM_REGION

    district_id = int(data.replace("district_id_", ""))
    user_input_data['from_district_id'] = district_id

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        edit_message_text = 'Lokatsiyangizni yuboring:'
        button_text = "\U0001F4CD Lokatsiyamni jo'natish"
        reply_text = "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        edit_message_text = 'Отправите местоположение:'
        button_text = "\U0001F4CD Отправить мое местоположение"
        reply_text = "Нажмите /skip, чтобы пропустить этот шаг"

    callback_query.edit_message_text(edit_message_text)
    reply_keyboard = ReplyKeyboardMarkup([[KeyboardButton(button_text, request_location=True)]], resize_keyboard=True)
    callback_query.message.reply_text(reply_text, reply_markup=reply_keyboard)

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

    elif update.message.text == '/skip':

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

    return TO_REGION


def to_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    user_input_data = context.user_data

    data = callback_query.data

    user = get_user(update.effective_user.id)
    # print('regions callback')
    # print(callback_query.data)
    region_id = int(data.replace("region_id_", ""))
    user_input_data['to_region_id'] = region_id

    logger.info('new_cargo_info: %s', user_input_data)

    if data == BUTTONS_DATA_DICT['regions'][region_id]:

        if user['lang'] == LANGS[0]:
            text = "Tumanni tanlang:"

        elif user['lang'] == LANGS[1]:
            text = "Выберите район:"

        inline_keyboard = InlineKeyboard('districts_keyboard', user['lang'], region_id)
        callback_query.edit_message_text(text)
        callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

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

        return TO_REGION

    district_id = int(data.replace("district_id_", ""))
    user_input_data['to_district_id'] = district_id

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yukni jo'natish lokatsiyasini yuborish:\n" \
               "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        text = 'Отправите местоположение доставки:\n' \
               "Нажмите /skip, чтобы пропустить этот шаг"

    callback_query.edit_message_text(text)

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

        user_input_data['to_location'] = {
            'longitude': longitude,
            'latitude': latitude
        }

    elif update.message.text == '/skip':

        user_input_data['to_location'] = {
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
            InlineKeyboardButton(button1_text, callback_data='kilogramm'),
            InlineKeyboardButton(button2_text, callback_data='tonna')
        ]
    ])

    update.message.reply_text(text, reply_markup=inline_keyboard)

    return CARGO_WEIGHT_UNIT


def cargo_weight_unit_callback(update: Update, context: CallbackContext):
    # print('cargo weight unit callback')
    callback_query = update.callback_query
    user_input_data = context.user_data
    data = callback_query.data

    user = get_user(update.effective_user.id)

    user_input_data['cargo_weight_unit'] = data
    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk og'irligini kiriting (raqamda):\n" \
               "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        text = "Введите вес груза (цифрами):\n" \
               "Нажмите /skip, чтобы пропустить этот шаг."

    callback_query.edit_message_text(text)

    return CARGO_WEIGHT


def cargo_weight_callback(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    user_input_data['cargo_weight'] = text

    if text == '/skip':
        user_input_data['cargo_weight'] = None

    if not text.isdigit() and text != '/skip':

        if user['lang'] == LANGS[0]:
            text = "Yuk og'irligini raqamda kiriting !!!"

        if user['lang'] == LANGS[1]:
            text = "Введите вес груза цифрами !!!"

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return CARGO_WEIGHT

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

    return CARGO_VOLUME_UNIT


def cargo_volume_unit_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    user_input_data = context.user_data

    user = get_user(update.effective_user.id)
    user_input_data['cargo_volume_unit'] = data
    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk hajmini kiriting (raqamda):\n" \
               "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        text = "Введите размер груза (цифрами):\n" \
               "Нажмите /skip, чтобы пропустить этот шаг."

    callback_query.edit_message_text(text)

    return CARGO_VOLUME


def cargo_volume_callback(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)
    user_input_data = context.user_data
    user_input_data['cargo_volume'] = text

    if text == '/skip':
        user_input_data['cargo_volume'] = None

    if not text.isdigit() and text != '/skip':

        if user['lang'] == LANGS[0]:
            text = "Yuk hajmini raqamda kiriting !!!"

        if user['lang'] == LANGS[1]:
            text = "Введите размер груза цифрами !!!"

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return CARGO_VOLUME

    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk tavsifini kiriting:\n" \
               "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        text = "Введите описание груза:\n" \
               "Нажмите /skip, чтобы пропустить этот шаг."

    update.message.reply_text(text)

    return CARGO_DEFINITION


def cargo_definition_callback(update: Update, context: CallbackContext):
    text = update.message.text
    user_input_data = context.user_data
    user_input_data['cargo_definition'] = text

    user = get_user(update.effective_user.id)

    if text == '/cancel':

        if user['lang'] == LANGS[0]:
            text = "E'loningiz bekor qilindi !"

        if user['lang'] == LANGS[1]:
            text = "Ваше объявление было отменено !"

        update.message.reply_text(text, reply_to_message_id=update.message.message_id)

        return ConversationHandler.END

    if text == '/skip':
        user_input_data['cargo_definition'] = None

    if text == '/menu' or text == '/start':

        if user['lang'] == LANGS[0]:
            text = "Sizda tugallanmagan e'lon mavjud.\n" \
                   "E'lonni bekor qilish uchun /cancel ni yuboring"

        if user['lang'] == LANGS[1]:
            text = "У вас есть незаконченное объявление.\n" \
                   "Отправите /cancel , чтобы отменить объявление"

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return CARGO_DEFINITION

    logger.info('use_input_data: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = "Yuk rasmini yuboring:\n" \
               "Bu bosqichni o'tkazib yuborish uchun /skip ni bosing."

    if user['lang'] == LANGS[1]:
        text = "Отправите фотография груза:\n" \
               "Нажмите /skip, чтобы пропустить этот шаг."

    update.message.reply_text(text)

    return CARGO_PHOTO


def cargo_photo_callback(update: Update, context: CallbackContext):
    # print('cargo photo callback ')
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    text = update.message.text
    user_input_data = context.user_data
    cargo_photo = update.message.photo

    user_input_data['cargo_photo'] = cargo_photo
    user = get_user(update.effective_user.id)

    from_point = get_region_and_district(user_input_data['from_region_id'], user_input_data['from_district_id'])
    to_point = get_region_and_district(user_input_data['to_region_id'], user_input_data['to_district_id'])

    caption_uz = f"Qayerdan: {from_point[1]['nameUz']}, {from_point[0]['nameUz']}\n" \
                 f"Qayerga: {to_point[1]['nameUz']}, {to_point[0]['nameUz']}\n\n" \
                 f"Yuk og'irligi: {user_input_data['cargo_weight']}, {user_input_data['cargo_weight_unit']}\n" \
                 f"Yuk hajmi: {user_input_data['cargo_volume']}, {user_input_data['cargo_volume_unit']}\n\n" \
                 f"Yuk tavsifi: {user_input_data['cargo_definition']}\n\n" \
                 f"Tel nomer 1: {user['phone_number']}\n" \
                 f"Tel nomer 2: {user['phone_number2']}\n"

    caption_ru = f"Откуда: {from_point[1]['nameRu']}, {from_point[0]['nameRu']}\n" \
                 f"Куда: {to_point[1]['nameRu']}, {to_point[0]['nameRu']}\n\n" \
                 f"Вес груза: {user_input_data['cargo_weight']}, {user_input_data['cargo_weight_unit']}\n" \
                 f"Размер груза: {user_input_data['cargo_volume']}, {user_input_data['cargo_volume_unit']}\n\n" \
                 f"Описание груза: {user_input_data['cargo_definition']}\n\n" \
                 f"Тел номер 1: {user['phone_number']}\n" \
                 f"Тел номер 2: {user['phone_number2']}\n"

    if user['lang'] == LANGS[0]:
        button_text = 'Tasdiqlash'
        caption = caption_uz

    if user['lang'] == LANGS[1]:
        button_text = 'Подтвердить'
        caption = caption_ru

    inline_keyboard = [
        [InlineKeyboardButton(button_text, callback_data='confirm')]
    ]

    from_latitude = user_input_data['from_location']['latitude']
    from_longitude = user_input_data['from_location']['longitude']

    if from_latitude and from_longitude:
        inline_keyboard.append(
            [InlineKeyboardButton('A', url=f'http://www.google.com/maps/place/{from_latitude},{from_longitude}/@{from_latitude},{from_longitude},12z')])

    to_latitude = user_input_data['to_location']['latitude']
    to_longitude = user_input_data['to_location']['longitude']

    if to_latitude and to_longitude:
        inline_keyboard.append(
            [InlineKeyboardButton('B', url=f'http://www.google.com/maps/place/{to_latitude},{to_longitude}/@{to_latitude},{to_longitude},12z')])

    if from_latitude and from_longitude and to_latitude and to_longitude:
        direction = f'https://www.google.com/maps/dir/{from_latitude},{from_longitude}/{to_latitude},{to_longitude}'
        inline_keyboard.append([InlineKeyboardButton('A->B', url=direction)])

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard)

    logger.info('use_input_data: %s', user_input_data)

    if text == '/skip' or len(cargo_photo) > 0:

        if text == '/skip':
            user_input_data['cargo_photo'] = None

            update.message.reply_text(caption, reply_markup=inline_keyboard)

        if len(cargo_photo) > 0:
            cargo_photo_id = cargo_photo[len(cargo_photo) - 1].file_id

            update.message.reply_photo(cargo_photo_id, caption=caption, reply_markup=inline_keyboard)

        return CONFIRMATION

    else:

        if user['lang'] == LANGS[0]:
            text = "Yuk rasmini yuboring:\n" \
                   "Yoki /skip ni bosing."

        if user['lang'] == LANGS[1]:
            text = "Отправите фотография груза:\n" \
                   "Или нажмите /skip ."

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return CARGO_PHOTO


def confirmation_callback(update: Update, contex: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)

    if data == 'confirm':

        if user['lang'] == LANGS[0]:
            text = 'Tasdiqlandi !'
        if user['lang'] == LANGS[1]:
            text = 'Подтверждено !'

        callback_query.message.reply_text(text)

    return ConversationHandler.END


def txt_callback_in_region(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)

    # print(ConversationHandler.check_update(update))

    # print('text callback in region')
    if text == '/cancel':

        if user['lang'] == LANGS[0]:
            text = 'Bekor qilindi!'

        if user['lang'] == LANGS[1]:
            text = 'Отменено!'

        inlinekeyboard = InlineKeyboard('main_keyboard', user['lang'])
        update.message.reply_text(text, reply_markup=inlinekeyboard.get_keyboard())

        return ConversationHandler.END

    else:

        if user['lang'] == LANGS[0]:
            text = "Sizda tugallanmagan e'lon mavjud.\n" \
                   "E'lonni bekor qilish uchun /cancel ni yuboring"

        if user['lang'] == LANGS[1]:
            text = "У вас есть незаконченное объявление.\n" \
                   "Отправите /cancel , чтобы отменить объявление"

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return FROM_REGION


def txt_callback_in_district(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)

    if text == '/cancel':

        if user['lang'] == LANGS[0]:
            text = 'Bekor qilindi!'

        if user['lang'] == LANGS[1]:
            text = 'Отменено!'

        inlinekeyboard = InlineKeyboard('main_keyboard', user['lang'])
        update.message.reply_text(text, reply_markup=inlinekeyboard.get_keyboard())

        return ConversationHandler.END

    else:
        if user['lang'] == LANGS[0]:
            text = "Sizda tugallanmagan e'lon mavjud.\n" \
                   "E'lonni bekor qilish uchun /cancel ni yuboring"

        if user['lang'] == LANGS[1]:
            text = "У вас есть незаконченное объявление.\n" \
                   "Отправите /cancel , чтобы отменить объявление"

        update.message.reply_text(text, reply_to_message_id=update.effective_message.message_id)

        return FROM_DISTRICT


def txt_callback_in_cargo_weight_unit(update: Update, context: CallbackContext):
    # print('txt_callback_in_cargo_weight_unit')
    text = update.message.text
    user = get_user(update.effective_user.id)

    if text == '/start' or text == '/menu':

        if user['lang'] == LANGS[0]:
            text = 'Bekor qilindi!'

        if user['lang'] == LANGS[1]:
            text = 'Отменено!'

        inlinekeyboard = InlineKeyboard('main_keyboard', user['lang'])
        update.message.reply_text(text, reply_markup=inlinekeyboard.get_keyboard())

    else:

        if user['lang'] == LANGS[0]:
            text = "Yuk og'irligini tanlang:"
            button1_text = UNITS['uz'][0]
            button2_text = UNITS['uz'][1]

        if user['lang'] == LANGS[1]:
            text = "Выберите вес груза:"
            button1_text = UNITS['ru'][0]
            button2_text = UNITS['ru'][1]

        inline_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='kilogramm'),
                InlineKeyboardButton(button2_text, callback_data='tonna')
            ]
        ])

        update.message.reply_text(text, reply_markup=inline_keyboard,
                                  reply_to_message_id=update.effective_message.message_id)

    return CARGO_WEIGHT_UNIT


def txt_callback_in_cargo_volume_unit(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)

    if text == '/start' or text == '/menu':

        if user['lang'] == LANGS[0]:
            text = 'Bekor qilindi!'

        if user['lang'] == LANGS[1]:
            text = 'Отменено!'

        inlinekeyboard = InlineKeyboard('main_keyboard', user['lang'])
        update.message.reply_text(text, reply_markup=inlinekeyboard.get_keyboard())

    else:

        if user['lang'] == LANGS[0]:
            text = "Yuk hajmini tanlang:"
            button_text = UNITS['uz'][2]

        if user['lang'] == LANGS[1]:
            text = "Выберите рвзмер груза:"
            button_text = UNITS['ru'][2]

        inline_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button_text, callback_data='m3'),
            ]
        ])

        update.message.reply_text(text, reply_markup=inline_keyboard,
                                  reply_to_message_id=update.effective_message.message_id)

    return CARGO_VOLUME_UNIT


def txt_callback_in_confirmation(update: Update, context: CallbackContext):
    text = update.message.text
    user = get_user(update.effective_user.id)

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

        return ConversationHandler.END


def new_cargo_conversation_callback(update: Update, context: CallbackContext):
    # print('new caro conversation starter')
    user = get_user(update.effective_user.id)

    callback_query = update.callback_query
    data = callback_query.data

    if data == BUTTONS_DATA_DICT[2]:

        if user['lang'] == LANGS[0]:
            text = "Viloyatingizni tanlang:"

        if user['lang'] == LANGS[1]:
            text = "Выберите свой область:"

    inline_keyboard = InlineKeyboard('regions_keyboard', user['lang'])
    callback_query.edit_message_text(text)
    callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

    return FROM_REGION


new_cargo_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(new_cargo_conversation_callback, pattern='^new')],
    states={
        FROM_REGION: [CallbackQueryHandler(from_region_callback),
                      MessageHandler(Filters.text, txt_callback_in_region)],

        FROM_DISTRICT: [CallbackQueryHandler(from_district_callback),
                        MessageHandler(Filters.text, txt_callback_in_district)],

        FROM_LOCATION: [MessageHandler(Filters.location | Filters.text, from_location_callback)],

        TO_REGION: [CallbackQueryHandler(to_region_callback),
                    MessageHandler(Filters.text, txt_callback_in_region)],

        TO_DISTRICT: [CallbackQueryHandler(to_district_callback),
                      MessageHandler(Filters.text, txt_callback_in_district)],

        TO_LOCATION: [MessageHandler(Filters.location | Filters.text, to_location_callback)],

        CARGO_WEIGHT_UNIT: [CallbackQueryHandler(cargo_weight_unit_callback),
                            MessageHandler(Filters.text, txt_callback_in_cargo_weight_unit)],

        CARGO_WEIGHT: [MessageHandler(Filters.text, cargo_weight_callback)],

        CARGO_VOLUME_UNIT: [CallbackQueryHandler(cargo_volume_unit_callback),
                            MessageHandler(Filters.text, txt_callback_in_cargo_volume_unit)],

        CARGO_VOLUME: [MessageHandler(Filters.text, cargo_volume_callback)],

        CARGO_DEFINITION: [MessageHandler(Filters.text, cargo_definition_callback)],

        CARGO_PHOTO: [MessageHandler(Filters.photo | Filters.text, cargo_photo_callback)],

        CONFIRMATION: [CallbackQueryHandler(confirmation_callback),
                       MessageHandler(Filters.text, txt_callback_in_confirmation)]
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
