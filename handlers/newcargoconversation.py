from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove, ParseMode
from telegram.ext import MessageHandler, ConversationHandler, CallbackQueryHandler, CallbackContext, Filters

from buttonsdatadict import BUTTONS_DATA_DICT
from filters import phone_number_filter
from handlers.editconversation import edit_conversation_handler
from helpers import set_user_data_in_bot_data
from inlinekeyboards import InlineKeyboard
from DB import insert_cargo
from layouts import *
from replykeyboards import ReplyKeyboard
from config import GROUP_ID
from languages import LANGS
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def new_cargo_callback(update: Update, context: CallbackContext):
    text = update.message.text.split(' ', 1)[-1]

    user_input_data = context.user_data
    bot_data = context.bot_data

    # set bot_data[update.effective_user.id] -> dict
    set_user_data_in_bot_data(update.effective_user.id, bot_data)
    user = bot_data[update.effective_user.id]

    if text == 'Yuk e\'lon qilish' or text == 'Объявить груз':

        if user['lang'] == LANGS[0]:
            text = 'Qayerdan (Viloyatni tanlang)'

        if user['lang'] == LANGS[1]:
            text = 'Откуда (Выберите область)'

        text = f'{text}:'
        update.message.reply_text(update.message.text, reply_markup=ReplyKeyboardRemove())

        inline_keyboard = InlineKeyboard('regions_keyboard', user['lang']).get_keyboard()
        message = update.message.reply_text(text, reply_markup=inline_keyboard)

        state = FROM_REGION

        user_input_data['state'] = state
        user_input_data['client_id'] = user['id']
        user_input_data['client_user_id'] = user['user_id']
        user_input_data['client_username'] = user['username']
        user_input_data['client_name'] = user['name']
        user_input_data['client_surname'] = user['surname']
        user_input_data['message_id'] = message.message_id

        return state


def from_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    region_id = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    user_input_data[FROM_REGION] = region_id

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = 'Qayerdan (Tumanni tanlang)'

    if user['lang'] == LANGS[1]:
        text = 'Откуда (Выберите район)'

    text = f'{text}:'

    inline_keyboard = InlineKeyboard('districts_keyboard', user['lang'], region_id).get_keyboard()

    callback_query.answer()
    callback_query.edit_message_text(text, reply_markup=inline_keyboard)

    state = FROM_DISTRICT
    user_input_data['state'] = state

    return state


def from_district_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())

    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == BUTTONS_DATA_DICT[6]:

        if user['lang'] == LANGS[0]:
            text = 'Qayerga (Viloyatni tanlang)'

        if user['lang'] == LANGS[1]:
            text = 'Куда (Выберите область)'

        text = f'{text}:'

        inline_keyboard = InlineKeyboard('regions_keyboard', user['lang']).get_keyboard()
        callback_query.edit_message_text(text, reply_markup=inline_keyboard)

        state = FROM_REGION

    else:

        user_input_data[FROM_DISTRICT] = data

        logger.info('new_cargo_info: %s', user_input_data)

        if user['lang'] == LANGS[0]:
            edit_message_text = 'Geolokatsiyangizni yuboring'
            button_text = 'Geolokatsiyamni jo\'natish'
            reply_text = 'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            edit_message_text = 'Отправьте свою геолокацию'
            button_text = 'Отправить мою геолокацию'
            reply_text = 'Или нажмите «next», чтобы пропустить этот шаг'

        edit_message_text = f'{edit_message_text}:'
        button_text = '\U0001F4CD ' + button_text

        reply_keyboard = ReplyKeyboardMarkup([
            [KeyboardButton(button_text, request_location=True)],
            [KeyboardButton('«next»')]
        ], resize_keyboard=True)

        callback_query.edit_message_text(edit_message_text)
        callback_query.message.reply_text(reply_text, reply_markup=reply_keyboard)

        state = FROM_LOCATION

    callback_query.answer()
    user_input_data['state'] = state

    return state


