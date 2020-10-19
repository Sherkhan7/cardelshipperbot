from telegram import Update, ParseMode
from telegram.ext import CallbackQueryHandler, CallbackContext
from replykeyboards import ReplyKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from DB.main import *
from languages import LANGS
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def main_inline_keyboard_callback(update: Update, context: CallbackContext):
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    #
    # with open('callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())
    #
    # logger.info('user_input_data: %s', user_input_data)
    callback_query = update.callback_query
    data = callback_query.data

    bot_data = context.bot_data

    if not bot_data:
        user_data = get_user(update.effective_user.id)
        bot_data['user_data'] = user_data

    user = bot_data['user_data']

    match_obj = re.search('^received', data)

    if data == BUTTONS_DATA_DICT[7] or data == BUTTONS_DATA_DICT[8]:

        if data == BUTTONS_DATA_DICT[7]:

            lang = LANGS[0]
            text = "Til: O'zbekcha"
            reply_text = "Til o'zgartirildi"
            edited_text = '\U0001F1FA\U0001F1FF'

        elif data == BUTTONS_DATA_DICT[8]:

            lang = LANGS[1]
            text = "Язык: русский"
            reply_text = 'Язык был изменен'
            edited_text = '\U0001F1F7\U0001F1FA'

        context.bot.answer_callback_query(callback_query.id, reply_text)
        update_user_info(user['user_id'], lang=lang)
        bot_data['user_data']['lang'] = lang

        reply_keyboard = ReplyKeyboard('menu_keyboard', lang).get_keyboard()
        callback_query.edit_message_text(edited_text)
        callback_query.message.reply_text(text, reply_markup=reply_keyboard)

    elif match_obj:

        data = match_obj.string
        sender = get_user(data.split('_')[1])
        cargo_id = data.split('_')[-1]

        if update_cargo_status(cargo_id, 'received') == 'updated':

            if user['lang'] == LANGS[0]:
                text = "\U0001F197 Siz yukni qabul qildingiz.\n\n" \
                       "\U0001F6E1 <b><i><u>Cardel Online</u></i></b> " \
                       "xizmatidan foydalanganingiz uchun rahmat \U0001F609."

            if user['lang'] == LANGS[1]:
                text = "\U0001F197 Вы приняли груз.\n\n" \
                       "\U0001F609 Благодарим вас за использование услуги " \
                       "\U0001F6E1 <b><i><u>Cardel Online</u></i></b>."

            callback_query.message.reply_text(text, parse_mode=ParseMode.HTML)

            if sender['lang'] == LANGS[0]:
                text = f"\U00002705 Qabul qiluvchi: <b><i>[ <u>{user['name']} {user['surname']}</u> ]</i></b> " \
                       f"yukingizni qabul qildi.\n\n\U0001F6E1 <b><i><u>Cardel Online</u></i></b> " \
                       f"xizmatidan foydalanganingiz uchun rahmat \U0001F609."

            if sender['lang'] == LANGS[1]:
                text = f"\U00002705 Получатель: <b><i>[ <u>{user['name']} {user['surname']}</u> ]</i></b>" \
                       " принял вашу груз.\n\n\U0001F609 Благодарим вас за использование " \
                       "услуги \U0001F6E1 <b><i><u>Cardel Online</u></i></b>."

            context.bot.send_message(sender['user_id'], text, parse_mode=ParseMode.HTML)


inline_keyboard_handler = CallbackQueryHandler(main_inline_keyboard_callback, pattern='')
