from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
# from handlers import (edit_address_conversation_handler, edit_cargo_info_conversation_handler,
#                      edit_date_and_time_conversation_handler)
from handlers.editcargoinfoconversation import edit_cargo_info_conversation_handler
from handlers.editaddressconversation import edit_address_conversation_handler
from handlers.editdateandtimeconversation import edit_date_and_time_conversation_handler
from DB import *
from inlinekeyboards import InlineKeyboard
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def edit_callback(update: Update, context: CallbackContext):
    print('edit_callback')
    # print(update.callback_query.data)

    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)
    user_input_data = context.user_data

    if data == 'edit_address':
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Yuboruvchi manzilini tahrirlash', callback_data='edit_from_address')],
            [InlineKeyboardButton('Yuboruvchi lokatsiyasini tahrirlash', callback_data='edit_from_location')],
            [InlineKeyboardButton('Qabul qiluvchi manzilini tahrirlash', callback_data='edit_to_address')],
            [InlineKeyboardButton('Qabul qiluvchi lokatsiyasini tahrirlash', callback_data='edit_to_location')],
            [InlineKeyboardButton('« Ortga', callback_data='back')],

        ])
        user_input_data['state'] = 'EDIT ADDRESS'
        state = 'edit_address'

    if data == 'edit_cargo_info':
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

    if data == 'edit_date':
        inline_keyboard = InlineKeyboard('dates_keyboard', user['lang']).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton('« Ortga', callback_data='back')])

        user_input_data['state'] = 'EDIT DATE'
        state = 'edit_date'

    if data == 'edit_date_and_time':
        # inline_keyboard = InlineKeyboard('hours_keyboard', user['lang'], begin=6, end=17).get_keyboard()
        # inline_keyboard['inline_keyboard'].append([InlineKeyboardButton('« Ortga', callback_data='back')])

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Kunni tahrirlash', callback_data='edit_date')],
            [InlineKeyboardButton('Vaqtni tahrirlash', callback_data='edit_time')],
            [InlineKeyboardButton('« Ortga', callback_data='back')],
        ])
        user_input_data['state'] = 'edit_date_and_time'
        state = 'edit_date_and_time'

    if data == 'terminate_editing':
        inline_keyboard = InlineKeyboard('confirm_keyboard', user['lang'], data=user_input_data).get_keyboard()

        user_input_data['state'] = 'confirmation'

        state = ConversationHandler.END

    callback_query.answer()
    callback_query.edit_message_reply_markup(inline_keyboard)

    return state


def terminate_callback(update: Update, context: CallbackContext):
    print('terminate_callback')

    return ConversationHandler.END


edit_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_callback, pattern='^edit|^terminate')],
    states={
        'edit_address': [edit_address_conversation_handler],
        'edit_cargo_info': [edit_cargo_info_conversation_handler],
        'edit_date_and_time': [edit_date_and_time_conversation_handler],
    },
    fallbacks=[CallbackQueryHandler(terminate_callback, pattern='^terminate')],

    map_to_parent={
        -1: 'confirmation',
        'EDIT': 'EDIT'
    }
)