def from_location_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    text = update.message.text

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if update.message.location or text == '«next»':

        if text == '«next»':

            user_input_data[FROM_LOCATION] = None

        else:

            longitude = update.message.location.longitude
            latitude = update.message.location.latitude

            user_input_data[FROM_LOCATION] = {
                'longitude': longitude,
                'latitude': latitude
            }

        logger.info('new_cargo_info: %s', user_input_data)

        if user['lang'] == LANGS[0]:
            text_2 = 'Qayerga (Viloyatni tanlang)'

        if user['lang'] == LANGS[1]:
            text_2 = 'Куда (Выберите область)'

        text_1 = '\U0001F44D\U0001F44D\U0001F44D'
        text_2 = f'{text_2}:'

        update.message.reply_text(text_1, reply_markup=ReplyKeyboardRemove())

        inline_keyboard = InlineKeyboard('regions_keyboard', user['lang']).get_keyboard()
        message = update.message.reply_text(text_2, reply_markup=inline_keyboard)

        state = TO_REGION
        user_input_data['state'] = state
        user_input_data['message_id'] = message.message_id

    else:

        if user['lang'] == LANGS[0]:
            error_text = 'Geolokatsiya yuborilmadi !\n\n' \
                         'Geolokatsiyangizni yuboring yoki «next» ni bosing'

        if user['lang'] == LANGS[1]:
            error_text = 'Геолокация не отправлена !\n\n' \
                         'Отправьте свою геолокацию или нажмите «next»'

        error_text = '\U000026A0 ' + error_text
        update.message.reply_text(error_text, quote=True)

        state = user_input_data['state']

    return state


def to_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    region_id = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    user_input_data[TO_REGION] = region_id

    logger.info('new_cargo_info: %s', user_input_data)

    if user['lang'] == LANGS[0]:
        text = 'Qayerga (Tumanni tanlang)'

    if user['lang'] == LANGS[1]:
        text = 'Куда (Выберите район)'

    text = f'{text}:'

    callback_query.answer()

    inline_keyboard = InlineKeyboard('districts_keyboard', user['lang'], region_id).get_keyboard()
    callback_query.edit_message_text(text, reply_markup=inline_keyboard)

    state = TO_DISTRICT
    user_input_data['state'] = state

    return state


def to_district_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == BUTTONS_DATA_DICT[6]:

        if user['lang'] == LANGS[0]:
            text = 'Yukni jo\'natish manzilini tanlang (Viloyatni tanlang)'

        if user['lang'] == LANGS[1]:
            text = 'Выберите адрес доставки (Выберите область)'

        text = f'{text}:'

        inline_keyboard = InlineKeyboard('regions_keyboard', user['lang']).get_keyboard()
        callback_query.edit_message_text(text, reply_markup=inline_keyboard)

        state = TO_REGION

    else:

        user_input_data[TO_DISTRICT] = data

        logger.info('new_cargo_info: %s', user_input_data)

        if user['lang'] == LANGS[0]:
            text = 'Yukni jo\'natish geolokatsiyasini yuboring\n\n ' \
                   'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            text = 'Отправите геолокацию доставки\n\n' \
                   'Или нажмите «next», чтобы пропустить этот шаг'

        state = TO_LOCATION

        callback_query.edit_message_text(text, reply_markup=get_skip_keyboard(state))

    callback_query.answer()
    user_input_data['state'] = state

    return state


def to_location_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if not update.message.location:

        if user['lang'] == LANGS[0]:
            error_text = 'Geolokatsiya yuborilmadi !\n\n' \
                         'Yukni jo\'natish geolokatsiyasini yuboring yoki «next» ni bosing'

        if user['lang'] == LANGS[1]:
            error_text = 'Геолокация не отправлена !\n\n' \
                         'Отправите геолокацию доставки или нажмите «next»'

        error_text = '\U000026A0 ' + error_text

        update.message.reply_text(error_text, quote=True)

        state = user_input_data['state']

    else:

        longitude = update.message.location.longitude
        latitude = update.message.location.latitude

        user_input_data[TO_LOCATION] = {
            'longitude': longitude,
            'latitude': latitude
        }

        logger.info('new_cargo_info: %s', user_input_data)

        if user['lang'] == LANGS[0]:
            text = 'Yuk og\'irligini tanlang:\n\n' \
                   'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            text = 'Выберите вес груза:\n\n' \
                   'Или нажмите «next», чтобы пропустить этот шаг'

        inline_keyboard = InlineKeyboard('weights_keyboard', user['lang']).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton('«next»', callback_data='skip_weight')])

        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
        message = update.message.reply_text(text, reply_markup=inline_keyboard)

        state = WEIGHT_UNIT
        user_input_data['state'] = state
        user_input_data['message_id'] = message.message_id

    return state


