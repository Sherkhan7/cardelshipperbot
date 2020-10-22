from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, ParseMode
from layouts import *
from inlinekeyboards import InlineKeyboard


def edit_address_callback(update: Update, context: CallbackContext):
    # print('edit_address_callback')

    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'back':
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()
        state = 'edit'
        user_input_data['state'] = state

    if data == 'edit_from_address' or data == 'edit_to_address':

        if user['lang'] == LANGS[0]:
            button1_text = 'Viloyatni tahrirlash'
            button2_text = 'Tumanni tahrirlash'
            button3_text = '« Ortga'
        if user['lang'] == LANGS[1]:
            button1_text = 'Изменить область'
            button2_text = 'Изменить район'
            button3_text = '« Назад'

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button1_text, callback_data='edit_region'),
             InlineKeyboardButton(button2_text, callback_data='edit_district')],
            [InlineKeyboardButton(button3_text, callback_data='back')]
        ])

        if data == 'edit_from_address':
            state = 'edit_from_address'

        if data == 'edit_to_address':
            state = 'edit_to_address'

        user_input_data['state'] = state

    if data == 'edit_from_location':
        if user['lang'] == LANGS[0]:
            button1_text = "\U0001F4CD Geolokatsiyamni jo'natish"
            button2_text = '« Ortga'
            button3_text = "«Eski geolokatsiyamni o'chirish»"
            text = "Geolokatsiyangizni yuboring:\n\n" \
                   "Yoki eskisini o\'chirish uchun «o\'chirish» ni bosing"
        if user['lang'] == LANGS[1]:
            button1_text = "\U0001F4CD Отправить мою геолокацию"
            button2_text = '« Назад'
            button3_text = '«Удалить мою старую геолокацию»'
            text = "Отправьте свою геолокацию:\n\n" \
                   "Или нажмите «удалить», чтобы удалить старую"

        if not user_input_data['from_location']:
            reply_keyboard = ReplyKeyboardMarkup([
                [KeyboardButton(button1_text, request_location=True)],
                [KeyboardButton(button2_text)]
            ], resize_keyboard=True)
            text = text.partition(':')
            text = text[0] + text[1]
        else:
            reply_keyboard = ReplyKeyboardMarkup([
                [KeyboardButton(button1_text, request_location=True)],
                [KeyboardButton(button3_text)],
                [KeyboardButton(button2_text)]
            ], resize_keyboard=True)

        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
        callback_query.message.reply_text(text, reply_markup=reply_keyboard)
        state = 'edit_from_location'
        user_input_data['state'] = state

        return state

    if data == 'edit_to_location':

        if user['lang'] == LANGS[0]:
            button1_text = '«Eski geolokatsiyani o\'chirish»'
            button2_text = '« Ortga'
            text = 'Yukni jo\'natish geolokatsiyasini yuboring:\n\n' \
                   'Yoki eskisini o\'chirish uchun «o\'chirish» ni bosing.'
        if user['lang'] == LANGS[1]:
            button1_text = '«Удалить старую геолокацию»'
            button2_text = '« Назад'
            text = "Отправите геолокацию доставки:\n\n" \
                   "Или нажмите «удалить», чтобы удалить старую."

        if not user_input_data['to_location']:
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(button2_text, callback_data='back')]
            ])
            text = text.partition(':')
            text = text[0] + text[1]
        else:
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(button1_text, callback_data='delete')],
                [InlineKeyboardButton(button2_text, callback_data='back')]
            ])

        state = 'edit_to_location'
        user_input_data['state'] = state

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

    user = context.bot_data[update.effective_user.id]
    user_input_data = context.user_data

    # print('---state---', user_input_data['state'])
    if data == 'back':
        inline_keyboard = InlineKeyboard('edit_address_keyboard', user['lang']).get_keyboard()
        state = 'edit_address'
        user_input_data['state'] = state
        text = get_new_cargo_layout(user_input_data, user)

    if data == 'edit_region':

        if user['lang'] == LANGS[0]:
            buton_text = '« Ortga'
            text = "Viloyatni tanlang:"
        if user['lang'] == LANGS[1]:
            buton_text = '« Назад'
            text = "Выберите область:"

        inline_keyboard = InlineKeyboard('regions_keyboard', user['lang']).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(buton_text, callback_data='back')])

        state = data

    if data == 'edit_district':

        if user['lang'] == LANGS[0]:
            text = "Tumanni tanlang:"
        if user['lang'] == LANGS[1]:
            text = "Выберите район:"

        if user_input_data['state'] == 'edit_from_address':
            region_id = user_input_data['from_region']

        elif user_input_data['state'] == 'edit_to_address':
            region_id = user_input_data['to_region']

        inline_keyboard = InlineKeyboard('districts_keyboard', user['lang'], region_id=region_id).get_keyboard()
        state = data

    callback_query.answer()
    if user_input_data['photo']:
        callback_query.edit_message_caption(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        callback_query.edit_message_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    return state


def edit_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print(data)

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'back':
        layout = get_new_cargo_layout(user_input_data, user)

        if user['lang'] == LANGS[0]:
            button1_text = 'Viloyatni tahrirlash'
            button2_text = 'Tumanni tahrirlash'
            button3_text = '« Ortga'
        if user['lang'] == LANGS[1]:
            button1_text = 'Изменить область'
            button2_text = 'Изменить район'
            button3_text = '« Назад'

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button1_text, callback_data='edit_region'),
             InlineKeyboardButton(button2_text, callback_data='edit_district')],
            [InlineKeyboardButton(button3_text, callback_data='back')]
        ])
        callback_query.answer()

        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        return user_input_data['state']

    region_id = int(data.replace("region_id_", ""))

    if user_input_data['state'] == 'edit_from_address':
        user_input_data['new_from_region'] = region_id

    if user_input_data['state'] == 'edit_to_address':
        user_input_data['new_to_region'] = region_id

    # logger.info('new_cargo_info: %s', user_input_data)

    inline_keyboard = InlineKeyboard('districts_keyboard', user['lang'], region_id=region_id)

    callback_query.answer()
    callback_query.edit_message_reply_markup(reply_markup=inline_keyboard.get_keyboard())

    return 'edit_district'


