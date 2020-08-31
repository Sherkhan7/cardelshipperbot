from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update
from inlinekeyboards import InlineKeyboard
from DB import *


def message_handler_callback(update: Update, context: CallbackContext):
    # print('message_handler')
    # print(update.message.contact.phone_number)

    user = get_user(update.effective_user.id)

    if user:

        inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])

        update.message.reply_text('MENU', reply_markup=inline_keyboard.get_keyboard())

    else:
        update.message.reply_text("Siz ro'yxatdan o'tmagansiz!\nBuning uchun /start ni boshing.\n"
                                  "\nВы не зарегистрированы!\nДля этого нажмите /start")


message_handler = MessageHandler(Filters.text | Filters.contact, message_handler_callback)
