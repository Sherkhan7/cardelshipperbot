from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update
from inlinekeyboards import InlineKeyboard
from DB import *
from languages import LANGS


def message_handler_callback(update: Update, context: CallbackContext):
    message_text = update.effective_message.text

    user = get_user(update.effective_user.id)
    if message_text == '/menu':

        if user:

            if user['lang'] == LANGS[0]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
                update.message.reply_text('MENU', reply_markup=inline_keyboard.get_keyboard())

            if user['lang'] == LANGS[1]:
                inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
                update.message.reply_text('MENU', reply_markup=inline_keyboard.get_keyboard())

        else:
            update.message.reply_text("Siz ro'yxatdan o'tmagansiz!\nBuning uchun /start ni boshing.\n"
                                      "\nВы не зарегистрированы!\nДля этого нажмите /start")


message_handler = MessageHandler(Filters.text, message_handler_callback)