def cargo_weight_unit_callback(update: Update, context: CallbackContext):
    # print('cargo weight unit callback')
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'skip_weight':
        user_input_data[WEIGHT_UNIT] = None
        user_input_data[WEIGHT] = None

        if user['lang'] == LANGS[0]:
            weight = 'noma\'lum'
            weight_text = 'Yuk og\'irligi'
            text = 'Yuk hajmini yuboring (raqamda):\n\n' \
                   'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            weight = 'неизвестно'
            weight_text = 'Вес груза'
            text = 'Отправьте объем груза (цифрами):\n\n' \
                   'Или нажмите «next», чтобы пропустить этот шаг'

        edit_text = f'<b><i>{weight_text}: {weight}</i></b>'
        callback_query.edit_message_text(edit_text, parse_mode=ParseMode.HTML)

        state = VOLUME

        message = callback_query.message.reply_text(text, reply_markup=get_skip_keyboard(state))
        user_input_data['message_id'] = message.message_id

    else:

        user_input_data[WEIGHT_UNIT] = data

        if user['lang'] == LANGS[0]:
            edit_text = 'Yuk og\'irligini yuboring (raqamda):'

        if user['lang'] == LANGS[1]:
            edit_text = 'Отправьте вес груза (цифрами):'

        state = WEIGHT

        callback_query.edit_message_text(edit_text)

    logger.info('use_input_data: %s', user_input_data)
    callback_query.answer()

    user_input_data['state'] = state
    return state


def cargo_weight_callback(update: Update, context: CallbackContext):
    error_text = update.message.text

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if not error_text.isdigit():

        if user['lang'] == LANGS[0]:
            error_text = 'Yuk og\'irligini raqamda yuboring'

        if user['lang'] == LANGS[1]:
            error_text = 'Отправьте вес груза цифрами'

        error_text = f'\U000026A0 {error_text} !'
        update.message.reply_text(error_text, quote=True)

        state = user_input_data['state']

    else:

        user_input_data[WEIGHT] = error_text

        logger.info('use_input_data: %s', user_input_data)

        if user['lang'] == LANGS[0]:
            error_text = 'Yuk hajmini yuboring (raqamda):\n\n' \
                         'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            error_text = 'Отправьте объем груза (цифрами):\n\n' \
                         'Или нажмите «next», чтобы пропустить этот шаг'

        state = VOLUME

        message = update.message.reply_text(error_text, reply_markup=get_skip_keyboard(state))

        user_input_data['state'] = state
        user_input_data['message_id'] = message.message_id

    return state


def cargo_volume_callback(update: Update, context: CallbackContext):
    text = update.message.text

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if not text.isdigit():

        if user['lang'] == LANGS[0]:
            error_text = 'Yuk hajmini raqamda yuboring !\n\n' \
                         'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            error_text = 'Отправьте объем груза цифрами !\n' \
                         'Или нажмите «next», чтобы пропустить этот шаг'

        error_text = '\U000026A0 ' + error_text
        update.message.reply_text(error_text, quote=True)

        state = user_input_data['state']

    else:

        user_input_data[VOLUME] = text
        user_input_data[VOLUME_UNIT] = 'm\U000000B3'

        logger.info('use_input_data: %s', user_input_data)

        if user['lang'] == LANGS[0]:
            text = 'Yuk tavsifini yuboring:\n\n' \
                   'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            text = 'Отправьте описание груза:\n\n' \
                   'Или нажмите «next», чтобы пропустить этот шаг'

        state = DEFINITION

        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
        message = update.message.reply_text(text, reply_markup=get_skip_keyboard(state))

        user_input_data['state'] = state
        user_input_data['message_id'] = message.message_id

    return state


