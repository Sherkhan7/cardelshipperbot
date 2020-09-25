from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, ParseMode
from layouts import *
from inlinekeyboards import InlineKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from hadlers.newcargoconversation import get_skip_keyboard


def edit_address_callback(update: Update, context: CallbackContext):
    # print('edit_address_callback')

    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data

    if data == 'back':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kunni tahrirlash', callback_data='edit_date')],
            [InlineKeyboardButton('Vaqtni tahrirlash', callback_data='edit_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])
        user_input_data['state'] = 'EDIT'
        state = 'EDIT'

    if data == 'edit_from_address':
        # print('edit_from_address')
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Viloyatni tahrirlash', callback_data='edit_region'),
             InlineKeyboardButton('Tumanni tahrirlash', callback_data='edit_district')]
        ])

        user_input_data['state'] = 'edit_from_address'
        state = 'edit_from_address'

    if data == 'edit_to_address':
        # print('edit_to_address')
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Viloyatni tahrirlash', callback_data='edit_region'),
             InlineKeyboardButton('Tumanni tahrirlash', callback_data='edit_district')]
        ])

        user_input_data['state'] = 'edit_to_address'
        state = 'edit_to_address'

    if data == 'edit_from_location':
        # print('edit_from_location')
        button_text = "\U0001F4CD Geolokatsiyamni jo'natish"
        reply_text = "Geolokatsiyangizni yuboring:\n\n" \
                     "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

        reply_keyboard = ReplyKeyboardMarkup([
            [KeyboardButton(button_text, request_location=True)],
            [KeyboardButton('«next»')]
        ], resize_keyboard=True)

        callback_query.message.reply_text(reply_text, reply_markup=reply_keyboard)
        user_input_data['state'] = 'edit_from_location'
        state = 'edit_from_location'
        inline_keyboard = None

    if data == 'edit_to_location':
        # print('edit_to_location')

        # if user['lang'] == LANGS[0]:
        text = "Yukni jo'natish geolokatsiyasini yuboring.\n\n" \
               "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

        # if user['lang'] == LANGS[1]:
        #     text = 'Отправите геолокацию доставки.\n\n' \
        #            'Или нажмите «next», чтобы пропустить этот шаг'

        inline_keyboard = None
        user_input_data['state'] = 'edit_to_location'
        state = 'edit_to_location'

    callback_query.answer()
    callback_query.edit_message_reply_markup(inline_keyboard)

    if data == 'edit_to_location':
        callback_query.message.reply_text(text, reply_markup=get_skip_keyboard('to_location'))
    return state


def edit_region_or_district_callback(update: Update, context: CallbackContext):
    # print('edit region or district callback')

    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    # print('---state---', user_input_data['state'])
    if user_input_data['state'] == 'edit_from_address':

        if data == 'edit_region':
            inline_keyboard = InlineKeyboard('regions_keyboard', 'uz').get_keyboard()
            state = 'edit_region'

        if data == 'edit_district':
            inline_keyboard = InlineKeyboard('districts_keyboard', 'uz',
                                             region_id=user_input_data['from_region']).get_keyboard()

            state = 'edit_district'

    if user_input_data['state'] == 'edit_to_address':
        if data == 'edit_region':
            inline_keyboard = InlineKeyboard('regions_keyboard', 'uz').get_keyboard()
            state = 'edit_region'

        if data == 'edit_district':
            inline_keyboard = InlineKeyboard('districts_keyboard', 'uz',
                                             region_id=user_input_data['to_region']).get_keyboard()

            state = 'edit_district'

    callback_query.answer()
    callback_query.edit_message_reply_markup(inline_keyboard)

    return state