def edit_district_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print(data)

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'back_btn':
        if user['lang'] == LANGS[0]:
            button1_text = 'Viloyatni tahrirlash'
            button2_text = 'Tumanni tahrirlash'
            button3_text = '« Ortga'
        if user['lang'] == LANGS[1]:
            button1_text = 'Изменить область'
            button2_text = 'Изменить район'
            button3_text = '« Назад'

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button1_text, callback_data='edit_region'),
             InlineKeyboardButton(button2_text, callback_data='edit_district')],
            [InlineKeyboardButton(button3_text, callback_data='back')]
        ])

        state = user_input_data['state']
        answer = None

        if state == 'edit_from_address':
            key = 'new_from_region'
        elif state == 'edit_to_address':
            key = 'new_to_region'

        if key in user_input_data.keys():
            user_input_data.pop(key)

        layout = get_new_cargo_layout(user_input_data, user)

        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    else:

        district_id = int(data.replace("district_id_", ""))
        state = user_input_data['state']

        if state == 'edit_from_address':
            new_key = 'new_from_region'
            key = FROM_REGION
            user_input_data[FROM_DISTRICT] = district_id

            if user['lang'] == LANGS[0]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Yuboruvchi manzili tahrirlandi."
            if user['lang'] == LANGS[1]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Адрес отправителя изменен."

        if state == 'edit_to_address':
            new_key = 'new_to_region'
            key = TO_REGION
            user_input_data[TO_DISTRICT] = district_id

            if user['lang'] == LANGS[0]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Qabul qiluvchi manzili tahrirlandi."
            if user['lang'] == LANGS[1]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Адрес получателя изменен."

        if new_key in user_input_data.keys():
            user_input_data[key] = user_input_data.pop(new_key)

        layout = get_new_cargo_layout(user_input_data, user)
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

        if user_input_data['photo']:
            callback_query.edit_message_caption(caption=layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        state = 'edit'
        user_input_data['state'] = state

    callback_query.answer(answer)

    return state


def edit_from_location_callback(update: Update, context: CallbackContext):
    user = context.bot_data[update.effective_user.id]
    user_input_data = context.user_data

    text = update.message.text

    if user['lang'] == LANGS[0]:
        reply_text = '\U0001F44F\U0001F44F\U0001F44F Yuboruvchi geolokatsiyasi tahrirlandi.'
    if user['lang'] == LANGS[1]:
        reply_text = '\U0001F44F\U0001F44F\U0001F44F Геолокация отправителя изменена.'

    if update.message.location:

        longitude = update.message.location.longitude
        latitude = update.message.location.latitude

        user_input_data['from_location'] = {
            'longitude': longitude,
            'latitude': latitude
        }
        update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())

        state = 'edit'
        user_input_data['state'] = state
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

    elif text == '«Eski geolokatsiyamni o\'chirish»' or text == '«Удалить мою старую геолокацию»':

        user_input_data['from_location'] = {
            'longitude': None,
            'latitude': None
        }

        update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())

        state = 'edit'
        user_input_data['state'] = state
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

    elif text == '« Ortga' or text == '« Назад':
        update.message.reply_text(update.message.text, reply_markup=ReplyKeyboardRemove())

        state = 'edit_address'
        user_input_data['state'] = state
        inline_keyboard = InlineKeyboard('edit_address_keyboard', user['lang']).get_keyboard()

    else:

        if user['lang'] == LANGS[0]:
            error = 'Geolokatsiyangizni yuboring !!!'

        if user['lang'] == LANGS[1]:
            error = 'Отправьте свою геолокацию !!!'

        update.message.reply_text(error, quote=True)

        return 'edit_from_location'

    # logger.info('new_cargo_info: %s', user_input_data)
    layout = get_new_cargo_layout(user_input_data, user)

    if user_input_data['photo']:
        message = update.message.reply_photo(user_input_data['photo']['file_id'], caption=layout,
                                             reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        user_input_data['message_id'] = message.message_id
    else:
        message = update.message.reply_html(layout, reply_markup=inline_keyboard)
        user_input_data['message_id'] = message.message_id

    return state


def edit_to_location_callback(update: Update, context: CallbackContext):
    # print('edit_to_location_callback')
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    callback_query = update.callback_query

    if callback_query:
        data = callback_query.data

        if data == 'back':
            text = get_new_cargo_layout(user_input_data, user)
            inline_keyboard = InlineKeyboard('edit_address_keyboard', user['lang']).get_keyboard()
            answer = None
            state = 'edit_address'
            user_input_data['state'] = state

        if data == 'delete':
            user_input_data[TO_LOCATION] = {
                'longitude': None,
                'latitude': None
            }

            text = get_new_cargo_layout(user_input_data, user)
            inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

            if user['lang'] == LANGS[0]:
                answer = '\U0001F44F\U0001F44F\U0001F44F Qabul qiluvchi geolokatsiyasi tahrirlandi.'
            if user['lang'] == LANGS[1]:
                answer = '\U0001F44F\U0001F44F\U0001F44F Геолокация получателя изменена.'

            state = 'edit'
            user_input_data['state'] = state

        callback_query.answer(answer)

        if user_input_data['photo']:
            callback_query.edit_message_caption(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
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
                error = 'Yukni jo\'natish geolokatsiyasini yuboring !!!'

            if user['lang'] == LANGS[1]:
                error = 'Отправите геолокацию доставки !!!'

            update.message.reply_text(error, quote=True)

            return 'edit_to_location'

        text = get_new_cargo_layout(user_input_data, user)
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

        if user['lang'] == LANGS[0]:
            answer = '\U0001F44F\U0001F44F\U0001F44F Qabul qiluvchi geolokatsiyasi tahrirlandi.'
        if user['lang'] == LANGS[1]:
            answer = '\U0001F44F\U0001F44F\U0001F44F Геолокация получателя изменена.'

        update.message.reply_text(answer)

        if user_input_data['photo']:
            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
            message = update.message.reply_photo(user_input_data['photo']['file_id'], caption=text,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            user_input_data['message_id'] = message.message_id
        else:
            message = update.message.reply_html(text, reply_markup=inline_keyboard)
            user_input_data['message_id'] = message.message_id

        state = 'edit'
        user_input_data['state'] = state

        return state


edit_address_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_address_callback, pattern='^(edit_from_address|edit_to_address|'
                                                                      'edit_from_location|edit_to_location|back)$')],
    states={
        'edit_from_address': [
            CallbackQueryHandler(edit_region_or_district_callback, pattern='^(edit_region|edit_district|back)$')
        ],
        'edit_to_address': [
            CallbackQueryHandler(edit_region_or_district_callback, pattern='^(edit_region|edit_district|back)$')],
        'edit_region': [CallbackQueryHandler(edit_region_callback)],
        'edit_district': [CallbackQueryHandler(edit_district_callback)],
        'edit_from_location': [
            MessageHandler(Filters.location | Filters.regex(
                r"^(« Ortga|« Назад|«Eski geolokatsiyamni o'chirish»|«Удалить мою старую геолокацию»)$|\w"),
                           edit_from_location_callback)],
        'edit_to_location': [CallbackQueryHandler(edit_to_location_callback, pattern='^(back|delete)$'),
                             MessageHandler(Filters.location | Filters.text, edit_to_location_callback)],

    },
    fallbacks=[],

    map_to_parent={
        'edit': 'edit',
        'edit_address': 'edit_address'
    }
)
