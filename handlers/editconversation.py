import logging
from telegram import Update, InlineKeyboardButton
from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext
from handlers.editaddressconversation import edit_address_conversation_handler
from handlers.editcargoinfoconversation import edit_cargo_info_conversation_handler
from handlers.editdateandtimeconversation import edit_date_and_time_conversation_handler
from inlinekeyboards import InlineKeyboard
from languages import LANGS
from inlinekeyboards.inlinekeyboardvariables import *
from globalvariables import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def edit_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = context.bot_data[update.effective_user.id]

    if data == 'edit_address':
        inline_keyboard = InlineKeyboard(edit_address_keyboard, user[LANG]).get_keyboard()
        state = 'edit_address'

    if data == 'edit_cargo_info':
        inline_keyboard = InlineKeyboard(edit_cargo_info_keyboard, user[LANG]).get_keyboard()
        state = 'edit_cargo_info'

    if data == 'terminate_editing':
        inline_keyboard = InlineKeyboard(confirm_keyboard, user[LANG], data=user_input_data).get_keyboard()
        state = 'confirmation'

    if data == 'edit_date_and_time':

        if user[LANG] == LANGS[0]:
            text = "Kunni tanlang"
            button_text = "Ortga"

        if user[LANG] == LANGS[1]:
            text = "Выберите день"
            button_text = "Назад"

        if user[LANG] == LANGS[2]:
            text = "Кунни танланг"
            button_text = "Ортга"

        text += ' :'
        button_text = '« ' + button_text

        inline_keyboard = InlineKeyboard(dates_keyboard, user[LANG]).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button_text, callback_data='back')])

        callback_query.answer()

        if user_input_data[PHOTO]:
            callback_query.edit_message_caption(text, reply_markup=inline_keyboard)
        else:
            callback_query.edit_message_text(text, reply_markup=inline_keyboard)

        state = 'edit_date_and_time'
        user_input_data[STATE] = state

        return state

    callback_query.answer()
    callback_query.edit_message_reply_markup(inline_keyboard)

    user_input_data[STATE] = state
    return state


edit_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_callback, pattern='^(edit_|terminate_)')],

    states={
        'edit_address': [edit_address_conversation_handler],
        'edit_cargo_info': [edit_cargo_info_conversation_handler],
        'edit_date_and_time': [edit_date_and_time_conversation_handler],
    },
    fallbacks=[],

    map_to_parent={
        'confirmation': 'confirmation',
        'edit': 'edit'
    }
)
