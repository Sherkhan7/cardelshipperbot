from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, ParseMode
from layouts import *
from inlinekeyboards import InlineKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from handlers.newcargoconversation import get_skip_keyboard


def edit_address_callback(update: Update, context: CallbackContext):
    # print('edit_address_callback')

    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data

    if data == 'back':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])
        user_input_data['state'] = 'EDIT'
        state = 'EDIT'

    if data == 'edit_from_address':
        # print('edit_from_address')
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Viloyatni tahrirlash', callback_data='edit_region'),
             InlineKeyboardButton('Tumanni tahrirlash', callback_data='edit_district')],
            [InlineKeyboardButton('« Ortga', callback_data='back')]
        ])

        user_input_data['state'] = 'edit_from_address'
        state = 'edit_from_address'

    if data == 'edit_from_location':
        # print('edit_from_location')

        if None in user_input_data['from_location'].values():
            button_text = "\U0001F4CD Geolokatsiyamni jo'natish"
            reply_text = "Geolokatsiyangizni yuboring:"
            reply_keyboard = ReplyKeyboardMarkup([
                [KeyboardButton(button_text, request_location=True)],
                [KeyboardButton('« Ortga')]
            ], resize_keyboard=True)
        else:
            button_text_1 = "\U0001F4CD Geolokatsiyamni jo'natish"
            button_text_2 = "«Eski geolokatsiyamni o'chirish»"
            reply_text = "Yangi geolokatsiyangizni yuboring:\n\n" \
                         "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"
            reply_keyboard = ReplyKeyboardMarkup([
                [KeyboardButton(button_text_1, request_location=True)],
                [KeyboardButton(button_text_2)],
                [KeyboardButton('« Ortga')]
            ], resize_keyboard=True)
        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
        callback_query.message.reply_text(reply_text, reply_markup=reply_keyboard)
        user_input_data['state'] = 'edit_from_location'
        state = 'edit_from_location'
        return state

    if data == 'edit_to_address':
        # print('edit_to_address')
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Viloyatni tahrirlash', callback_data='edit_region'),
             InlineKeyboardButton('Tumanni tahrirlash', callback_data='edit_district')],
            [InlineKeyboardButton('« Ortga', callback_data='back')]
        ])

        user_input_data['state'] = 'edit_to_address'
        state = 'edit_to_address'

    if data == 'edit_to_location':
        # print('edit_to_location')

        # if user['lang'] == LANGS[0]:
        if None in user_input_data['to_location'].values():
            text = "Yukni jo'natish geolokatsiyasini yuboring."
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('« Ortga', callback_data='back')]
            ])
        else:
            text = "Yukni jo'natish geolokatsiyasini yuboring.\n\n" \
                   "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("«Eski geolokatsiyani o'chirish»", callback_data='next')],
                [InlineKeyboardButton('« Ortga', callback_data='back')]
            ])

        # if user['lang'] == LANGS[1]:
        #     text = 'Отправите геолокацию доставки.\n\n' \
        #            'Или нажмите «next», чтобы пропустить этот шаг'

        user_input_data['state'] = 'edit_to_location'
        state = 'edit_to_location'
        callback_query.answer()
        if user_input_data[PHOTO]:
            callback_query.edit_message_caption(text, reply_markup=inline_keyboard)
        else:
            callback_query.edit_message_text(text, reply_markup=inline_keyboard)
        return state
    callback_query.answer()
    callback_query.edit_message_reply_markup(inline_keyboard)
    return state


