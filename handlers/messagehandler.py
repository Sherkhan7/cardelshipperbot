from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from inlinekeyboards import InlineKeyboard
from layouts import *
from replykeyboards import ReplyKeyboard
from DB import *


def message_handler_callback(update: Update, context: CallbackContext):
    # print('message_handler')
    # print(update.message.contact.phone_number)
    full_text = update.message.text
    text = full_text.split(' ', 1)[-1]

    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user = get_user(update.effective_user.id)

    # update.message.reply_text('bla bla', reply_markup=InlineKeyboardMarkup([
    #     [InlineKeyboardButton('next', callback_data='skip_to_location')],
    #     [InlineKeyboardButton('123', callback_data='skip_location')],
    #     [InlineKeyboardButton('fdffd', callback_data='location')]
    # ]))

    if user:

        if text == '/menu':

            if user['lang'] == LANGS[0]:
                reply_text = '\U0001F4D6 Menu'
            if user['lang'] == LANGS[1]:
                reply_text = '\U0001F4D6 Меню'

            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang'])
            update.message.reply_text(reply_text, reply_markup=reply_keyboard.get_keyboard())

        elif text == 'Sozlamalar' or text == 'Настройки':

            reply_keyboard = ReplyKeyboard('settings_keyboard', user['lang'])

            update.message.reply_text(full_text, reply_markup=reply_keyboard.get_keyboard())

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
            update.message.reply_text(full_text, reply_markup=reply_keyboard.get_keyboard())
        else:

            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang'])

            thinking_emoji = '\U0001F914'

            update.message.reply_text(thinking_emoji, reply_markup=reply_keyboard.get_keyboard(),
                                      reply_to_message_id=update.message.message_id)

    else:

        update.message.reply_text("Siz ro'yxatdan o'tmagansiz!\nBuning uchun /start ni boshing.\n"
                                  "\nВы не зарегистрированы!\nДля этого нажмите /start")


message_handler = MessageHandler(Filters.text & ~Filters.command, message_handler_callback)
