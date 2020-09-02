from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from inlinekeyboards import InlineKeyboard
from DB import *


def message_handler_callback(update: Update, context: CallbackContext):
    # print('message_handler')
    # print(update.message.contact.phone_number)
    text = update.message.text
    first = '0'
    second = str(int(first)+1)
    third = str(int(second)+1)
    forth = str(int(third)+1)

    inline_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('orqaga', callback_data='back_'+first),
            InlineKeyboardButton(first, callback_data=f'{first}'),
            InlineKeyboardButton(second, callback_data=f'{second}'),
            InlineKeyboardButton(third, callback_data=f'{third}'),
            InlineKeyboardButton(forth, callback_data=f'{forth}'),
            InlineKeyboardButton('oldinga', callback_data='next_'+forth)
         ]
    ])

    update.message.reply_text('soantni kiriting', reply_markup=inline_keyboard)

    user = get_user(update.effective_user.id)

    # if user:
    #
    #     inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])
    #
    #     update.message.reply_text('MENU', reply_markup=inline_keyboard.get_keyboard())
    #
    # else:
    #     update.message.reply_text("Siz ro'yxatdan o'tmagansiz!\nBuning uchun /start ni boshing.\n"
    #                               "\nВы не зарегистрированы!\nДля этого нажмите /start")


message_handler = MessageHandler(Filters.text | Filters.contact, message_handler_callback)