def cargo_definition_callback(update: Update, context: CallbackContext):
    text = update.message.text

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    user_input_data[DEFINITION] = text

    if text == '/cancel':

        if user['lang'] == LANGS[0]:
            cancel_text = 'E\'lon bekor qilindi'

        if user['lang'] == LANGS[1]:
            cancel_text = 'Объявление отменено'

        cancel_text = f'\U0000274C {cancel_text} !'

        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
        update.message.reply_text(cancel_text, quote=True)

        user_input_data.clear()
        return ConversationHandler.END

    if text == '/menu' or text == '/start':

        if user['lang'] == LANGS[0]:
            warning_text = 'Sizda tugallanmagan e\'lon mavjud !\n\n' \
                           'E\'lonni bekor qilish uchun /cancel ni yuboring'

        if user['lang'] == LANGS[1]:
            warning_text = 'У вас есть незаконченное объявление !\n\n' \
                           'Отправите /cancel , чтобы отменить объявление'

        text = f'\U000026A0 ' + warning_text
        update.message.reply_text(text, quote=True)

        state = user_input_data['state']

    else:

        logger.info('use_input_data: %s', user_input_data)

        if user['lang'] == LANGS[0]:
            text = 'Yuk rasmini yuboring:\n\n' \
                   'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            text = 'Отправите фотография груза:\n\n' \
                   'Или нажмите «next», чтобы пропустить этот шаг'

        state = PHOTO

        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
        message = update.message.reply_text(text, reply_markup=get_skip_keyboard(state))

        user_input_data['state'] = state
        user_input_data['message_id'] = message.message_id

    return state


def cargo_photo_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    cargo_photo = update.message.photo

    if not cargo_photo:

        if user['lang'] == LANGS[0]:
            error_text = 'Yuk rasmi yuborilmadi !\n' \
                         'Yuk rasmini yuboring:\n\n' \
                         'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            error_text = 'Фотография груза не отправлено !\n' \
                         'Отправите фотография груза:\n\n' \
                         'Или нажмите «next», чтобы пропустить этот шаг'

        error_text = '\U000026A0 ' + error_text

        update.message.reply_text(error_text, quote=True)

        state = user_input_data['state']

    else:

        user_input_data[PHOTO] = cargo_photo[-1].to_dict()

        if user['lang'] == LANGS[0]:
            text = 'Yukni jo\'natish kunini belgilang'

        if user['lang'] == LANGS[1]:
            text = 'Установите дату доставки'

        text = f'{text}:'

        inline_keyboard = InlineKeyboard('dates_keyboard', user['lang']).get_keyboard()

        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
        message = update.message.reply_text(text, reply_markup=inline_keyboard)

        state = DATE

        user_input_data['state'] = state
        user_input_data['message_id'] = message.message_id

    return state


def date_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'now':

        user_input_data[DATE] = datetime.datetime.now().strftime('%d-%m-%Y')
        user_input_data[TIME] = 'now'

        phone_number_layout = get_phone_number_layout(user['lang'])

        if user['lang'] == LANGS[0]:
            edit_text = 'Siz bilan bog\'lanish uchun raqamingizni yuboring'

        if user['lang'] == LANGS[1]:
            edit_text = 'Отправьте свой номер для связи с вами'

        reply_text = phone_number_layout

        callback_query.edit_message_text(edit_text)
        logger.info('use_input_data: %s', user_input_data)

        reply_keyboard = ReplyKeyboard('phone_number_keyboard', user['lang']).get_keyboard()
        callback_query.message.reply_html(reply_text, reply_markup=reply_keyboard)

        state = CLIENT_PHONE_NUMBER

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
            edit_text = 'Soatni belgilang'

        if user['lang'] == LANGS[1]:
            edit_text = 'Выберите время'

        edit_text = f'{edit_text}:'

        inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17).get_keyboard()
        callback_query.edit_message_text(edit_text, reply_markup=inline_keyboard)

        state = TIME

    callback_query.answer()

    user_input_data['state'] = state

    return state


def hour_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'next' or data == 'back_btn':

        if data == 'next':
            inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=18, end=29).get_keyboard()

        if data == 'back_btn':
            inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17).get_keyboard()

        callback_query.edit_message_reply_markup(inline_keyboard)

        state = user_input_data['state']

    else:

        user_input_data[TIME] = data
        phone_number_layout = get_phone_number_layout(user['lang'])

        if user['lang'] == LANGS[0]:
            edit_text = 'Siz bilan bog\'lanish uchun raqamingizni yuboring\n\n'

        if user['lang'] == LANGS[1]:
            edit_text = 'Отправьте свой номер для связи с вами\n\n'

        reply_text = phone_number_layout

        callback_query.edit_message_text(edit_text)
        logger.info('use_input_data: %s', user_input_data)

        reply_keyboard = ReplyKeyboard('phone_number_keyboard', user['lang']).get_keyboard()
        callback_query.message.reply_html(reply_text, reply_markup=reply_keyboard)

        state = CLIENT_PHONE_NUMBER

        user_input_data['state'] = state

    callback_query.answer()
    return state


