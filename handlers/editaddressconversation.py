from telegram import (Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup,
                      KeyboardButton, ParseMode)
from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from inlinekeyboards import InlineKeyboard
from layouts import get_new_cargo_layout
from languages import LANGS
from inlinekeyboards.inlinekeyboardvariables import *
from globalvariables import *


def edit_address_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'back':
        inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()

        state = 'edit'
        user_input_data[STATE] = state

    if data == 'edit_from_address' or data == 'edit_to_address':

        if user[LANG] == LANGS[0]:
            button1_text = "Viloyatni tahrirlash"
            button2_text = "Tumanni tahrirlash"
            button3_text = "Ortga"

        if user[LANG] == LANGS[1]:
            button1_text = "Изменить область"
            button2_text = "Изменить район"
            button3_text = "Назад"

        if user[LANG] == LANGS[2]:
            button1_text = "Вилоятни таҳрирлаш"
            button2_text = "Туманни таҳрирлаш"
            button3_text = "Ортга"

        button3_text = '« ' + button3_text

        inline_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='edit_region'),
                InlineKeyboardButton(button2_text, callback_data='edit_district')
            ],

            [InlineKeyboardButton(button3_text, callback_data='back')]
        ])

        if data == 'edit_from_address':
            state = 'edit_from_address'

        if data == 'edit_to_address':
            state = 'edit_to_address'

        user_input_data[STATE] = state

    if data == 'edit_from_location':

        if user[LANG] == LANGS[0]:
            button1_text = "Geolokatsiyamni jo'natish"
            button2_text = "Ortga"
            button3_text = "Eski geolokatsiyamni o'chirish"
            text = "Geolokatsiyangizni yuboring:\n\n" \
                   "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"

        if user[LANG] == LANGS[1]:
            button1_text = "Отправить мою геолокацию"
            button2_text = "Назад"
            button3_text = "Удалить мою старую геолокацию"
            text = "Отправьте свою геолокацию:\n\n" \
                   "Или нажмите «удалить», чтобы удалить старую"

        if user[LANG] == LANGS[2]:
            button1_text = "Геолокациямни жўнатиш"
            button2_text = "Ортга"
            button3_text = "Ески геолокациямни ўчириш"
            text = "Геолокациянгизни юборинг:\n\n" \
                   "Ёки ескисини ўчириш учун «ўчириш» ни босинг"

        button1_text = '\U0001F4CD ' + button1_text
        button2_text = '« ' + button2_text
        button3_text = f'«{button3_text}»'

        if not user_input_data[FROM_LOCATION]:

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
        user_input_data[STATE] = state

        return state

    if data == 'edit_to_location':

        if user[LANG] == LANGS[0]:
            button1_text = "Eski geolokatsiyani o'chirish"
            button2_text = "Ortga"
            text = "Yukni jo'natish geolokatsiyasini yuboring:\n\n " \
                   "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"

        if user[LANG] == LANGS[1]:
            button1_text = "Удалить старую геолокацию"
            button2_text = "Назад"
            text = "Отправите геолокацию доставки:\n\n" \
                   "Или нажмите «удалить», чтобы удалить старую"

        if user[LANG] == LANGS[2]:
            button1_text = "Ески геолокацияни ўчириш"
            button2_text = "Ортга"
            text = "Юкни жўнатиш геолокациясини юборинг:\n\n" \
                   "Ёки ескисини ўчириш учун «ўчириш» ни босинг"

        button1_text = f'«{button1_text}»'
        button2_text = '« ' + button2_text

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

        callback_query.answer()

        if user_input_data[PHOTO]:
            callback_query.edit_message_caption(text, reply_markup=inline_keyboard)
        else:
            callback_query.edit_message_text(text, reply_markup=inline_keyboard)

        state = 'edit_to_location'
        user_input_data[STATE] = state

        return state

    callback_query.answer()
    callback_query.edit_message_reply_markup(inline_keyboard)
    return state


