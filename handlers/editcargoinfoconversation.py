import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from filters import phone_number_filter
from inlinekeyboards import InlineKeyboard
from languages import LANGS
from layouts import get_new_cargo_layout, get_phone_number_layout
from inlinekeyboards.inlinekeyboardvariables import *
from globalvariables import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def edit_cargo_info_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'back':
        inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()

        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        state = 'edit'
        user_input_data[STATE] = state

        return state

    if data == 'edit_weight':

        if user[LANG] == LANGS[0]:
            button3_text = "Yuk og'irligini o'chirish"
            button4_text = "Ortga"
            text = "Yuk og'irlik birligini tanlang :\n\n" \
                   "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"

        if user[LANG] == LANGS[1]:
            button3_text = "Удалить вес груза"
            button4_text = "Назад"
            text = "Выберите единицу веса груза :\n\n" \
                   "Или нажмите «удалить», чтобы удалить старую"

        if user[LANG] == LANGS[2]:
            button3_text = "Юк оғирлигини ўчириш"
            button4_text = "Ортга"
            text = "Юк оғирлик бирлигини танланг :\n\n" \
                   "Ёки ескисини ўчириш учун «ўчириш» ни босинг"

        button4_text = '« ' + button4_text
        inline_keyboard = InlineKeyboard(weights_keyboard, user[LANG]).get_keyboard()

        if user_input_data[WEIGHT]:
            inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button3_text, callback_data='delete')])

        else:
            text = text.partition(':')
            text = text[0] + text[1]

        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button4_text, callback_data='back')])

        state = 'edit_weight_unit'

    if data == 'edit_volume':

        if user[LANG] == LANGS[0]:
            button3_text = "Yuk hajmini o'chirish"
            button4_text = "Ortga"
            text = "Yuk hajmini yuboring (raqamda) :\n\n" \
                   "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"

        if user[LANG] == LANGS[1]:
            button3_text = "Удалить объем груза"
            button4_text = "Назад"
            text = "Отправьте объем груза (цифрами) :\n\n" \
                   "Или нажмите «удалить», чтобы удалить старую"

        if user[LANG] == LANGS[2]:
            button3_text = "Юк ҳажмини ўчириш"
            button4_text = "Ортга"
            text = "Юк ҳажмини юборинг (рақамда) :\n\n" \
                   "Ёки ескисини ўчириш учун «ўчириш» ни босинг"

        button4_text = '« ' + button4_text
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button4_text, callback_data='back')],
        ])

        if user_input_data[VOLUME]:
            inline_keyboard['inline_keyboard'].insert(0, [InlineKeyboardButton(button3_text, callback_data='delete')])

        else:
            text = text.partition(':')
            text = text[0] + text[1]

        state = 'edit_volume'

    if data == 'edit_definition':

        if user[LANG] == LANGS[0]:
            button3_text = "Yuk tavsifini o'chirish"
            button4_text = "Ortga"
            text = "Yuk tavsifini yuboring :\n\n" \
                   "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"

        if user[LANG] == LANGS[1]:
            button3_text = "Удалить описание груза"
            button4_text = "Назад"
            text = "Отправить описание груза :\n\n" \
                   "Или нажмите «удалить», чтобы удалить старую"

        if user[LANG] == LANGS[2]:
            button3_text = "Юк тавсифини ўчириш"
            button4_text = "Ортга"
            text = "Юк тавсифини yuboring :\n\n" \
                   "Ёки ескисини ўчириш учун «ўчириш» ни босинг"

        button4_text = '« ' + button4_text
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button4_text, callback_data='back')],
        ])

        if user_input_data[DEFINITION]:
            inline_keyboard['inline_keyboard'].insert(0, [InlineKeyboardButton(button3_text, callback_data='delete')])

        else:
            text = text.partition(':')
            text = text[0] + text[1]

        state = 'edit_definition'

    if data == 'edit_photo':

        if user[LANG] == LANGS[0]:
            button3_text = "Yuk rasmini o'chirish"
            button4_text = "Ortga"
            text = "Yuk rasmini yuboring :\n\n" \
                   "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"

        if user[LANG] == LANGS[1]:
            button3_text = "Удалить фотография груза"
            button4_text = "Назад"
            text = "Отправите фотография груза :\n\n" \
                   "Или нажмите «удалить», чтобы удалить старую"

        if user[LANG] == LANGS[2]:
            button3_text = "Юк расмини ўчириш"
            button4_text = "Ортга"
            text = "Юк расмини юборинг :\n\n" \
                   "Ёки ескисини ўчириш учун «ўчириш» ни босинг"

        button4_text = '« ' + button4_text
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button4_text, callback_data='back')],
        ])

        if user_input_data[PHOTO]:
            inline_keyboard['inline_keyboard'].insert(0, [InlineKeyboardButton(button3_text, callback_data='delete')])

        else:
            text = text.partition(':')
            text = text[0] + text[1]

        state = 'edit_photo'

    if data == 'edit_client_phone':

        phone_number_layout = get_phone_number_layout(user[LANG])

        if user[LANG] == LANGS[0]:
            button_text = "Ortga"

        if user[LANG] == LANGS[1]:
            button_text = "Назад"

        if user[LANG] == LANGS[2]:
            button_text = "Ортга"

        button_text = '« ' + button_text
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button_text, callback_data='back')],
        ])

        text = phone_number_layout

        state = 'edit_client_phone'

    callback_query.answer()

    if user_input_data[PHOTO]:
        callback_query.edit_message_caption(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        callback_query.edit_message_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    user_input_data[STATE] = state

    return state


def edit_weight_unit_callback(update: Update, context: CallbackContext):
    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    callback_query = update.callback_query
    data = callback_query.data

    if data == 'back':
        inline_keyboard = InlineKeyboard(edit_cargo_info_keyboard, user[LANG]).get_keyboard()
        layout = get_new_cargo_layout(user_input_data, user[LANG])

        answer = None
        state = 'edit_cargo_info'

    if data == 'delete':
        user_input_data[WEIGHT] = None

        inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()
        layout = get_new_cargo_layout(user_input_data, user[LANG])

        if user[LANG] == LANGS[0]:
            answer = "Yuk og'irligi tahrirlandi"

        if user[LANG] == LANGS[1]:
            answer = "Вес груза изменен"

        if user[LANG] == LANGS[2]:
            answer = "Юк оғирлиги таҳрирланди"

        answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer
        state = 'edit'

    if callback_query.data == 'kg' or callback_query.data == 't':
        user_input_data['new_weight_unit'] = callback_query.data

        if user[LANG] == LANGS[0]:
            text = "Yangi yuk og'irligini yuboring (raqamda)"
            button_text = "Ortga"

        if user[LANG] == LANGS[1]:
            text = "Отправьте новый вес груза (цифрами)"
            button_text = "Назад"

        if user[LANG] == LANGS[2]:
            text = "Янги юк оғирлигини юборинг (рақамда)"
            button_text = "Ортга"

        text = f'{text} :'
        button_text = '« ' + button_text

        layout = text

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button_text, callback_data='back')],
        ])

        answer = None
        state = 'edit_weight'

    callback_query.answer(answer)

    if user_input_data[PHOTO]:
        callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    user_input_data[STATE] = state

    return state


