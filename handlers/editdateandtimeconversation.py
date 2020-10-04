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
    user = get_user(update.effective_user.id)

    if data == 'back' or data == 'now':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])
        state = 'EDIT'
        user_input_data['state'] = state
        answer = None

        if data == 'now':
            user_input_data['date'] = datetime.datetime.now().strftime('%d-%m-%Y')
            user_input_data['time'] = 'now'
            answer = 'Kun va vaqt tahrirlandi'

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

        # if user['lang'] == LANGS[0]:
        text = 'Soatni belgilang:'
        #
        # if user['lang'] == LANGS[1]:
        #     text = 'Выберите время:'

        inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton('« Ortga', callback_data='back_btn')])
        layout = text
        answer = None
        state = 'edit_time'

    # if data == 'edit_date':
    #     # inline_keyboard = InlineKeyboard('dates_keyboard', 'uz').get_keyboard()
    #     tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    #     after_tomorrow = tomorrow + datetime.timedelta(days=1)
    #     day_after_tomorrow = after_tomorrow + datetime.timedelta(days=1)
    #
    #     # if lang == LANGS[0]:
    #     button1_text = 'Bugun'
    #
    #     # if lang == LANGS[1]:
    #     #     button1_text = 'Сейчас'
    #     #     button2_text = 'Cегодня'
    #
    #     inline_keyboard = InlineKeyboardMarkup([
    #         [
    #             InlineKeyboardButton(f'{button1_text}\n{datetime.datetime.today().strftime("%d-%m-%Y")}',
    #                                  callback_data=f'{datetime.datetime.today().strftime("%d-%m-%Y")}'),
    #             InlineKeyboardButton(f'{tomorrow.strftime("%d-%m-%Y")}',
    #                                  callback_data=f'{tomorrow.strftime("%d-%m-%Y")}'),
    #         ],
    #         [
    #             InlineKeyboardButton(f'{after_tomorrow.strftime("%d-%m-%Y")}',
    #                                  callback_data=f'{after_tomorrow.strftime("%d-%m-%Y")}'),
    #             InlineKeyboardButton(f'{day_after_tomorrow.strftime("%d-%m-%Y")}',
    #                                  callback_data=f'{day_after_tomorrow.strftime("%d-%m-%Y")}'),
    #         ]
    #     ])
    #     callback_query.edit_message_reply_markup(inline_keyboard)
    #     state = 'edit_date'
    if user_input_data['photo']:
        callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    callback_query.answer(answer)
    return state


def edit_time_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print(data)
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'back_btn':
        inline_keyboard = InlineKeyboard('dates_keyboard', user['lang']).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton('« Ortga', callback_data='back')])

        # inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17).get_keyboard()
        # inline_keyboard['inline_keyboard'].append([InlineKeyboardButton('« Ortga', callback_data='back')])

        # inline_keyboard = InlineKeyboardMarkup([
        #     [InlineKeyboardButton('Kunni tahrirlash', callback_data='edit_date')],
        #     [InlineKeyboardButton('Vaqtni tahrirlash', callback_data='edit_time')],
        #     [InlineKeyboardButton('« Ortga', callback_data='back')],
        # ])
        state = 'edit_date_and_time'
        user_input_data['state'] = state
        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)
        return state
    if data == 'next' or data == 'back':

        if data == 'next':
            inline_keyboard = InlineKeyboard('hours_keyboard', 'uz', begin=18, end=29).get_keyboard()
        if data == 'back':
            inline_keyboard = InlineKeyboard('hours_keyboard', 'uz', begin=6, end=17).get_keyboard()

        callback_query.answer()
        callback_query.edit_message_reply_markup()

        return 'edit_time'
    else:
        inline_keyboard = InlineKeyboard('minutes_keyboard', 'uz', data=data).get_keyboard()
        if user_input_data['photo']:
            callback_query.edit_message_caption('Daqiqani belgilang', reply_markup=inline_keyboard)
        else:
            callback_query.edit_message_text('Daqiqani belgilang', reply_markup=inline_keyboard)
        callback_query.answer()

        return 'edit_minute'


def edit_minute_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    # print('data:', data)
    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    if data == 'back':

        inline_keyboard = InlineKeyboard('hours_keyboard', 'uz', begin=6, end=17).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton('« Ortga', callback_data='back_btn')])
        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        return 'edit_time'

    else:
        user_input_data['time'] = data
        user_input_data['date'] = user_input_data.pop('new_date')
        layout = get_new_cargo_layout(user_input_data, user)

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])
        state = 'EDIT'
        if user_input_data['photo']:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        user_input_data['state'] = state
        callback_query.answer('Kun va vaqt tahrirlandi')
        return state


edit_date_and_time_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_date_and_time_callback,
                                       pattern=r"^(now|today|tomorrow|after_tomorrow|back)$")],
    states={
        'edit_time': [CallbackQueryHandler(edit_time_callback, pattern=r'back_btn|back|next|^(\d|1\d|2[0-3])$')],
        'edit_minute': [CallbackQueryHandler(edit_minute_callback, pattern=r'back|^(\d|1\d|2[0-3])[:](0|\d\d)$')]
    },
    fallbacks=[],

    map_to_parent={
        'EDIT': 'EDIT',
        'edit_date_and_time': 'edit_date_and_time'
    }
)
# (0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-](20\d\d)