def edit_region_or_district_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user = context.bot_data[update.effective_user.id]
    user_input_data = context.user_data

    if data == 'back':
        inline_keyboard = InlineKeyboard(edit_address_keyboard, user[LANG]).get_keyboard()
        text = get_new_cargo_layout(user_input_data, user[LANG])

        state = 'edit_address'
        user_input_data[STATE] = state

    if data == 'edit_region':

        if user[LANG] == LANGS[0]:
            buton_text = "Ortga"
            text = "Viloyatni tanlang"

        if user[LANG] == LANGS[1]:
            buton_text = "Назад"
            text = "Выберите область"

        if user[LANG] == LANGS[2]:
            buton_text = "Ортга"
            text = "Вилоятни танланг"

        text = f'{text} :'
        buton_text = '« ' + buton_text

        inline_keyboard = InlineKeyboard(regions_keyboard, user[LANG]).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(buton_text, callback_data='back')])

        state = 'edit_region'

    if data == 'edit_district':

        if user[LANG] == LANGS[0]:
            text = "Tumanni tanlang"

        if user[LANG] == LANGS[1]:
            text = "Выберите район"

        if user[LANG] == LANGS[2]:
            text = "Туманни танланг"

        text = f'{text} :'

        if user_input_data[STATE] == 'edit_from_address':
            region_id = user_input_data[FROM_REGION]

        elif user_input_data[STATE] == 'edit_to_address':
            region_id = user_input_data[TO_REGION]

        inline_keyboard = InlineKeyboard(districts_keyboard, user[LANG], region_id=region_id).get_keyboard()

        state = 'edit_district'

    callback_query.answer()

    if user_input_data[PHOTO]:
        callback_query.edit_message_caption(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        callback_query.edit_message_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    return state


def edit_region_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'back':
        layout = get_new_cargo_layout(user_input_data, user[LANG])

        if user[LANG] == LANGS[0]:
            button1_text = "Viloyatni tahrirlash"
            button2_text = "Tumanni tahrirlash"
            button3_text = "Ortga"

        if user[LANG] == LANGS[1]:
            button1_text = "Изменить область"
            button2_text = "Изменить район"
            button3_text = "Назад"

        if user[LANG] == LANGS[2]:
            button1_text = "Вилоятни таҳрирлаш"
            button2_text = "Туманни таҳрирлаш"
            button3_text = "Ортга"

        button3_text = '« ' + button3_text

        inline_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='edit_region'),
                InlineKeyboardButton(button2_text, callback_data='edit_district')
            ],
            [
                InlineKeyboardButton(button3_text, callback_data='back')
            ]
        ])

        callback_query.answer()

        if user_input_data[PHOTO]:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        return user_input_data[STATE]

    region_id = data

    if user_input_data[STATE] == 'edit_from_address':
        user_input_data['new_from_region'] = region_id

    if user_input_data[STATE] == 'edit_to_address':
        user_input_data['new_to_region'] = region_id

    # logger.info('new_cargo_info: %s', user_input_data)

    callback_query.answer()

    inline_keyboard = InlineKeyboard(districts_keyboard, user[LANG], region_id=region_id).get_keyboard()
    callback_query.edit_message_reply_markup(reply_markup=inline_keyboard)

    return 'edit_district'


def edit_district_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'back_btn':

        if user[LANG] == LANGS[0]:
            button1_text = "Viloyatni tahrirlash"
            button2_text = "Tumanni tahrirlash"
            button3_text = "Ortga"

        if user[LANG] == LANGS[1]:
            button1_text = "Изменить область"
            button2_text = "Изменить район"
            button3_text = "Назад"

        if user[LANG] == LANGS[2]:
            button1_text = "Вилоятни таҳрирлаш"
            button2_text = "Туманни таҳрирлаш"
            button3_text = "Ортга"

        button3_text = '« ' + button3_text

        inline_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='edit_region'),
                InlineKeyboardButton(button2_text, callback_data='edit_district')
            ],
            [
                InlineKeyboardButton(button3_text, callback_data='back')
            ]
        ])

        state = user_input_data[STATE]
        answer = None

        if state == 'edit_from_address':
            key = 'new_from_region'

        elif state == 'edit_to_address':
            key = 'new_to_region'

        if key in user_input_data.keys():
            user_input_data.pop(key)

        layout = get_new_cargo_layout(user_input_data, user[LANG])

        if user_input_data[PHOTO]:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    else:

        district_id = data

        state = user_input_data[STATE]

        if state == 'edit_from_address':

            new_key = 'new_from_region'
            key = FROM_REGION
            user_input_data[FROM_DISTRICT] = district_id

            if user[LANG] == LANGS[0]:
                answer = "Yuboruvchi manzili tahrirlandi"

            if user[LANG] == LANGS[1]:
                answer = "Адрес отправителя изменен"

            if user[LANG] == LANGS[2]:
                answer = "Юборувчи манзили таҳрирланди"

        if state == 'edit_to_address':

            new_key = 'new_to_region'
            key = TO_REGION
            user_input_data[TO_DISTRICT] = district_id

            if user[LANG] == LANGS[0]:
                answer = "Qabul qiluvchi manzili tahrirlandi"

            if user[LANG] == LANGS[1]:
                answer = "Адрес получателя изменен"

            if user[LANG] == LANGS[2]:
                answer = "Қабул қилувчи манзили таҳрирланди"

        answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer

        if new_key in user_input_data.keys():
            user_input_data[key] = user_input_data.pop(new_key)

        layout = get_new_cargo_layout(user_input_data, user[LANG])
        inline_keyboard = InlineKeyboard('edit_keyboard', user[LANG]).get_keyboard()

        if user_input_data[PHOTO]:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        state = 'edit'
        user_input_data[STATE] = state

    callback_query.answer(answer)

    return state


