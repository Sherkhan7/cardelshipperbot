from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from DB import *
from inlinekeyboards import InlineKeyboard
from handlers.newcargoconversation import get_skip_keyboard
import logging
from units import UNITS
from layouts import get_new_cargo_layout, get_phone_number_layout
from filters import phone_number_filter

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def edit_cargo_info_callback(update: Update, context: CallbackContext):
    # print('edit_cargo_info_callback')

    callback_query = update.callback_query
    data = callback_query.data

    # print(data)
    user_input_data = context.user_data

    if data == 'back':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])

        callback_query.edit_message_reply_markup(inline_keyboard)

        user_input_data['state'] = 'EDIT'
        state = 'EDIT'

    if data == 'edit_weight':
        text_2 = "Yuk og'irlik birligini tanlang:"
        button1_text = UNITS['uz'][0]
        button2_text = UNITS['uz'][1]

        inline_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='kg'),
                InlineKeyboardButton(button2_text, callback_data='t')
            ],
            [InlineKeyboardButton('« Ortga', callback_data='back')],
        ])

        if user_input_data['photo']:
            callback_query.edit_message_caption(text_2, reply_markup=inline_keyboard)
        else:
            callback_query.edit_message_text(text_2, reply_markup=inline_keyboard)

        state = 'edit_weight'
        user_input_data['state'] = 'edit_weight_unit'

    if data == 'edit_volume':
        if user_input_data['volume']:
            text_1 = "Yuk hajmini yuboring (raqamda):\n" \
                     "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Hajmni o'chirish", callback_data='next')],
                [InlineKeyboardButton('« Ortga', callback_data='back')],
            ])
        else:
            text_1 = "Yuk hajmini yuboring (raqamda):\n"
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('« Ortga', callback_data='back')],
            ])
        if user_input_data['photo']:
            callback_query.edit_message_caption(text_1, reply_markup=inline_keyboard)
        else:
            callback_query.edit_message_text(text_1, reply_markup=inline_keyboard)

        state = 'edit_volume'

    if data == 'edit_definition':
        if user_input_data['definition']:
            text = "Yuk tavsifini yuboring:\n" \
                   "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Tavsifni o'chirish", callback_data='next')],
                [InlineKeyboardButton('« Ortga', callback_data='back')],
            ])
        else:
            text = "Yuk tavsifini yuboring:\n"
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('« Ortga', callback_data='back')],
            ])

        if user_input_data['photo']:
            callback_query.edit_message_caption(text, reply_markup=inline_keyboard)
        else:
            callback_query.edit_message_text(text, reply_markup=inline_keyboard)

        state = 'edit_definition'

    if data == 'edit_photo':
        if user_input_data['photo']:
            text = "Yuk rasmini yuboring:\n" \
                   "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Rasmni o'chirish", callback_data='next')],
                [InlineKeyboardButton('« Ortga', callback_data='back')],
            ])
        else:
            text = "Yuk rasmini yuboring:\n"
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('« Ortga', callback_data='back')],
            ])

        if user_input_data['photo']:
            callback_query.edit_message_caption(text, reply_markup=inline_keyboard)
        else:
            callback_query.edit_message_text(text, reply_markup=inline_keyboard)

        state = 'edit_photo'

    if data == 'edit_receiver_phone':
        reply_text = get_phone_number_layout('uz')
        if user_input_data['receiver_phone_number']:
            text = "Yukni qabul qiluvchining telefon raqamini yuboring:\n"
            text += reply_text
            text += "\nYoki eskisini o'chirish uchun «o'chirish» ni bosing."
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Raqamni o'chirish", callback_data='next')],
                [InlineKeyboardButton('« Ortga', callback_data='back')],
            ])
        else:
            text = "Yukni qabul qiluvchining telefon raqamini yuboring:\n"
            text += reply_text
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('« Ortga', callback_data='back')],
            ])

        if user_input_data['photo']:
            callback_query.edit_message_caption(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        state = 'edit_receiver_phone'

    callback_query.answer()
    return state


def edit_weight_callback(update: Update, context: CallbackContext):
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)
    # print('state:', user_input_data['state'])

    if user_input_data['state'] == 'edit_weight_unit':
        callback_query = update.callback_query

        if callback_query.data == 'back':
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Og'irlikni tahrirlash", callback_data='edit_weight'),
                 InlineKeyboardButton('Hajmni tahrirlash', callback_data='edit_volume')],
                [InlineKeyboardButton("Tavsifni tahrirlash", callback_data='edit_definition'),
                 InlineKeyboardButton("Rasmni tahrirlash", callback_data='edit_photo')],
                [InlineKeyboardButton("Qabul qiluvchi telefonini tahrirlash", callback_data='edit_receiver_phone')],
                [InlineKeyboardButton('« Ortga', callback_data='back')],

            ])
            user_input_data['state'] = 'edit_cargo_info'
            state = 'edit_cargo_info'
            answer = None
            layout = get_new_cargo_layout(user_input_data, user)

        else:
            user_input_data['weight_unit'] = callback_query.data
            state = 'edit_weight'
            user_input_data['state'] = state
            answer = None

            if user_input_data['weight']:
                reply_text = "Yangi yuk og'irligini yuboring (raqamda):\n" \
                             "Yoki eskisini o'chirish uchun «o'chirish» ni bosing"
                inline_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("O'g'rilikni o'chirish", callback_data='next')],
                    [InlineKeyboardButton('« Ortga', callback_data='back')],
                ])
                layout = reply_text
            else:
                reply_text = "Yangi yuk og'irligini yuboring (raqamda):\n"
                inline_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton('« Ortga', callback_data='back')],
                ])
                layout = reply_text

        callback_query.answer(answer)

        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        return state

    if user_input_data['state'] == 'edit_weight':

        callback_query = update.callback_query

        if callback_query:
            data = callback_query.data

            if data == 'back':
                state = 'edit_weight'
                user_input_data['state'] = 'edit_weight_unit'
                text_2 = "Yuk og'irlik birligini tanlang:"
                button1_text = UNITS['uz'][0]
                button2_text = UNITS['uz'][1]

                inline_keyboard = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(button1_text, callback_data='kg'),
                        InlineKeyboardButton(button2_text, callback_data='t')
                    ],
                    [InlineKeyboardButton('« Ortga', callback_data='back')],
                ])
                answer = None
                layout = text_2

            if data == 'next':
                user_input_data['weight'] = None
                inline_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
                    [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
                    [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
                    [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
                ])
                state = 'EDIT'
                user_input_data['state'] = state

                layout = get_new_cargo_layout(user_input_data, user)
                answer = "Yuk og'irligi tahrirlandi"

            callback_query.answer(answer)

            if user_input_data['photo']:
                callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            else:
                callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

            return state

        else:

            text = update.message.text

            if not text.isdigit():
                # if user['lang'] == LANGS[0]:
                text = "Yuk og'irligini raqamda kiriting !!!\n"

                # if user['lang'] == LANGS[1]:
                #     text = "Введите вес груза цифрами !!!\n\n" \
                #            "Или нажмите «next»."

                update.message.reply_text(text, quote=True)

                return 'edit_weight'

            user_input_data['weight'] = text
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
                [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
                [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
                [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
            ])
            state = 'EDIT'
            user_input_data['state'] = state

            layout = get_new_cargo_layout(user_input_data, user)

            update.message.reply_text("Yuk og'irligi tahrirlandi")

            if user_input_data['photo']:
                context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
                message = update.message.reply_photo(user_input_data['photo'].get('file_id'), layout,
                                                     reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
                user_input_data['message_id'] = message.message_id
            else:
                message = update.message.reply_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
                user_input_data['message_id'] = message.message_id

            return state


def edit_volume_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if callback_query:
        data = callback_query.data

        if data == 'back':
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Og'irlikni tahrirlash", callback_data='edit_weight'),
                 InlineKeyboardButton('Hajmni tahrirlash', callback_data='edit_volume')],
                [InlineKeyboardButton("Tavsifni tahrirlash", callback_data='edit_definition'),
                 InlineKeyboardButton("Rasmni tahrirlash", callback_data='edit_photo')],
                [InlineKeyboardButton("Qabul qiluvchi telefonini tahrirlash", callback_data='edit_receiver_phone')],
                [InlineKeyboardButton('« Ortga', callback_data='back')],

            ])
            user_input_data['state'] = 'edit_cargo_info'
            state = 'edit_cargo_info'
            answer = None

        if data == 'next':
            user_input_data['volume'] = None
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
                [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
                [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
                [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
            ])
            answer = "Yuk hajmi tahrirlandi"
            state = 'EDIT'
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
            # if user['lang'] == LANGS[0]:
            text = "Yuk hajmini raqamda kiriting !!!\n\n"
            # if user['lang'] == LANGS[1]:
            #     text = "Введите объем груза цифрами !!!\n\n" \
            #            "Или нажмите «next», чтобы пропустить этот шаг."

            update.message.reply_text(text, quote=True)

            return 'edit_volume'

        user_input_data['volume'] = text
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])
        answer = "Yuk hajmi tahrirlandi"
        state = 'EDIT'
        user_input_data['state'] = state

        layout = get_new_cargo_layout(user_input_data, user)

        update.message.reply_text(answer)

        if user_input_data['photo']:
            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
            message = update.message.reply_photo(user_input_data['photo'].get('file_id'), layout,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            user_input_data['message_id'] = message.message_id
        else:
            message = update.message.reply_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            user_input_data['message_id'] = message.message_id

        return state


def edit_definition_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if callback_query:
        data = callback_query.data
        if data == 'back':
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Og'irlikni tahrirlash", callback_data='edit_weight'),
                 InlineKeyboardButton('Hajmni tahrirlash', callback_data='edit_volume')],
                [InlineKeyboardButton("Tavsifni tahrirlash", callback_data='edit_definition'),
                 InlineKeyboardButton("Rasmni tahrirlash", callback_data='edit_photo')],
                [InlineKeyboardButton("Qabul qiluvchi telefonini tahrirlash", callback_data='edit_receiver_phone')],
                [InlineKeyboardButton('« Ortga', callback_data='back')],

            ])
            user_input_data['state'] = 'edit_cargo_info'
            state = 'edit_cargo_info'
            answer = None

        if data == 'next':
            user_input_data['definition'] = None
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
                [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
                [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
                [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
            ])
            answer = "Yuk tavsifi tahrirlandi"
            state = 'EDIT'
            user_input_data['state'] = state

        layout = get_new_cargo_layout(user_input_data, user)

        callback_query.answer(answer)

        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        return state

    else:

        user_input_data['definition'] = update.message.text
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])
        answer = "Yuk tavsifi tahrirlandi"
        state = 'EDIT'
        user_input_data['state'] = state
        layout = get_new_cargo_layout(user_input_data, user)
        update.message.reply_text(answer)

        if user_input_data['photo']:
            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
            message = update.message.reply_photo(user_input_data['photo'].get('file_id'), layout,
                                                 reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            user_input_data['message_id'] = message.message_id
        else:
            message = update.message.reply_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
            user_input_data['message_id'] = message.message_id

        return state


def edit_photo_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if callback_query:
        data = callback_query.data
        if data == 'back':
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Og'irlikni tahrirlash", callback_data='edit_weight'),
                 InlineKeyboardButton('Hajmni tahrirlash', callback_data='edit_volume')],
                [InlineKeyboardButton("Tavsifni tahrirlash", callback_data='edit_definition'),
                 InlineKeyboardButton("Rasmni tahrirlash", callback_data='edit_photo')],
                [InlineKeyboardButton("Qabul qiluvchi telefonini tahrirlash", callback_data='edit_receiver_phone')],
                [InlineKeyboardButton('« Ortga', callback_data='back')],

            ])
            user_input_data['state'] = 'edit_cargo_info'
            state = 'edit_cargo_info'
            answer = None

        if data == 'next':
            user_input_data['photo'] = None
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
                [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
                [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
                [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
            ])
            answer = "Yuk rasmi tahrirlandi"
            state = 'EDIT'
            user_input_data['state'] = state
            layout = get_new_cargo_layout(user_input_data, user)
            context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
            message = callback_query.message.reply_html(layout, reply_markup=inline_keyboard)
            user_input_data['message_id'] = message.message_id
            callback_query.answer(answer)
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

            # if user['lang'] == LANGS[0]:
            error_text = "Yuk rasmi yuborilmadi !!!\n" \
                         "Yuk rasmini yuboring:"

            # if user['lang'] == LANGS[1]:
            #     error_text = 'Фотография груза не отправлено !!!'
            #     text = "Отправите фотография груза:\n" \
            #            "Или нажмите «next», чтобы пропустить этот шаг."

            update.message.reply_text(error_text, quote=True)

            return 'edit_photo'

        layout = get_new_cargo_layout(user_input_data, user)
        update.message.reply_text("Yuk rasmi tahrirlandi")

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])
        state = 'EDIT'
        user_input_data['state'] = state
        message = update.message.reply_photo(user_input_data['photo'].get('file_id'), layout,
                                             reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        user_input_data['message_id'] = message.message_id

        return state


def edit_receiver_phone_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if callback_query:
        data = callback_query.data

        if data == 'back':
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Og'irlikni tahrirlash", callback_data='edit_weight'),
                 InlineKeyboardButton('Hajmni tahrirlash', callback_data='edit_volume')],
                [InlineKeyboardButton("Tavsifni tahrirlash", callback_data='edit_definition'),
                 InlineKeyboardButton("Rasmni tahrirlash", callback_data='edit_photo')],
                [InlineKeyboardButton("Qabul qiluvchi telefonini tahrirlash", callback_data='edit_receiver_phone')],
                [InlineKeyboardButton('« Ortga', callback_data='back')],

            ])
            user_input_data['state'] = 'edit_cargo_info'
            state = 'edit_cargo_info'
            answer = None

        if data == 'next':
            user_input_data['receiver_phone_number'] = None
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
                [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
                [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
                [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
            ])
            answer = "Yukni qabul qiluvchining telefon raqami tahrirlandi"
            state = 'EDIT'
            user_input_data['state'] = state

        layout = get_new_cargo_layout(user_input_data, user)

        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        callback_query.answer(answer)
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

            layout = get_new_cargo_layout(user_input_data, user)
            inline_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
                [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
                [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
                [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
            ])
            answer = "Yukni qabul qiluvchining telefon raqami tahrirlandi"
            state = 'EDIT'
            user_input_data['state'] = state
            layout = get_new_cargo_layout(user_input_data, user)
            update.message.reply_text(answer)

            if user_input_data['photo']:
                context.bot.edit_message_reply_markup(update.effective_chat.id, user_input_data.pop('message_id'))
                message = update.message.reply_photo(user_input_data['photo'].get('file_id'), layout,
                                                     reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
                user_input_data['message_id'] = message.message_id
            else:
                message = update.message.reply_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
                user_input_data['message_id'] = message.message_id

            return state

        else:
            reply_text = get_phone_number_layout('uz')

            # if user['lang'] == LANGS[0]:
            text = "Xato telefon raqami yuborildi !!!\n"
            text += reply_text

            error_text = "Siz o'z telefon raqmingizni yubordingiz !!!\n\n" \
                         "Yukni qabul qiluvchining telefon raqamini yuboring:"

            # if user['lang'] == LANGS[1]:
            #     text = "Номер телефона с ошибкой отправлен !!!"
            #     reply_text += "\nИли нажмите «next», чтобы пропустить этот шаг."
            #     error_text = 'Вы отправили свой номер телефона !!!\n\n' \
            #                  'Отправьте номер телефона получателя груза:'

            if phone_number == user['phone_number']:
                text = error_text

            update.message.reply_text(text, quote=True, parse_mode=ParseMode.HTML)

            return 'edit_receiver_phone'


def edit_weight_conv_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'back':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Og'irlikni tahrirlash", callback_data='edit_weight'),
             InlineKeyboardButton('Hajmni tahrirlash', callback_data='edit_volume')],
            [InlineKeyboardButton("Tasnifni tahrirlash", callback_data='edit_definition'),
             InlineKeyboardButton("Rasmni tahrirlash", callback_data='edit_photo')],
            [InlineKeyboardButton("Qabul qiluvchi telefonini tahrirlash", callback_data='edit_receiver_phone')],
            [InlineKeyboardButton('« Ortga', callback_data='back')],

        ])

        callback_query.edit_message_reply_markup(inline_keyboard)
        callback_query.answer()
        return 'edit_cargo_info'

    if data == 'edit_weight_unit':
        # if user['lang'] == LANGS[0]:
        text_2 = "Yuk og'irligini tanlang:"
        button1_text = UNITS['uz'][0]
        button2_text = UNITS['uz'][1]

        # if user['lang'] == LANGS[1]:
        #     text_1 = "Шаг 3."
        #     text_2 = "Выберите вес груза:"
        #     button1_text = UNITS['ru'][0]
        #     button2_text = UNITS['ru'][1]

        inline_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(button1_text, callback_data='kg'),
                InlineKeyboardButton(button2_text, callback_data='t')
            ]
        ])

        callback_query.edit_message_reply_markup(None)
        callback_query.message.reply_text(text_2, reply_markup=inline_keyboard)
        user_input_data['state'] = 'edit_weight_unit'

        return 'edit_weight_unit'

    if data == 'edit_weight':
        reply_text = "Yuk og'irligini yuboring (raqamda):\n\n" \
                     "Bu bosqichni o'tkazib yuborish uchun «next» ni bosing."

        callback_query.edit_message_reply_markup(None)
        callback_query.message.reply_text(reply_text, reply_markup=get_skip_keyboard('weight'))

        return 'edit_weight'


