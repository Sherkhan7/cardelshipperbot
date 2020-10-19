from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from inlinekeyboards import InlineKeyboard
from layouts import *
from replykeyboards import ReplyKeyboard
from DB import *


def message_handler_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    full_text = update.message.text
    text = full_text.split(' ', 1)[-1]

    bot_data = context.bot_data

    if not bot_data:
        user_data = get_user(update.effective_user.id)
        bot_data['user_data'] = user_data

    user = bot_data['user_data']

    if user:

        if text == '/menu':

            if user['lang'] == LANGS[0]:
                reply_text = '\U0001F4D6 Menu'
            if user['lang'] == LANGS[1]:
                reply_text = '\U0001F4D6 Меню'

            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang']).get_keyboard()
            update.message.reply_text(reply_text, reply_markup=reply_keyboard)

        elif text == 'Sozlamalar' or text == 'Настройки':

            reply_keyboard = ReplyKeyboard('settings_keyboard', user['lang']).get_keyboard()

            update.message.reply_text(full_text, reply_markup=reply_keyboard)

        elif text == 'Mening ma\'lumotlarim' or text == 'Мои данные':

            inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang']).get_keyboard()
            update.message.reply_html(get_user_info_layout(user), reply_markup=inline_keyboard)

        elif text == 'Tilni o\'zgartirish' or text == 'Изменить язык':

            reply_text = 'Tilni tanlang.\nВыберите язык.'

            inline_keyboard = InlineKeyboard('langs_keyboard').get_keyboard()

            update.message.reply_text(reply_text, reply_markup=inline_keyboard)

        elif text == 'Ortga' or text == 'Назад':

            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang']).get_keyboard()
            update.message.reply_text(full_text, reply_markup=reply_keyboard)

        else:

            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang']).get_keyboard()

            thinking_emoji = '\U0001F914'

            update.message.reply_text(thinking_emoji, quote=True, reply_markup=reply_keyboard)

    else:

        update.message.reply_text('\U000026A0 Siz ro\'yxatdan o\'tmagansiz! \nBuning uchun /start ni bosing.\n\n'
                                  '\U000026A0 Вы не зарегистрированы !\nДля этого нажмите /start.')


message_handler = MessageHandler(Filters.text & ~Filters.command, message_handler_callback)