def edit_from_location_callback(update: Update, context: CallbackContext):
    text = update.message.text

    user = context.bot_data[update.effective_user.id]
    user_input_data = context.user_data

    if user[LANG] == LANGS[0]:
        reply_text = "Yuboruvchi geolokatsiyasi tahrirlandi"

    if user[LANG] == LANGS[1]:
        reply_text = "Геолокация отправителя изменена"

    if user[LANG] == LANGS[2]:
        reply_text = "Юборувчи геолокацияси таҳрирланди"

    reply_text = '\U0001F44F\U0001F44F\U0001F44F ' + reply_text

    if update.message.location:

        longitude = update.message.location.longitude
        latitude = update.message.location.latitude

        user_input_data[FROM_LOCATION] = {
            'longitude': longitude,
            'latitude': latitude
        }

        update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())

        inline_keyboard = InlineKeyboard('edit_keyboard', user[LANG]).get_keyboard()

        state = 'edit'
        user_input_data[STATE] = state

    elif text == "«Eski geolokatsiyamni o'chirish»" or text == '«Удалить мою старую геолокацию»' or \
            text == "«Ески геолокациямни ўчириш»":

        user_input_data[FROM_LOCATION] = None

        update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())

        inline_keyboard = InlineKeyboard('edit_keyboard', user[LANG]).get_keyboard()

        state = 'edit'
        user_input_data[STATE] = state

    elif text == "« Ortga" or text == "« Назад" or text == "« Ортга":

        update.message.reply_text(update.message.text, reply_markup=ReplyKeyboardRemove())

        inline_keyboard = InlineKeyboard(edit_address_keyboard, user[LANG]).get_keyboard()

        state = 'edit_address'
        user_input_data[STATE] = state

    else:

        if user[LANG] == LANGS[0]:
            error_text = "Geolokatsiyangizni yuboring"

        if user[LANG] == LANGS[1]:
            error_text = "Отправьте свою геолокацию"

        if user[LANG] == LANGS[2]:
            error_text = "Геолокациянгизни юборинг"

        error_text = f'\U000026A0 {error_text} !'

        update.message.reply_text(error_text, quote=True)

        return user_input_data[STATE]

    # logger.info('new_cargo_info: %s', user_input_data)
    layout = get_new_cargo_layout(user_input_data, user[LANG])

    if user_input_data[PHOTO]:
        message = update.message.reply_photo(user_input_data[PHOTO]['file_id'], caption=layout,
                                             reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        message = update.message.reply_html(layout, reply_markup=inline_keyboard)

    user_input_data[MESSAGE_ID] = message.message_id

    return state


def edit_to_location_callback(update: Update, context: CallbackContext):
    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    callback_query = update.callback_query

    if callback_query:

        data = callback_query.data
        layout = get_new_cargo_layout(user_input_data, user[LANG])

        if data == 'back':
            inline_keyboard = InlineKeyboard(edit_address_keyboard, user[LANG]).get_keyboard()
            answer = None

            state = 'edit_address'

        if data == 'delete':
            user_input_data[TO_LOCATION] = None

            inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()

            if user[LANG] == LANGS[0]:
                answer = "Qabul qiluvchi geolokatsiyasi tahrirlandi"

            if user[LANG] == LANGS[1]:
                answer = "Геолокация получателя изменена"

            if user[LANG] == LANGS[2]:
                answer = "Қабул қилувчи геолокацияси таҳрирланди"

            answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer

            state = 'edit'

        callback_query.answer(answer)

        if user_input_data[PHOTO]:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        user_input_data[STATE] = state

        return state

    else:

        if update.message.location:

            longitude = update.message.location.longitude
            latitude = update.message.location.latitude

            user_input_data[TO_LOCATION] = {
                'longitude': longitude,
                'latitude': latitude
            }

            if user[LANG] == LANGS[0]:
                answer = "Qabul qiluvchi geolokatsiyasi tahrirlandi"

            if user[LANG] == LANGS[1]:
                answer = "Геолокация получателя изменена"

            if user[LANG] == LANGS[2]:
                answer = "Қабул қилувчи геолокацияси таҳрирланди"

            answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer

            update.message.reply_text(answer)

            layout = get_new_cargo_layout(user_input_data, user[LANG])
            inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()

            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))

            if user_input_data[PHOTO]:
                message = update.message.reply_photo(user_input_data[PHOTO]['file_id'], caption=layout,
                                                     reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            else:
                message = update.message.reply_html(layout, reply_markup=inline_keyboard)

            state = 'edit'
            user_input_data[STATE] = state
            user_input_data[MESSAGE_ID] = message.message_id

            return state

        else:

            if user[LANG] == LANGS[0]:
                error_text = "Yukni jo'natish geolokatsiyasini yuboring"

            if user[LANG] == LANGS[1]:
                error_text = "Отправите геолокацию доставки"

            if user[LANG] == LANGS[2]:
                error_text = "Юкни жўнатиш геолокациясини юборинг"

            error_text = f'\U000026A0 {error_text} !'
            update.message.reply_text(error_text, quote=True)

            return user_input_data[STATE]


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
                r'^(« Ortga|« Назад|«Eski geolokatsiyamni o\'chirish»|«Удалить мою старую геолокацию»)$|\w'),
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
