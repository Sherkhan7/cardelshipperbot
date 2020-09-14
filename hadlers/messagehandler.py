from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from inlinekeyboards import InlineKeyboard
from layouts import *
from replykeyboards import ReplyKeyboard
from DB import *


def message_handler_callback(update: Update, context: CallbackContext):
    # print('message_handler')
    # print(update.message.contact.phone_number)
    text = update.message.text.split(' ', 1)[-1]

    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user = get_user(update.effective_user.id)

    if user:

        if text == 'Sozlamalar' or text == 'Настройки':

            reply_keyboard = ReplyKeyboard('settings_keyboard', user['lang'])

            update.message.reply_text(text, reply_markup=reply_keyboard.get_keyboard())

        elif text == "Mening ma'lumotlarim" or text == 'Мои данные':

            inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang'])
            update.message.reply_text(get_user_info_layout(user), reply_markup=inline_keyboard.get_keyboard(),
                                      parse_mode=ParseMode.HTML)

        elif text == "Tilni o'zgartirish" or text == "Изменить язык":

            reply_text = 'Tilni tanlang.\nВыберите язык.'

            inline_keyboard = InlineKeyboard('langs_keyboard')

            update.message.reply_text(reply_text, reply_markup=inline_keyboard.get_keyboard())

        elif text == 'Ortga' or text == 'Назад':

            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang'])
            update.message.reply_text(text, reply_markup=reply_keyboard.get_keyboard())
        else:

            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang'])

            update.message.reply_text('\U0001F914', reply_markup=reply_keyboard.get_keyboard(),
                                      reply_to_message_id=update.message.message_id)

    else:

        update.message.reply_text("Siz ro'yxatdan o'tmagansiz!\nBuning uchun /start ni boshing.\n"
                                  "\nВы не зарегистрированы!\nДля этого нажмите /start")


message_handler = MessageHandler(Filters.text & ~Filters.command, message_handler_callback)
