from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from inlinekeyboards import InlineKeyboard
from languages import LANGS
from filters import phone_number_filter
from DB import *


def message_handler_callback(update: Update, context: CallbackContext):
    # print('message_handler')
    # print(update.message.contact.phone_number)
    text = update.message.text
    #
    # print(text)
    # print(update.message)

    user = get_user(update.effective_user.id)

    if user:

        inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])

        update.message.reply_text('MENU', reply_markup=inline_keyboard.get_keyboard())

    else:
        update.message.reply_text("Siz ro'yxatdan o'tmagansiz!\nBuning uchun /start ni boshing.\n"
                                  "\nВы не зарегистрированы!\nДля этого нажмите /start")


message_handler = MessageHandler(Filters.text | Filters.contact, message_handler_callback)
