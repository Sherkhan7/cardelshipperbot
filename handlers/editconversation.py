from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from handlers.editcargoinfoconversation import edit_cargo_info_conversation_handler
from handlers.editaddressconversation import edit_address_conversation_handler
from handlers.editdateandtimeconversation import edit_date_and_time_conversation_handler
from DB import *
from inlinekeyboards import InlineKeyboard
from languages import LANGS
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def edit_callback(update: Update, context: CallbackContext):
    # print('edit_callback')

    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    if data == 'edit_address':
        inline_keyboard = InlineKeyboard('edit_address_keyboard', user['lang']).get_keyboard()
        state = 'edit_address'
        user_input_data['state'] = state

    if data == 'edit_cargo_info':
        inline_keyboard = InlineKeyboard('edit_cargo_info_keyboard', user['lang']).get_keyboard()
        state = 'edit_cargo_info'
        user_input_data['state'] = state

    if data == 'edit_date_and_time':

        state = 'edit_date_and_time'
        user_input_data['state'] = state

        if user['lang'] == LANGS[0]:
            text = 'Kunni tanlang'
            button_text = '« Ortga'
        if user['lang'] == LANGS[1]:
            text = 'Выберите день'
            button_text = '« Назад'

        inline_keyboard = InlineKeyboard('dates_keyboard', user['lang']).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button_text, callback_data='back')])

        callback_query.answer()

        if user_input_data['photo']:
            callback_query.edit_message_caption(text, reply_markup=inline_keyboard)
        else:
            callback_query.edit_message_text(text, reply_markup=inline_keyboard)

        return state

    if data == 'terminate_editing':
        inline_keyboard = InlineKeyboard('confirm_keyboard', user['lang'], data=user_input_data).get_keyboard()

        user_input_data['state'] = 'confirmation'

        state = ConversationHandler.END

    callback_query.answer()
    callback_query.edit_message_reply_markup(inline_keyboard)

    return state


edit_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_callback, pattern='edit|terminate')],
    states={
        'edit_address': [edit_address_conversation_handler],
        'edit_cargo_info': [edit_cargo_info_conversation_handler],
        'edit_date_and_time': [edit_date_and_time_conversation_handler],
    },
    fallbacks=[],

    map_to_parent={
        -1: 'confirmation',
        'edit': 'edit'
    }
)