def edit_region_or_district_callback(update: Update, context: CallbackContext):
    # print('edit region or district callback')

    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    # print('---state---', user_input_data['state'])
    if data == 'back':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Yuboruvchi manzilini tahrirlash', callback_data='edit_from_address')],
            [InlineKeyboardButton('Yuboruvchi lokatsiyasini tahrirlash', callback_data='edit_from_location')],
            [InlineKeyboardButton('Qabul qiluvchi manzilini tahrirlash', callback_data='edit_to_address')],
            [InlineKeyboardButton('Qabul qiluvchi lokatsiyasini tahrirlash', callback_data='edit_to_location')],
            [InlineKeyboardButton('« Ortga', callback_data='back')],

        ])
        user_input_data['state'] = 'EDIT ADDRESS'
        state = 'edit_address'

    if user_input_data['state'] == 'edit_from_address':

        if data == 'edit_region':
            inline_keyboard = InlineKeyboard('regions_keyboard', 'uz').get_keyboard()
            inline_keyboard['inline_keyboard'].append([InlineKeyboardButton('« Ortga', callback_data='back')])
            state = 'edit_region'

        if data == 'edit_district':
            inline_keyboard = InlineKeyboard('districts_keyboard', 'uz',
                                             region_id=user_input_data['from_region']).get_keyboard()

            state = 'edit_district'

    if user_input_data['state'] == 'edit_to_address':
        if data == 'edit_region':
            inline_keyboard = InlineKeyboard('regions_keyboard', 'uz').get_keyboard()
            inline_keyboard['inline_keyboard'].append([InlineKeyboardButton('« Ortga', callback_data='back')])
            state = 'edit_region'

        if data == 'edit_district':
            inline_keyboard = InlineKeyboard('districts_keyboard', 'uz',
                                             region_id=user_input_data['to_region']).get_keyboard()

            state = 'edit_district'

    callback_query.answer()
    callback_query.edit_message_reply_markup(inline_keyboard)

    return state


def edit_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print(data)

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)
    if data == 'back':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Viloyatni tahrirlash', callback_data='edit_region'),
             InlineKeyboardButton('Tumanni tahrirlash', callback_data='edit_district')],
            [InlineKeyboardButton('« Ortga', callback_data='back')],

        ])
        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        state = user_input_data['state']
        return state
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