def phone_number_callback(update: Update, context: CallbackContext):
    with open('jsons/update.json', 'w') as update_file:
        update_file.write(update.to_json())
    text = update.message.text
    contact = update.message.contact

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if contact:
        phone_number = phone_number_filter(contact.phone_number)

    else:
        phone_number = phone_number_filter(text)

    if phone_number:

        user_input_data[CLIENT_PHONE_NUMBER] = phone_number

        layout = get_new_cargo_layout(user_input_data, user['lang'])

        inline_keyboard = InlineKeyboard('confirm_keyboard', user['lang'], data=user_input_data).get_keyboard()

        update.message.reply_text('\U0001F447\U0001F447\U0001F447', reply_markup=ReplyKeyboardRemove())

        if user_input_data[PHOTO]:
            message = update.message.reply_photo(user_input_data[PHOTO].get('file_id'), layout,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            message = update.message.reply_html(layout, reply_markup=inline_keyboard)

        logger.info('use_input_data: %s', user_input_data)

        state = CONFIRMATION
        user_input_data['state'] = state
        user_input_data['message_id'] = message.message_id

    else:

        if user['lang'] == LANGS[0]:
            error_text = 'Xato telefon raqami yuborildi'

        if user['lang'] == LANGS[1]:
            error_text = 'Номер телефона с ошибкой отправлен'

        error_text = f'\U000026A0 {error_text} !'
        phone_number_layout = get_phone_number_layout(user['lang'])

        update.message.reply_text(error_text, quote=True)
        update.message.reply_html(phone_number_layout)

        state = user_input_data['state']

    return state


def confirmation_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    logger.info('user_input_data: %s', user_input_data)

    if data == 'confirm':

        if user['lang'] == LANGS[0]:
            text = 'E\'lon tasdiqlandi'

        if user['lang'] == LANGS[1]:
            text = 'Объявление подтверждено'

        text = f'\U00002705 {text} !'

        reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang']).get_keyboard()
        callback_query.message.reply_text(text, reply_markup=reply_keyboard)

        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data['message_id'])

        user_input_data['state'] = 'opened'
        layout = get_new_cargo_layout(user_input_data, user['lang'])
        layout_2 = get_new_cargo_layout(user_input_data, lang='cy')

        if user_input_data[FROM_LOCATION] or user_input_data[TO_LOCATION]:
            inline_keyboard = InlineKeyboard('geolocation_keyboard', lang='cy', data=user_input_data).get_keyboard()

        else:
            inline_keyboard = None

        if user_input_data[PHOTO]:
            context.bot.edit_message_caption(user_input_data['client_user_id'], user_input_data['message_id'],
                                             caption=layout, parse_mode=ParseMode.HTML)

            message = context.bot.send_photo(GROUP_ID, user_input_data[PHOTO].get('file_id'),
                                             layout_2, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            context.bot.edit_message_text(layout, user_input_data['client_user_id'], user_input_data['message_id'],
                                          parse_mode=ParseMode.HTML)

            message = context.bot.send_message(GROUP_ID, layout_2, reply_markup=inline_keyboard,
                                               parse_mode=ParseMode.HTML)

        user_input_data['message_id'] = message.message_id
        insert_cargo(dict(user_input_data))

        user_input_data.clear()
        state = ConversationHandler.END

    if data == 'edit':
        # with open('jsons/callback_query.json', 'w') as cargo:
        #     cargo.write(callback_query.to_json())
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        state = EDIT
        user_input_data['state'] = state

    return state


def txt_callback(update: Update, context: CallbackContext):
    text = update.message.text

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    logger.info('user_inpt_data: %s', user_input_data)

    if user_input_data['state'] == CONFIRMATION:

        if user['lang'] == LANGS[0]:
            confirm = 'Tasdiqlash'
            warning_text = 'Sizda tasdiqlanmagan e\'lon bor !\n\n' \
                           f'Tasdiqlash uchun  <b><i>«{confirm}»</i></b> tugmasini bosing'

        if user['lang'] == LANGS[1]:
            confirm = 'Подтвердить'
            warning_text = 'У вас есть неподтвержденное объявление !\n\n' \
                           f'Нажмите кнопку <b><i>«{confirm}»</i></b>, чтобы подтвердить'

        warning_text = '\U000026A0 ' + warning_text
        update.message.reply_html(warning_text, quote=True)

        return user_input_data['state']

    if text == '/cancel':

        if user['lang'] == LANGS[0]:
            cancel_text = 'E\'lon bekor qilindi'

        if user['lang'] == LANGS[1]:
            cancel_text = 'Объявление отменено'

        cancel_text = f'\U0000274C {cancel_text} !'
        reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang']).get_keyboard()

        update.message.reply_text(cancel_text, reply_markup=reply_keyboard)
        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))

        user_input_data.clear()
        return ConversationHandler.END

    else:

        if user['lang'] == LANGS[0]:
            warning_text = 'Sizda tugallanmagan e\'lon mavjud !\n\n' \
                           'E\'lonni bekor qilish uchun /cancel ni yuboring'

        if user['lang'] == LANGS[1]:
            warning_text = 'У вас есть незаконченное объявление !\n\n' \
                           'Отправите /cancel , чтобы отменить объявление'

        warning_text = '\U000026A0 ' + warning_text
        update.message.reply_text(warning_text, quote=True)

        return user_input_data['state']


