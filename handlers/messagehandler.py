from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update
from inlinekeyboards import InlineKeyboard
from layouts import *
from replykeyboards import ReplyKeyboard
from helpers import set_user_data_in_bot_data
from pprint import pprint


def message_handler_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    # context.bot.edit_message_text('edited_text', -1001384173376, 315)
    full_text = update.message.text
    text = full_text.split(' ', 1)[-1]
    bot_data = context.bot_data

    # set bot_data[update.effective_user.id] -> dict
    set_user_data_in_bot_data(update.effective_user.id, bot_data)
    user = bot_data[update.effective_user.id]
    pprint(bot_data)

    if user:

        if text == 'Sozlamalar' or text == 'Настройки':

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

            thinking_emoji = '\U0001F914'

            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang']).get_keyboard()
            update.message.reply_text(thinking_emoji, quote=True, reply_markup=reply_keyboard)

    else:

        reply_text = '\U000026A0 Siz ro\'yxatdan o\'tmagansiz !\nBuning uchun /start ni bosing.\n\n' \
                     '\U000026A0 Вы не зарегистрированы !\nДля этого нажмите /start.'

        update.message.reply_text(reply_text)


message_handler = MessageHandler(Filters.text & (~ Filters.command), message_handler_callback)
