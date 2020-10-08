from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from DB import *
from inlinekeyboards import InlineKeyboard
from layouts import get_new_cargo_layout
from languages import LANGS


def edit_date_and_time_callback(update: Update, context: CallbackContext):
    # print('edit_time_callback')
    callback_query = update.callback_query
    data = callback_query.data
    # print(data)
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'back' or data == 'now':
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()
        answer = None
        state = 'edit'

        if data == 'now':
            user_input_data['date'] = datetime.datetime.now().strftime('%d-%m-%Y')
            user_input_data['time'] = 'now'

            if user['lang'] == LANGS[0]:
                answer = '\U0001F44F\U0001F44F\U0001F44F Kun va vaqt tahrirlandi.'
            if user['lang'] == LANGS[1]:
                answer = '\U0001F44F\U0001F44F\U0001F44F Дата и время изменены.'

        layout = get_new_cargo_layout(user_input_data, user)

    if data == 'today' or data == 'tomorrow' or data == 'after_tomorrow':

        if data == 'today':
            user_input_data['new_date'] = datetime.datetime.now().strftime('%d-%m-%Y')

        if data == 'tomorrow':
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            user_input_data['new_date'] = tomorrow.strftime('%d-%m-%Y')

        if data == 'after_tomorrow':
            after_tomorrow = datetime.datetime.now() + datetime.timedelta(days=2)
            user_input_data['new_date'] = after_tomorrow.strftime('%d-%m-%Y')

        if user['lang'] == LANGS[0]:
            text = 'Soatni belgilang:'
            button_text = '« Ortga'
        if user['lang'] == LANGS[1]:
            text = 'Выберите время:'
            button_text = '« Назад'

        inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button_text, callback_data='back_btn')])
        layout = text
        answer = None
        state = 'edit_time'

    callback_query.answer(answer)

    if user_input_data['photo']:
        callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    user_input_data['state'] = state
    return state


def edit_time_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print(data)
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'back_btn' or data == 'next' or data == 'back':

        if data == 'back_btn':

            user_input_data.pop('new_date')

            if user['lang'] == LANGS[0]:
                button_text = '« Ortga'
            if user['lang'] == LANGS[1]:
                button_text = '« Назад'

            inline_keyboard = InlineKeyboard('dates_keyboard', user['lang']).get_keyboard()
            inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button_text, callback_data='back')])

            state = 'edit_date_and_time'

        if data == 'next' or data == 'back':

            if data == 'next':
                inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=18, end=29).get_keyboard()
            if data == 'back':
                inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17).get_keyboard()

            state = user_input_data['state']

        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        user_input_data['state'] = state
        return state

    else:

        if user['lang'] == LANGS[0]:
            text = 'Daqiqani belgilang:'
        if user['lang'] == LANGS[1]:
            text = 'Выберите минуту:'

        inline_keyboard = InlineKeyboard('minutes_keyboard', user['lang'], data=data).get_keyboard()

        callback_query.answer()
        if user_input_data['photo']:
            callback_query.edit_message_caption(text, reply_markup=inline_keyboard)
        else:
            callback_query.edit_message_text(text, reply_markup=inline_keyboard)

        state = 'edit_minute'
        user_input_data['state'] = state
        return state


def edit_minute_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print('data:', data)
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'back':

        if user['lang'] == LANGS[0]:
            button_text = '« Ortga'
        if user['lang'] == LANGS[1]:
            button_text = '« Назад'

        inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button_text, callback_data='back_btn')])

        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        state = 'edit_time'

    else:
        if user['lang'] == LANGS[0]:
            answer = '\U0001F44F\U0001F44F\U0001F44F Kun va vaqt tahrirlandi.'
        if user['lang'] == LANGS[1]:
            answer = '\U0001F44F\U0001F44F\U0001F44F Дата и время изменены.'

        user_input_data['time'] = data
        user_input_data['date'] = user_input_data.pop('new_date')
        layout = get_new_cargo_layout(user_input_data, user)
        inline_keyboard = InlineKeyboard('edit_keyboard', user['lang']).get_keyboard()

        callback_query.answer(answer)

        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        state = 'edit'

    user_input_data['state'] = state
    return state


edit_date_and_time_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_date_and_time_callback,
                                       pattern=r"^(now|today|tomorrow|after_tomorrow|back)$")],
    states={
        'edit_time': [CallbackQueryHandler(edit_time_callback, pattern=r'^(back_btn|back|next|\d|1\d|2[0-3])$')],
        'edit_minute': [CallbackQueryHandler(edit_minute_callback, pattern=r'^back|(\d|1\d|2[0-3])[:](0|\d\d)$')]
    },
    fallbacks=[],

    map_to_parent={
        'edit': 'edit',
        'edit_date_and_time': 'edit_date_and_time'
    }
)
# (0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-](20\d\d)