def edit_district_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print(data)

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'back_btn':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Viloyatni tahrirlash', callback_data='edit_region'),
             InlineKeyboardButton('Tumanni tahrirlash', callback_data='edit_district')],
            [InlineKeyboardButton('« Ortga', callback_data='back')],

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
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])

        if user_input_data['photo']:
            callback_query.message.edit_caption(caption=layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        state = 'EDIT'
        user_input_data['state'] = state

    callback_query.answer(answer)

    return state


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
        user_input_data['state'] = 'EDIT'
        state = 'EDIT'
        update.message.reply_text('Yuboruvchi geolokatsiyasi tahrirlandi', reply_markup=ReplyKeyboardRemove())

    elif update.message.text == "«Eski geolokatsiyamni o'chirish»":

        user_input_data['from_location'] = {
            'longitude': None,
            'latitude': None
        }
        user_input_data['state'] = 'EDIT'
        state = 'EDIT'
        update.message.reply_text('Yuboruvchi geolokatsiyasi tahrirlandi', reply_markup=ReplyKeyboardRemove())

    elif update.message.text == '« Ortga':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Yuboruvchi manzilini tahrirlash', callback_data='edit_from_address')],
            [InlineKeyboardButton('Yuboruvchi lokatsiyasini tahrirlash', callback_data='edit_from_location')],
            [InlineKeyboardButton('Qabul qiluvchi manzilini tahrirlash', callback_data='edit_to_address')],
            [InlineKeyboardButton('Qabul qiluvchi lokatsiyasini tahrirlash', callback_data='edit_to_location')],
            [InlineKeyboardButton('« Ortga', callback_data='back')],

        ])
        user_input_data['state'] = 'EDIT ADDRESS'
        state = 'edit_address'
        text = get_new_cargo_layout(user_input_data, user)
        update.message.reply_text(update.message.text, reply_markup=ReplyKeyboardRemove())
        if user_input_data['photo']:
            message = update.message.reply_photo(user_input_data['photo']['file_id'], caption=text,
                                                 reply_markup=inline_keyboard,
                                                 parse_mode=ParseMode.HTML)
            user_input_data['message_id'] = message.message_id
        else:
            update.message.reply_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        return state
    else:

        if user['lang'] == LANGS[0]:
            error = 'Geolokatsiyangizni yuboring !!!'

        if user['lang'] == LANGS[1]:
            error = 'Укажите свою геолокацию !!!'

        update.message.reply_text(error, quote=True)

        return 'edit_from_location'

    # logger.info('new_cargo_info: %s', user_input_data)
    text = get_new_cargo_layout(user_input_data, user)
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
        [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
        [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
        [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
    ])
    if user_input_data['photo']:
        message = update.message.reply_photo(user_input_data['photo']['file_id'], caption=text,
                                             reply_markup=inline_keyboard,
                                             parse_mode=ParseMode.HTML)
        user_input_data['message_id'] = message.message_id
    else:
        update.message.reply_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    return state


def edit_to_location_callback(update: Update, context: CallbackContext):
    # print('edit_to_location_callback')
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    callback_query = update.callback_query

    if callback_query:
        data = callback_query.data

        if data == 'back':

            text = get_new_cargo_layout(user_input_data, user)
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('Yuboruvchi manzilini tahrirlash', callback_data='edit_from_address')],
                [InlineKeyboardButton('Yuboruvchi lokatsiyasini tahrirlash', callback_data='edit_from_location')],
                [InlineKeyboardButton('Qabul qiluvchi manzilini tahrirlash', callback_data='edit_to_address')],
                [InlineKeyboardButton('Qabul qiluvchi lokatsiyasini tahrirlash', callback_data='edit_to_location')],
                [InlineKeyboardButton('« Ortga', callback_data='back')],

            ])
            user_input_data['state'] = 'EDIT ADDRESS'
            state = 'edit_address'

            callback_query.answer()
            if user_input_data['photo']:
                callback_query.edit_message_caption(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            else:
                callback_query.edit_message_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

            return state
        if data == 'next':

            user_input_data[TO_LOCATION] = {
                'longitude': None,
                'latitude': None
            }

            text = get_new_cargo_layout(user_input_data, user)
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
                [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
                [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
                [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
            ])
            state = 'EDIT'
            user_input_data['state'] = state

            callback_query.answer('Qabul qiluvchi geolokatsiyasi tahrirlandi')
            if user_input_data['photo']:
                context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
                message = callback_query.message.reply_photo(user_input_data['photo']['file_id'], caption=text,
                                                             reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
                user_input_data['message_id'] = message.message_id
            else:
                callback_query.edit_message_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

            return state
    else:
        if update.message.location:

            longitude = update.message.location.longitude
            latitude = update.message.location.latitude

            user_input_data[TO_LOCATION] = {
                'longitude': longitude,
                'latitude': latitude
            }

        else:

            if user['lang'] == LANGS[0]:
                error = "Geolokatsiya noto'g'ri !!!\n" \
                        "Yukni jo'natish geolokatsiyasini yuboring."

            if user['lang'] == LANGS[1]:
                error = 'Геолокация неправильная !!!\n' \
                        'Отправите геолокацию доставки или нажмите «next» :'

            update.message.reply_text(error, quote=True)

            return 'edit_to_location'

        text = get_new_cargo_layout(user_input_data, user)
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])
        state = 'EDIT'
        user_input_data['state'] = state
        update.message.reply_text('Qabul qiluvchi geolokatsiyasi tahrirlandi')
        if user_input_data['photo']:
            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
            message = update.message.reply_photo(user_input_data['photo']['file_id'], caption=text,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            user_input_data['message_id'] = message.message_id
        else:
            update.message.reply_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        return state


def message_callback_in_address(update: Update, context: CallbackContext):
    print('message callback in address')


edit_address_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_address_callback, pattern='edit_from_address|edit_to_address|'
                                                                      'edit_from_location|edit_to_location|back')],
    states={
        'edit_from_address': [
            CallbackQueryHandler(edit_region_or_district_callback, pattern='edit_region|edit_district|back'),
            MessageHandler(Filters.text & ~Filters.command, message_callback_in_address)
        ],
        'edit_to_address': [
            CallbackQueryHandler(edit_region_or_district_callback, pattern='edit_region|edit_district|back')],
        'edit_region': [CallbackQueryHandler(edit_region_callback)],
        'edit_district': [CallbackQueryHandler(edit_district_callback)],
        'edit_from_location': [
            MessageHandler(Filters.location | Filters.regex(r"^(« Ortga|«Eski geolokatsiyamni o'chirish»|)$|\w"),
                           edit_from_location_callback)],
        'edit_to_location': [CallbackQueryHandler(edit_to_location_callback),
                             MessageHandler(Filters.location | Filters.text, edit_to_location_callback)],

    },
    fallbacks=[],

    map_to_parent={
        -1: -1,
        'EDIT': 'EDIT',
        'edit_address': 'edit_address'
    }
)