def get_skip_keyboard(state):
    # if lang == LANGS[0]:
    #     button_text = 'keyingisi'
    #
    # if lang == LANGS[1]:
    #     button_text = 'следующий'

    if state == TO_LOCATION:
        data = 'skip_to_location'

    if state == VOLUME:
        data = 'skip_volume'

    if state == DEFINITION:
        data = 'skip_definition'

    if state == PHOTO:
        data = 'skip_photo'

    return InlineKeyboardMarkup([
        [InlineKeyboardButton('«next»', callback_data=data)]
    ])


def skip_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'skip_to_location':

        user_input_data[TO_LOCATION] = None

        if user['lang'] == LANGS[0]:
            location = 'noma\'lum'
            location_text = 'Yukni jo\'natish geolokatsiyasi'
            text = 'Yuk og\'irligini tanlang:\n\n' \
                   'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            location = 'неизвестно'
            location_text = 'Геолокация доставки'
            text = 'Выберите вес груза:\n\n' \
                   'Или нажмите «next», чтобы пропустить этот шаг'

        edit_text = f'<b><i>{location_text}: {location}</i></b>'
        callback_query.edit_message_text(edit_text, parse_mode=ParseMode.HTML)

        inline_keyboard = InlineKeyboard('weights_keyboard', user['lang']).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton('«next»', callback_data='skip_weight')])

        message = callback_query.message.reply_text(text, reply_markup=inline_keyboard)
        user_input_data['message_id'] = message.message_id

        state = WEIGHT_UNIT

    if data == 'skip_volume':

        user_input_data[VOLUME] = None

        if user['lang'] == LANGS[0]:
            volume = 'noma\'lum'
            volume_text = 'Yuk hajmi'
            reply_text = 'Yuk tavsifini yuboring:\n\n' \
                         'Yoki bu bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            volume = 'неизвестно'
            volume_text = 'Объем груза'
            reply_text = 'Отправьте описание груза:\n\n' \
                         'Или нажмите «next», чтобы пропустить этот шаг'

        edit_text = f'<b><i>{volume_text}: {volume}</i></b>'
        callback_query.edit_message_text(edit_text, parse_mode=ParseMode.HTML)

        state = DEFINITION

        message = callback_query.message.reply_text(reply_text, reply_markup=get_skip_keyboard(state))
        user_input_data['message_id'] = message.message_id

    if data == 'skip_definition':

        user_input_data[DEFINITION] = None

        if user['lang'] == LANGS[0]:
            definition = 'noma\'lum'
            definition_text = 'Yuk tasnifi'
            reply_text = 'Yuk rasmini yuboring:\n\n' \
                         'Yoki bosqichni o\'tkazib yuborish uchun «next» ni bosing'

        if user['lang'] == LANGS[1]:
            definition = 'неизвестно'
            definition_text = 'Описание груза'
            reply_text = 'Отправите фотография груза:\n\n' \
                         'Или нажмите «next», чтобы пропустить этот шаг'

        edit_text = f'<b><i>{definition_text}: {definition}</i></b>'
        callback_query.edit_message_text(edit_text, parse_mode=ParseMode.HTML)

        state = PHOTO

        message = callback_query.message.reply_text(reply_text, reply_markup=get_skip_keyboard(state))
        user_input_data['message_id'] = message.message_id

    if data == 'skip_photo':

        user_input_data[PHOTO] = None

        if user['lang'] == LANGS[0]:
            photo = 'yuborilmagan'
            photo_text = 'Yuk rasmi'
            reply_text = 'Yukni jo\'natish kunini tanlang'

        if user['lang'] == LANGS[1]:
            photo = 'не отправлено'
            photo_text = 'Фотография груза'
            reply_text = 'Выберите дату доставки'

        edit_text = f'<b><i>{photo_text}: {photo}</i></b>'
        reply_text = f'{reply_text}:'

        callback_query.edit_message_text(edit_text, parse_mode=ParseMode.HTML)

        inline_keyboard = InlineKeyboard('dates_keyboard', user['lang']).get_keyboard()
        message = callback_query.message.reply_text(reply_text, reply_markup=inline_keyboard)

        user_input_data['message_id'] = message.message_id

        state = DATE

    user_input_data['state'] = state
    return state