def edit_district_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print(data)

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'back_btn':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Viloyatni tahrirlash', callback_data='edit_region'),
             InlineKeyboardButton('Tumanni tahrirlash', callback_data='edit_district')]
        ])
        state = user_input_data['state']
        answer = None
        layout = get_new_cargo_layout(user_input_data, user)
        # callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        callback_query.edit_message_reply_markup(inline_keyboard)

    else:

        district_id = int(data.replace("district_id_", ""))

        if user_input_data['state'] == 'edit_from_address':
            user_input_data[FROM_DISTRICT] = district_id
            answer = "\U0001F44F\U0001F44F\U0001F44F Yuboruvchi manzili tahrirlandi."

        if user_input_data['state'] == 'edit_to_address':
            user_input_data[TO_DISTRICT] = district_id
            answer = "\U0001F44F\U0001F44F\U0001F44F Qabul qiluvchi manzili tahrirlandi."

        layout = get_new_cargo_layout(user_input_data, user)
        inline_keyboard = InlineKeyboard('confirm_keyboard', user['lang'], data=user_input_data).get_keyboard()

        if user_input_data['photo']:
            callback_query.message.edit_caption(caption=layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        user_input_data['state'] = CONFIRMATION
        state = ConversationHandler.END

    callback_query.answer(answer)

    return state


def edit_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    print(data)

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    region_id = int(data.replace("region_id_", ""))

    if user_input_data['state'] == 'edit_from_address':
        user_input_data[FROM_REGION] = region_id

    if user_input_data['state'] == 'edit_to_address':
        user_input_data[TO_REGION] = region_id

    # logger.info('new_cargo_info: %s', user_input_data)

    if data == BUTTONS_DATA_DICT['regions'][region_id]:
        inline_keyboard = InlineKeyboard('districts_keyboard', 'uz', region_id)
        callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

        callback_query.answer()

    return 'edit_district'


def edit_from_location_callback(update: Update, context: CallbackContext):
    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

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

        return 'edit_from_location'

    # logger.info('new_cargo_info: %s', user_input_data)
    text = get_new_cargo_layout(user_input_data, user)
    inline_keyboard = InlineKeyboard('confirm_keyboard', user['lang'], data=user_input_data).get_keyboard()

    update.message.reply_text('Yuboruvchi geolokatsiyasi tahrirlandi', reply_markup=ReplyKeyboardRemove())

    if user_input_data['photo']:
        update.message.reply_photo(user_input_data['photo']['file_id'], caption=text, reply_markup=inline_keyboard,
                                   parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    user_input_data['state'] = CONFIRMATION

    return ConversationHandler.END


def edit_to_location_callback(update: Update, context: CallbackContext):
    # print('edit_to_location_callback')
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    callback_query = update.callback_query

    if callback_query:

        # with open('jsons/callback_query.json', 'w') as update_file:
        #     update_file.write(callback_query.to_json())

        user_input_data[TO_LOCATION] = {
            'longitude': None,
            'latitude': None
        }

        text = get_new_cargo_layout(user_input_data, user)
        inline_keyboard = InlineKeyboard('confirm_keyboard', user['lang'], data=user_input_data).get_keyboard()

        callback_query.answer('Qabul qiluvchi geolokatsiyasi tahrirlandi')

        if user_input_data['photo']:
            callback_query.edit_message_text('Qabul qiluvchi geolokatsiyasi tahrirlandi')
            callback_query.message.reply_photo(user_input_data['photo']['file_id'], caption=text,
                                               reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    else:

        # with open('jsons/update.json', 'w') as update_file:
        #     update_file.write(update.to_json())

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
            update.message.reply_text(text, reply_markup=get_skip_keyboard('to_location'))

            return 'edit_to_location'

        inline_keyboard = InlineKeyboard('confirm_keyboard', user['lang'], data=user_input_data).get_keyboard()
        text = get_new_cargo_layout(user_input_data, user)

        update.message.reply_text('Qabul qiluvchi geolokatsiyasi tahrirlandi')
        if user_input_data['photo']:
            update.message.reply_photo(user_input_data['photo']['file_id'], caption=text,
                                       reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    user_input_data['state'] = CONFIRMATION

    return ConversationHandler.END


def message_callback_in_address(update: Update, context: CallbackContext):
    print('message callback in address')


edit_address_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_address_callback,
                                       pattern='edit_from_address|edit_to_address|'
                                               'edit_from_location|edit_to_location|back')],
    states={
        'edit_from_address': [
            CallbackQueryHandler(edit_region_or_district_callback, pattern='edit_region|edit_district'),
            MessageHandler(Filters.text & ~Filters.command, message_callback_in_address)
        ],
        'edit_to_address': [
            CallbackQueryHandler(edit_region_or_district_callback, pattern='edit_region|edit_district')],
        'edit_region': [CallbackQueryHandler(edit_region_callback)],
        'edit_district': [CallbackQueryHandler(edit_district_callback)],
        'edit_from_location': [MessageHandler(Filters.location | Filters.text, edit_from_location_callback)],
        'edit_to_location': [CallbackQueryHandler(edit_to_location_callback),
                             MessageHandler(Filters.location | Filters.text, edit_to_location_callback)],

    },
    fallbacks=[],

    map_to_parent={
        -1: -1,
        'EDIT': 'EDIT'
    }
)