edit_cargo_info_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_cargo_info_callback, pattern='edit_weight|edit_volume|'
                                                                         'edit_definition|edit_photo|'
                                                                         'edit_receiver_phone|back')],
    states={
        'edit_weight': [CallbackQueryHandler(edit_weight_callback, pattern='^(kg|t|back|next)$'),
                        MessageHandler(Filters.text & ~Filters.command, edit_weight_callback)],
        'edit_volume': [CallbackQueryHandler(edit_volume_callback, pattern='^(back|next)$'),
                        MessageHandler(Filters.text & ~Filters.command, edit_volume_callback)],
        'edit_definition': [CallbackQueryHandler(edit_definition_callback, pattern='^(back|next)$'),
                            MessageHandler(Filters.text & ~Filters.command, edit_definition_callback)],
        'edit_photo': [CallbackQueryHandler(edit_photo_callback, pattern='^(back|next)$'),
                       MessageHandler(Filters.text & ~Filters.command | Filters.photo, edit_photo_callback)],
        'edit_receiver_phone': [CallbackQueryHandler(edit_receiver_phone_callback, pattern='^(back|next)$'),
                                MessageHandler(Filters.text & ~Filters.command, edit_receiver_phone_callback)],

    },
    fallbacks=[],

    map_to_parent={
        'EDIT': 'EDIT',
        'edit_cargo_info': 'edit_cargo_info'
    }
)