new_cargo_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('(Yuk e\'lon qilish|Объявить груз)$'), new_cargo_callback)],

    states={
        FROM_REGION: [CallbackQueryHandler(from_region_callback, pattern=r'^(\d+)$'),
                      MessageHandler(Filters.text, txt_callback)],

        FROM_DISTRICT: [CallbackQueryHandler(from_district_callback, pattern=r'^(\d+)$'),
                        MessageHandler(Filters.text, txt_callback)],

        FROM_LOCATION: [MessageHandler(Filters.location | Filters.text, from_location_callback)],

        TO_REGION: [CallbackQueryHandler(to_region_callback, pattern=r'^(\d+)$'),
                    MessageHandler(Filters.text, txt_callback)],

        TO_DISTRICT: [CallbackQueryHandler(to_district_callback, pattern=r'^(\d+)$'),
                      MessageHandler(Filters.text, txt_callback)],

        TO_LOCATION: [
            CallbackQueryHandler(skip_callback, pattern='^skip_(to_location|volume|definition|photo)$'),
            MessageHandler(Filters.location | Filters.text, to_location_callback)],

        WEIGHT_UNIT: [CallbackQueryHandler(cargo_weight_unit_callback, pattern='^(kg|t|skip_weight)$'),
                      MessageHandler(Filters.text, txt_callback)],

        WEIGHT: [MessageHandler(Filters.text, cargo_weight_callback)],

        VOLUME: [
            CallbackQueryHandler(skip_callback, pattern='^skip_(to_location|volume|definition|photo)$'),
            MessageHandler(Filters.text, cargo_volume_callback)],

        DEFINITION: [
            CallbackQueryHandler(skip_callback, pattern='^skip_(to_location|volume|definition|photo)$'),
            MessageHandler(Filters.text, cargo_definition_callback)],

        PHOTO: [
            CallbackQueryHandler(skip_callback, pattern='^skip_(to_location|volume|definition|photo)$'),
            MessageHandler(Filters.photo | Filters.text, cargo_photo_callback)],

        DATE: [CallbackQueryHandler(date_callback, pattern='^(now|today|tomorrow|after_tomorrow)$'),
               MessageHandler(Filters.text, txt_callback)],

        TIME: [CallbackQueryHandler(hour_callback, pattern=r'^(back_btn|next|\d+[:]00)$'),
               MessageHandler(Filters.text, txt_callback)],

        CLIENT_PHONE_NUMBER: [MessageHandler(Filters.text | Filters.contact, phone_number_callback)],

        CONFIRMATION: [CallbackQueryHandler(confirmation_callback, pattern='^(confirm|edit)$'),
                       MessageHandler(Filters.text, txt_callback)],

        EDIT: [edit_conversation_handler]
    },

    fallbacks=[],
)
