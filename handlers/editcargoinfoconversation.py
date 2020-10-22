from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from inlinekeyboards import InlineKeyboard
import logging
from units import UNITS
from layouts import get_new_cargo_layout, get_phone_number_layout
from filters import phone_number_filter
from languages import LANGS

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def edit_cargo_info_callback(update: Update, context: CallbackContext):
    # print('edit_cargo_info_callback')
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'back':
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()
        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        state = 'edit'
        user_input_data['state'] = state

        return state

    if data == 'edit_weight':

        button1_text = UNITS[user['lang']][0]
        button2_text = UNITS[user['lang']][1]

        if user['lang'] == LANGS[0]:
            button3_text = 'Yuk og\'irligini o\'chirish'
            button4_text = '« Ortga'
            text = 'Yuk og\'irlik birligini tanlang:\n' \
                   'Yoki eskisini o\'chirish uchun «o\'chirish» ni bosing.'
        if user['lang'] == LANGS[1]:
            button3_text = 'Удалить вес груза'
            button4_text = '« Назад'
            text = 'Выберите единицу веса груза:\n' \
                   'Или нажмите «удалить», чтобы удалить старую.'

        if user_input_data['weight']:
            inline_keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(button1_text, callback_data='kg'),
                    InlineKeyboardButton(button2_text, callback_data='t')
                ],
                [InlineKeyboardButton(button3_text, callback_data='delete')],
                [InlineKeyboardButton(button4_text, callback_data='back')],
            ])
        else:
            text = text.partition(':')
            text = text[0] + text[1]

            inline_keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(button1_text, callback_data='kg'),
                    InlineKeyboardButton(button2_text, callback_data='t')
                ],
                [InlineKeyboardButton(button4_text, callback_data='back')],
            ])

        state = 'edit_weight_unit'

    if data == 'edit_volume':

        if user['lang'] == LANGS[0]:
            button3_text = 'Yuk hajmini o\'chirish'
            button4_text = '« Ortga'
            text = 'Yuk hajmini yuboring (raqamda):\n' \
                   'Yoki eskisini o\'chirish uchun «o\'chirish» ni bosing.'
        if user['lang'] == LANGS[1]:
            button3_text = 'Удалить объем груза'
            button4_text = '« Назад'
            text = 'Отправьте объем груза (цифрами):\n' \
                   'Или нажмите «удалить», чтобы удалить старую.'

        if user_input_data['volume']:
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(button3_text, callback_data='delete')],
                [InlineKeyboardButton(button4_text, callback_data='back')],
            ])
        else:
            text = text.partition(':')
            text = text[0] + text[1]

            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(button4_text, callback_data='back')],
            ])

        state = 'edit_volume'

    if data == 'edit_definition':

        if user['lang'] == LANGS[0]:
            button3_text = 'Yuk tavsifini o\'chirish'
            button4_text = '« Ortga'
            text = 'Yuk tavsifini yuboring:\n' \
                   'Yoki eskisini o\'chirish uchun «o\'chirish» ni bosing.'

        if user['lang'] == LANGS[1]:
            button3_text = 'Удалить описание груза'
            button4_text = '« Назад'
            text = 'Отправить описание груза:\n' \
                   'Или нажмите «удалить», чтобы удалить старую.'

        if user_input_data['definition']:
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(button3_text, callback_data='delete')],
                [InlineKeyboardButton(button4_text, callback_data='back')],
            ])
        else:
            text = text.partition(':')
            text = text[0] + text[1]
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(button4_text, callback_data='back')],
            ])

        state = 'edit_definition'

    if data == 'edit_photo':
        if user['lang'] == LANGS[0]:
            button3_text = 'Yuk rasmini o\'chirish'
            button4_text = '« Ortga'
            text = 'Yuk rasmini yuboring:\n' \
                   'Yoki eskisini o\'chirish uchun «o\'chirish» ni bosing.'
        if user['lang'] == LANGS[1]:
            button3_text = 'Удалить фотография груза'
            button4_text = '« Назад'
            text = 'Отправите фотография груза:\n' \
                   'Или нажмите «удалить», чтобы удалить старую.'

        if user_input_data['photo']:
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(button3_text, callback_data='delete')],
                [InlineKeyboardButton(button4_text, callback_data='back')],
            ])
        else:
            text = text.partition(':')
            text = text[0] + text[1]

            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(button4_text, callback_data='back')],
            ])

        state = 'edit_photo'

    if data == 'edit_receiver_phone':
        phone_number_layout = get_phone_number_layout(user['lang'])
        if user['lang'] == LANGS[0]:
            button3_text = 'Telefon raqamini o\'chirish'
            button4_text = '« Ortga'
            text = 'Yukni qabul qiluvchining telefon raqamini yuboring:\n\n' \
                   'Yoki eskisini o\'chirish uchun «o\'chirish» ni bosing.'
        if user['lang'] == LANGS[1]:
            button3_text = 'Удалить номер телефона'
            button4_text = '« Назад'
            text = 'Отправьте номер телефона получателя груза:\n\n' \
                   'Или нажмите «удалить», чтобы удалить старую.'

        if user_input_data['receiver_phone_number']:
            text += f'\n{phone_number_layout}'
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(button3_text, callback_data='delete')],
                [InlineKeyboardButton(button4_text, callback_data='back')],
            ])
        else:
            text = text.partition(':')
            text = text[0] + text[1]
            text += f'\n{phone_number_layout}'
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(button4_text, callback_data='back')],
            ])

        state = 'edit_receiver_phone'

    callback_query.answer()

    if user_input_data['photo']:
        callback_query.edit_message_caption(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        callback_query.edit_message_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    user_input_data['state'] = state
    return state


def edit_weight_unit_callback(update: Update, context: CallbackContext):
    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    callback_query = update.callback_query
    data = callback_query.data

    if data == 'back':
        inline_keyboard = InlineKeyboard('edit_cargo_info_keyboard', user['lang']).get_keyboard()
        state = 'edit_cargo_info'
        answer = None
        layout = get_new_cargo_layout(user_input_data, user)

    if data == 'delete':
        user_input_data['weight'] = None
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()
        state = 'edit'

        layout = get_new_cargo_layout(user_input_data, user)

        if user['lang'] == LANGS[0]:
            answer = '\U0001F44F\U0001F44F\U0001F44F Yuk og\'irligi tahrirlandi'
        if user['lang'] == LANGS[1]:
            answer = '\U0001F44F\U0001F44F\U0001F44F Вес груза изменен'

    if callback_query.data == 'kg' or callback_query.data == 't':
        user_input_data['new_weight_unit'] = callback_query.data
        state = 'edit_weight'
        answer = None

        if user['lang'] == LANGS[0]:
            text = "Yangi yuk og'irligini yuboring (raqamda):\n"
            button_text = '« Ortga'
        if user['lang'] == LANGS[1]:
            text = 'Отправьте новый вес груза (цифрами):\n'
            button_text = '« Назад'

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button_text, callback_data='back')],
        ])
        layout = text

    callback_query.answer(answer)

    if user_input_data['photo']:
        callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    user_input_data['state'] = state
    return state


