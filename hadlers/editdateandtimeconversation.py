from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from DB import *
from inlinekeyboards import InlineKeyboard
from layouts import get_new_cargo_layout


def edit_date_and_time_callback(update: Update, context: CallbackContext):
    # print('edit_time_callback')

    callback_query = update.callback_query
    data = callback_query.data
    # print(data)
    user_input_data = context.user_data

    if data == 'back':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kunni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])

        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        user_input_data['state'] = 'EDIT'
        return 'EDIT'

    if data == 'edit_date':
        # inline_keyboard = InlineKeyboard('dates_keyboard', 'uz').get_keyboard()
        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        after_tomorrow = tomorrow + datetime.timedelta(days=1)
        day_after_tomorrow = after_tomorrow + datetime.timedelta(days=1)

        # if lang == LANGS[0]:
        button1_text = 'Bugun'

        # if lang == LANGS[1]:
        #     button1_text = 'Сейчас'
        #     button2_text = 'Cегодня'

        inline_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f'{button1_text}\n{datetime.datetime.today().strftime("%d-%m-%Y")}',
                                     callback_data=f'{datetime.datetime.today().strftime("%d-%m-%Y")}'),
                InlineKeyboardButton(f'{tomorrow.strftime("%d-%m-%Y")}',
                                     callback_data=f'{tomorrow.strftime("%d-%m-%Y")}'),
            ],
            [
                InlineKeyboardButton(f'{after_tomorrow.strftime("%d-%m-%Y")}',
                                     callback_data=f'{after_tomorrow.strftime("%d-%m-%Y")}'),
                InlineKeyboardButton(f'{day_after_tomorrow.strftime("%d-%m-%Y")}',
                                     callback_data=f'{day_after_tomorrow.strftime("%d-%m-%Y")}'),
            ]
        ])
        callback_query.edit_message_reply_markup(inline_keyboard)
        state = 'edit_date'

    if data == 'edit_time':
        inline_keyboard = InlineKeyboard('hours_keyboard', 'uz', begin=6, end=17).get_keyboard()
        callback_query.edit_message_reply_markup(inline_keyboard)

        state = 'edit_time'

    callback_query.answer()
    return state


def edit_date_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print(data)
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    user_input_data['date'] = data
    callback_query.answer("Kun tahrirlandi")

    layout = get_new_cargo_layout(user_input_data, user)
    inline_keyboard = InlineKeyboard('confirm_keyboard', 'uz', data=user_input_data).get_keyboard()

    if user_input_data['photo']:
        callback_query.message.edit_caption(caption=layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def edit_time_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print(data)
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'next' or data == 'back':

        if data == 'next':
            inline_keyboard = InlineKeyboard('hours_keyboard', 'uz', begin=18, end=29).get_keyboard()
        if data == 'back':
            inline_keyboard = InlineKeyboard('hours_keyboard', 'uz', begin=6, end=17).get_keyboard()

        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        return 'edit_time'
    else:
        inline_keyboard = InlineKeyboard('minutes_keyboard', 'uz', data=data)

        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard.get_keyboard())

        return 'edit_minute'


def edit_minute_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print('data:', data)
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'back':

        if data == 'back':
            inline_keyboard = InlineKeyboard('hours_keyboard', 'uz', begin=6, end=17).get_keyboard()

        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        return 'edit_time'

    else:
        user_input_data['time'] = data
        callback_query.answer('Vaqt tahrirlandi')

        layout = get_new_cargo_layout(user_input_data, user)
        inline_keyboard = InlineKeyboard('confirm_keyboard', 'uz', data=user_input_data).get_keyboard()

        if user_input_data['photo']:
            callback_query.message.edit_caption(caption=layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        return ConversationHandler.END


edit_date_and_time_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_date_and_time_callback, pattern='edit_date|edit_time|back')],
    states={
        'edit_date': [
            CallbackQueryHandler(edit_date_callback,
                                 pattern=r"^(0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-](20\d\d)$")],
        'edit_time': [CallbackQueryHandler(edit_time_callback, pattern=r'back|next|^(\d|1\d|2[0-3])$')],
        'edit_minute': [CallbackQueryHandler(edit_minute_callback, pattern=r'back|^(\d|1\d|2[0-3])[:](0|\d\d)$')]
    },
    fallbacks=[],

    map_to_parent={
        -1: -1,
        'EDIT': 'EDIT'
    }
)