def edit_weight_callback(update: Update, context: CallbackContext):
    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    callback_query = update.callback_query

    if callback_query:

        if callback_query.data == 'back':

            if 'new_weight_unit' in user_input_data.keys():
                user_input_data.pop('new_weight_unit')

            if user[LANG] == LANGS[0]:
                button3_text = "Yuk og'irligini o'chirish"
                button4_text = "Ortga"
                text = "Yuk og'irlik birligini tanlang :\n\n" \
                       "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"

            if user[LANG] == LANGS[1]:
                button3_text = "Удалить вес груза"
                button4_text = "Назад"
                text = "Выберите единицу веса груза :\n\n" \
                       "Или нажмите «удалить», чтобы удалить старую"

            if user[LANG] == LANGS[2]:
                button3_text = "Юк оғирлигини ўчириш"
                button4_text = "Ортга"
                text = "Юк оғирлик бирлигини танланг :\n\n" \
                       "Ёки ескисини ўчириш учун «ўчириш» ни босинг"

            button4_text = '« ' + button4_text
            inline_keyboard = InlineKeyboard(weights_keyboard, user[LANG]).get_keyboard()

            if user_input_data[WEIGHT]:
                inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button3_text, callback_data='delete')])

            else:
                text = text.partition(':')
                text = text[0] + text[1]

            inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button4_text, callback_data='back')])

            callback_query.answer()

            if user_input_data[PHOTO]:
                callback_query.edit_message_caption(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            else:
                callback_query.edit_message_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

            state = 'edit_weight_unit'
            user_input_data[STATE] = state

            return state

    else:

        text = update.message.text

        if not text.isdigit():
            if user[LANG] == LANGS[0]:
                error_text = "Yuk og'irligini raqamda yuboring"

            if user[LANG] == LANGS[1]:
                error_text = "Отправите  вес груза цифрами"

            if user[LANG] == LANGS[2]:
                error_text = "Юк оғирлигини рақамда юборинг"

            error_text = f'\U000026A0 {error_text} !'

            update.message.reply_text(error_text, quote=True)

            return user_input_data[STATE]

        user_input_data[WEIGHT] = text
        user_input_data[WEIGHT_UNIT] = user_input_data.pop('new_weight_unit')

        inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()
        layout = get_new_cargo_layout(user_input_data, user[LANG])

        if user[LANG] == LANGS[0]:
            answer = "Yuk og'irligi tahrirlandi"

        if user[LANG] == LANGS[1]:
            answer = "Вес груза изменен"

        if user[LANG] == LANGS[2]:
            answer = "Юк оғирлиги таҳрирланди"

        answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer

        update.message.reply_text(answer)
        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop(MESSAGE_ID))

        if user_input_data[PHOTO]:
            message = update.message.reply_photo(user_input_data[PHOTO].get('file_id'), layout,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            message = update.message.reply_html(layout, reply_markup=inline_keyboard)

        state = 'edit'
        user_input_data[STATE] = state
        user_input_data[MESSAGE_ID] = message.message_id

        return state


def edit_volume_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if callback_query:
        data = callback_query.data

        if data == 'back':
            inline_keyboard = InlineKeyboard(edit_cargo_info_keyboard, user[LANG]).get_keyboard()

            answer = None
            state = 'edit_cargo_info'

        if data == 'delete':
            user_input_data[VOLUME] = None
            inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()

            if user[LANG] == LANGS[0]:
                answer = "Yuk hajmi tahrirlandi"

            if user[LANG] == LANGS[1]:
                answer = "Объем груза изменен"

            if user[LANG] == LANGS[2]:
                answer = "Юк ҳажми таҳрирланди"

            answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer
            state = 'edit'

        layout = get_new_cargo_layout(user_input_data, user[LANG])

        callback_query.answer(answer)

        if user_input_data[PHOTO]:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        user_input_data[STATE] = state

        return state

    else:

        text = update.message.text

        if not text.isdigit():
            if user[LANG] == LANGS[0]:
                error_text = "Yuk hajmini raqamda kiriting"

            if user[LANG] == LANGS[1]:
                error_text = "Введите объем груза цифрами"

            if user[LANG] == LANGS[0]:
                error_text = "Юк ҳажмини рақамда киритинг"

            error_text = f'\U000026A0 {error_text} !'
            update.message.reply_text(error_text, quote=True)

            return user_input_data[STATE]

        if user[LANG] == LANGS[0]:
            answer = "Yuk hajmi tahrirlandi"

        if user[LANG] == LANGS[1]:
            answer = "Объем груза изменен"

        if user[LANG] == LANGS[2]:
            answer = "Юк ҳажми таҳрирланди"

        answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer
        update.message.reply_text(answer)

        inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()
        user_input_data[VOLUME] = text

        layout = get_new_cargo_layout(user_input_data, user[LANG])
        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop(MESSAGE_ID))

        if user_input_data[PHOTO]:
            message = update.message.reply_photo(user_input_data[PHOTO].get('file_id'), layout,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            message = update.message.reply_html(layout, reply_markup=inline_keyboard)

        state = 'edit'
        user_input_data[STATE] = state
        user_input_data[MESSAGE_ID] = message.message_id

        return state


def edit_definition_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if callback_query:
        data = callback_query.data

        if data == 'back':
            inline_keyboard = InlineKeyboard(edit_cargo_info_keyboard, user[LANG]).get_keyboard()
            answer = None
            state = 'edit_cargo_info'

        if data == 'delete':
            user_input_data[DEFINITION] = None
            inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()

            if user[LANG] == LANGS[0]:
                answer = "Yuk tavsifi tahrirlandi"

            if user[LANG] == LANGS[1]:
                answer = "Описание груза изменен"

            if user[LANG] == LANGS[2]:
                answer = "Юк тавсифи таҳрирланди"

            answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer
            state = 'edit'

        layout = get_new_cargo_layout(user_input_data, user[LANG])

        callback_query.answer(answer)

        if user_input_data[PHOTO]:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        user_input_data[STATE] = state

    else:

        if user[LANG] == LANGS[0]:
            answer = "Yuk tavsifi tahrirlandi"

        if user[LANG] == LANGS[1]:
            answer = "Описание груза изменен"

        if user[LANG] == LANGS[2]:
            answer = "Юк тавсифи таҳрирланди"

        answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer
        update.message.reply_text(answer)

        user_input_data[DEFINITION] = update.message.text
        inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()
        layout = get_new_cargo_layout(user_input_data, user[LANG])

        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop(MESSAGE_ID))

        if user_input_data[PHOTO]:
            message = update.message.reply_photo(user_input_data[PHOTO].get('file_id'), layout,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            message = update.message.reply_html(layout, reply_markup=inline_keyboard)

        state = 'edit'
        user_input_data[STATE] = state
        user_input_data[MESSAGE_ID] = message.message_id

    return state


def edit_photo_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if callback_query:
        data = callback_query.data

        if data == 'back':
            inline_keyboard = InlineKeyboard(edit_cargo_info_keyboard, user[LANG]).get_keyboard()
            answer = None
            state = 'edit_cargo_info'

            layout = get_new_cargo_layout(user_input_data, user[LANG])
            callback_query.answer(answer)

            if user_input_data[PHOTO]:
                callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            else:
                callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        if data == 'delete':
            user_input_data[PHOTO] = None
            inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()

            if user[LANG] == LANGS[0]:
                answer = "Yuk rasmi tahrirlandi"

            if user[LANG] == LANGS[1]:
                answer = "Фотография груза изменен"

            if user[LANG] == LANGS[2]:
                answer = "Юк расми таҳрирланди"

            answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer
            callback_query.message.reply_text(answer)

            layout = get_new_cargo_layout(user_input_data, user[LANG])

            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop(MESSAGE_ID))
            message = callback_query.message.reply_html(layout, reply_markup=inline_keyboard)

            state = 'edit'
            user_input_data[MESSAGE_ID] = message.message_id

    else:

        cargo_photo = update.message.photo

        if not cargo_photo:

            if user[LANG] == LANGS[0]:
                error_text = "Yuk rasmi yuborilmadi"

            if user[LANG] == LANGS[1]:
                error_text = "Фотография груза не отправлено"

            if user[LANG] == LANGS[2]:
                error_text = "Юк расми юборилмади"

            error_text = f'\U000026A0 {error_text} !'

            update.message.reply_text(error_text, quote=True)

            return user_input_data[STATE]

        user_input_data[PHOTO] = cargo_photo[-1].to_dict()

        if user[LANG] == LANGS[0]:
            answer = "Yuk rasmi tahrirlandi"

        if user[LANG] == LANGS[1]:
            answer = "Фотография груза изменен"

        if user[LANG] == LANGS[2]:
            answer = "Юк расми таҳрирланди"

        answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer
        update.message.reply_text(answer)

        layout = get_new_cargo_layout(user_input_data, user[LANG])
        inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()

        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop(MESSAGE_ID))
        message = update.message.reply_photo(user_input_data[PHOTO].get('file_id'), layout,
                                             reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        state = 'edit'
        user_input_data[MESSAGE_ID] = message.message_id

    user_input_data[STATE] = state
    return state


def edit_client_phone_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if callback_query:
        data = callback_query.data

        if data == 'back':
            inline_keyboard = InlineKeyboard(edit_cargo_info_keyboard, user[LANG]).get_keyboard()
            answer = None
            state = 'edit_cargo_info'

        callback_query.answer(answer)
        layout = get_new_cargo_layout(user_input_data, user[LANG])

        if user_input_data[PHOTO]:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        user_input_data[STATE] = state

        return state

    else:

        contact = update.message.contact
        text = update.message.text

        if contact:
            phone_number = phone_number_filter(contact.phone_number)

        else:
            phone_number = phone_number_filter(text)

        if phone_number:

            user_input_data[USER_PHONE_NUMBER] = phone_number
            inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()

            if user[LANG] == LANGS[0]:
                answer = "Telefon raqami tahrirlandi"

            if user[LANG] == LANGS[1]:
                answer = "Номер телефона изменен"

            if user[LANG] == LANGS[2]:
                answer = "Телефон рақами таҳрирланди"

            answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer
            update.message.reply_text(answer)

            layout = get_new_cargo_layout(user_input_data, user[LANG])

            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop(MESSAGE_ID))

            if user_input_data[PHOTO]:
                message = update.message.reply_photo(user_input_data[PHOTO].get('file_id'), layout,
                                                     reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            else:
                message = update.message.reply_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

            state = 'edit'
            user_input_data[STATE] = state
            user_input_data[MESSAGE_ID] = message.message_id

            return state

        else:

            if user[LANG] == LANGS[0]:
                error_text = "Xato telefon raqami yuborildi"

            if user[LANG] == LANGS[1]:
                error_text = "Номер телефона с ошибкой отправлен"

            if user[LANG] == LANGS[2]:
                error_text = "Хато телефон рақами юборилди"

            error_text = f'\U000026A0 {error_text} !'
            phone_number_layout = get_phone_number_layout(user[LANG])

            update.message.reply_text(error_text, quote=True)
            update.message.reply_html(phone_number_layout)

            return user_input_data[STATE]


edit_cargo_info_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_cargo_info_callback,
                                       pattern='^(edit_weight|edit_volume|edit_definition'
                                               '|edit_photo|edit_client_phone|back)$')],
    states={
        'edit_weight_unit': [CallbackQueryHandler(edit_weight_unit_callback, pattern='^(kg|t|delete|back)$')],

        'edit_weight': [CallbackQueryHandler(edit_weight_callback, pattern='^back$'),
                        MessageHandler(Filters.text & ~Filters.command, edit_weight_callback)],

        'edit_volume': [CallbackQueryHandler(edit_volume_callback, pattern='^(back|delete)$'),
                        MessageHandler(Filters.text & ~Filters.command, edit_volume_callback)],

        'edit_definition': [CallbackQueryHandler(edit_definition_callback, pattern='^(back|delete)$'),
                            MessageHandler(Filters.text & ~Filters.command, edit_definition_callback)],

        'edit_photo': [CallbackQueryHandler(edit_photo_callback, pattern='^(back|delete)$'),
                       MessageHandler(Filters.text & ~Filters.command | Filters.photo, edit_photo_callback)],

        'edit_client_phone': [CallbackQueryHandler(edit_client_phone_callback, pattern='^(back|delete)$'),
                              MessageHandler(Filters.text & ~Filters.command, edit_client_phone_callback)],
    },
    fallbacks=[],

    map_to_parent={
        'edit': 'edit',
        'edit_cargo_info': 'edit_cargo_info'
    }
)