def edit_weight_callback(update: Update, context: CallbackContext):
    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]
    # print('state:', user_input_data['state'])

    callback_query = update.callback_query

    if callback_query:

        if callback_query.data == 'back':

            if 'new_weight_unit' in user_input_data.keys():
                user_input_data.pop('new_weight_unit')

            button1_text = UNITS[user['lang']][0]
            button2_text = UNITS[user['lang']][1]

            if user['lang'] == LANGS[0]:
                button3_text = 'Yuk og\'irligini o\'chirish'
                button4_text = '« Ortga'
                text = 'Yuk og\'irlik birligini tanlang:\n' \
                       'Yoki eskisini o\'chirish uchun «o\'chirish» ni bosing.'
            if user['lang'] == LANGS[1]:
                button3_text = 'Удалить вес груза'
                button4_text = '« Назад'
                text = 'Выберите единицу веса груза:\n' \
                       'Или нажмите «удалить», чтобы удалить старую.'

            if user_input_data['weight']:
                inline_keyboard = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(button1_text, callback_data='kg'),
                        InlineKeyboardButton(button2_text, callback_data='t')
                    ],
                    [InlineKeyboardButton(button3_text, callback_data='delete')],
                    [InlineKeyboardButton(button4_text, callback_data='back')],
                ])
            else:
                text = text.partition(':')
                text = text[0] + text[1]

                inline_keyboard = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(button1_text, callback_data='kg'),
                        InlineKeyboardButton(button2_text, callback_data='t')
                    ],
                    [InlineKeyboardButton(button4_text, callback_data='back')],
                ])

            callback_query.answer()
            if user_input_data['photo']:
                callback_query.edit_message_caption(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            else:
                callback_query.edit_message_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

            state = 'edit_weight_unit'
            user_input_data['state'] = state
            return state

    else:

        text = update.message.text

        if not text.isdigit():
            if user['lang'] == LANGS[0]:
                error = "Yuk og'irligini raqamda yuboring !!!"

            if user['lang'] == LANGS[1]:
                error = "Отправите  вес груза цифрами !!!"

            update.message.reply_text(error, quote=True)

            return user_input_data['state']

        user_input_data['weight'] = text
        user_input_data['weight_unit'] = user_input_data.pop('new_weight_unit')

        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()
        state = 'edit'
        user_input_data['state'] = state

        layout = get_new_cargo_layout(user_input_data, user)

        if user['lang'] == LANGS[0]:
            answer = '\U0001F44F\U0001F44F\U0001F44F Yuk og\'irligi tahrirlandi'
        if user['lang'] == LANGS[1]:
            answer = '\U0001F44F\U0001F44F\U0001F44F Вес груза изменен'

        update.message.reply_text(answer)

        if user_input_data['photo']:
            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
            message = update.message.reply_photo(user_input_data['photo'].get('file_id'), layout,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            user_input_data['message_id'] = message.message_id
        else:
            message = update.message.reply_html(layout, reply_markup=inline_keyboard)
            user_input_data['message_id'] = message.message_id

        return state


def edit_volume_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if callback_query:
        data = callback_query.data

        if data == 'back':
            inline_keyboard = InlineKeyboard('edit_cargo_info_keyboard', user['lang']).get_keyboard()
            state = 'edit_cargo_info'
            user_input_data['state'] = state
            answer = None

        if data == 'delete':
            user_input_data['volume'] = None
            inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

            if user['lang'] == LANGS[0]:
                answer = '\U0001F44F\U0001F44F\U0001F44F Yuk hajmi tahrirlandi'
            if user['lang'] == LANGS[1]:
                answer = '\U0001F44F\U0001F44F\U0001F44F Объем груза изменен'

            state = 'edit'
            user_input_data['state'] = state

        layout = get_new_cargo_layout(user_input_data, user)

        callback_query.answer(answer)

        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        return state

    else:

        text = update.message.text

        if not text.isdigit():
            if user['lang'] == LANGS[0]:
                error = "Yuk hajmini raqamda kiriting !!!"
            if user['lang'] == LANGS[1]:
                error = "Введите объем груза цифрами !!!"

            update.message.reply_text(error, quote=True)

            return user_input_data['state']

        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()
        user_input_data['volume'] = text

        if user['lang'] == LANGS[0]:
            answer = '\U0001F44F\U0001F44F\U0001F44F Yuk hajmi tahrirlandi'
        if user['lang'] == LANGS[1]:
            answer = '\U0001F44F\U0001F44F\U0001F44F Объем груза изменен'

        update.message.reply_text(answer)
        layout = get_new_cargo_layout(user_input_data, user)

        if user_input_data['photo']:
            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
            message = update.message.reply_photo(user_input_data['photo'].get('file_id'), layout,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            user_input_data['message_id'] = message.message_id
        else:
            message = update.message.reply_html(layout, reply_markup=inline_keyboard)
            user_input_data['message_id'] = message.message_id

        state = 'edit'
        user_input_data['state'] = state
        return state


def edit_definition_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if callback_query:
        data = callback_query.data

        if data == 'back':
            inline_keyboard = InlineKeyboard('edit_cargo_info_keyboard', user['lang']).get_keyboard()
            answer = None
            state = 'edit_cargo_info'

        if data == 'delete':
            user_input_data['definition'] = None
            inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

            if user['lang'] == LANGS[0]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Yuk tavsifi tahrirlandi"
            if user['lang'] == LANGS[1]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Описание груза изменен."
            state = 'edit'

        layout = get_new_cargo_layout(user_input_data, user)

        callback_query.answer(answer)

        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        user_input_data['state'] = state
        return state

    else:

        user_input_data['definition'] = update.message.text
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()
        layout = get_new_cargo_layout(user_input_data, user)

        if user['lang'] == LANGS[0]:
            answer = "\U0001F44F\U0001F44F\U0001F44F Yuk tavsifi tahrirlandi"
        if user['lang'] == LANGS[1]:
            answer = "\U0001F44F\U0001F44F\U0001F44F Описание груза изменен."

        update.message.reply_text(answer)

        if user_input_data['photo']:
            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
            message = update.message.reply_photo(user_input_data['photo'].get('file_id'), layout,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            user_input_data['message_id'] = message.message_id
        else:
            message = update.message.reply_html(layout, reply_markup=inline_keyboard)
            user_input_data['message_id'] = message.message_id

        state = 'edit'
        user_input_data['state'] = state
        return state


def edit_photo_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if callback_query:
        data = callback_query.data

        if data == 'back':
            inline_keyboard = InlineKeyboard('edit_cargo_info_keyboard', user['lang']).get_keyboard()
            answer = None
            state = 'edit_cargo_info'
            user_input_data['state'] = state

        if data == 'delete':
            user_input_data['photo'] = None
            inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

            if user['lang'] == LANGS[0]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Yuk rasmi tahrirlandi"
            if user['lang'] == LANGS[1]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Фотография груза изменен."

            callback_query.answer(answer)
            layout = get_new_cargo_layout(user_input_data, user)

            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
            message = callback_query.message.reply_html(layout, reply_markup=inline_keyboard)
            user_input_data['message_id'] = message.message_id

            state = 'edit'
            user_input_data['state'] = state
            return state

        layout = get_new_cargo_layout(user_input_data, user)

        callback_query.answer(answer)

        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        return state

    else:
        cargo_photo = update.message.photo

        if len(cargo_photo) > 0:

            user_input_data['photo'] = cargo_photo[-1].to_dict()

        else:

            if user['lang'] == LANGS[0]:
                error = 'Yuk rasmi yuborilmadi !!!\n' \
                        'Yuk rasmini yuboring:'

            if user['lang'] == LANGS[1]:
                error = 'Фотография груза не отправлено !!!\n' \
                        'Отправите фотография груза:'

            update.message.reply_text(error, quote=True)

            return user_input_data['state']

        if user['lang'] == LANGS[0]:
            answer = "\U0001F44F\U0001F44F\U0001F44F Yuk rasmi tahrirlandi"
        if user['lang'] == LANGS[1]:
            answer = "\U0001F44F\U0001F44F\U0001F44F Фотография груза изменен."

        update.message.reply_text(answer)

        layout = get_new_cargo_layout(user_input_data, user)
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

        context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
        message = update.message.reply_photo(user_input_data['photo'].get('file_id'), layout,
                                             reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        user_input_data['message_id'] = message.message_id

        state = 'edit'
        user_input_data['state'] = state
        return state


def edit_receiver_phone_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if callback_query:
        data = callback_query.data

        if data == 'back':
            inline_keyboard = InlineKeyboard('edit_cargo_info_keyboard', user['lang']).get_keyboard()
            answer = None
            state = 'edit_cargo_info'

        if data == 'delete':
            user_input_data['receiver_phone_number'] = None
            inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

            if user['lang'] == LANGS[0]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Yukni qabul qiluvchining telefon raqami tahrirlandi"
            if user['lang'] == LANGS[1]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Номер телефона получателя груза изменен."

            state = 'edit'

        callback_query.answer(answer)
        layout = get_new_cargo_layout(user_input_data, user)

        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        user_input_data['state'] = state
        return state

    else:

        contact = update.message.contact
        text = update.message.text

        if contact:
            phone_number = phone_number_filter(contact.phone_number)

        else:
            phone_number = phone_number_filter(text)

        if phone_number and phone_number != user['phone_number']:
            user_input_data['receiver_phone_number'] = phone_number
            inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

            if user['lang'] == LANGS[0]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Yukni qabul qiluvchining telefon raqami tahrirlandi"
            if user['lang'] == LANGS[1]:
                answer = "\U0001F44F\U0001F44F\U0001F44F Номер телефона получателя груза изменен."

            update.message.reply_text(answer)

            layout = get_new_cargo_layout(user_input_data, user)

            if user_input_data['photo']:
                context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
                message = update.message.reply_photo(user_input_data['photo'].get('file_id'), layout,
                                                     reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
                user_input_data['message_id'] = message.message_id
            else:
                message = update.message.reply_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
                user_input_data['message_id'] = message.message_id

            state = 'edit'
            user_input_data['state'] = state
            return state

        else:

            if user['lang'] == LANGS[0]:
                text = 'Xato telefon raqami yuborildi !!!'
                error_text = 'Siz o\'z telefon raqmingizni yubordingiz !!!\n\n' \
                             'Yukni qabul qiluvchining telefon raqamini yuboring:'
            if user['lang'] == LANGS[1]:
                text = 'Номер телефона с ошибкой отправлен !!!'
                error_text = 'Вы отправили свой номер телефона !!!\n' \
                             'Отправить номер телефона получателя груза:'

            if phone_number == user['phone_number']:
                text = error_text

            phone_number_layout = get_phone_number_layout(user['lang'])
            text += f'\n{phone_number_layout}'

            update.message.reply_html(text, quote=True)

            return user_input_data['state']


edit_cargo_info_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_cargo_info_callback,
                                       pattern='^(edit_weight|edit_volume|edit_definition'
                                               '|edit_photo|edit_receiver_phone|back)$')],
    states={
        'edit_weight_unit': [CallbackQueryHandler(edit_weight_unit_callback, pattern='^(kg|t|back|delete)$')],

        'edit_weight': [CallbackQueryHandler(edit_weight_callback, pattern='^back'),
                        MessageHandler(Filters.text & ~Filters.command, edit_weight_callback)],
        'edit_volume': [CallbackQueryHandler(edit_volume_callback, pattern='^(back|delete)$'),
                        MessageHandler(Filters.text & ~Filters.command, edit_volume_callback)],
        'edit_definition': [CallbackQueryHandler(edit_definition_callback, pattern='^(back|delete)$'),
                            MessageHandler(Filters.text & ~Filters.command, edit_definition_callback)],
        'edit_photo': [CallbackQueryHandler(edit_photo_callback, pattern='^(back|delete)$'),
                       MessageHandler(Filters.text & ~Filters.command | Filters.photo, edit_photo_callback)],
        'edit_receiver_phone': [CallbackQueryHandler(edit_receiver_phone_callback, pattern='^(back|delete)$'),
                                MessageHandler(Filters.text & ~Filters.command, edit_receiver_phone_callback)],

    },
    fallbacks=[],

    map_to_parent={
        'edit': 'edit',
        'edit_cargo_info': 'edit_cargo_info'
    }
)
