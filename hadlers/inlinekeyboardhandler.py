from telegram import Update, ParseMode
from telegram.ext import CallbackQueryHandler, CallbackContext
from inlinekeyboards import InlineKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from DB.main import *
from languages import LANGS
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def main_inline_keyboard_callback(update: Update, context: CallbackContext):
    print('main_inline_keyboard')

    callback_query = update.callback_query
    data = callback_query.data

    user = get_user(update.effective_user.id)

    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    #
    # with open('callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())

    # logger.info('user_input_data: %s', user_input_data)

    match_obj = re.search('^received', data)

    if data == BUTTONS_DATA_DICT[1]:

        if user['lang'] == LANGS[0]:
            name = 'Ism'
            surname = 'Familya'
            phone = 'Tel 1'
            phone_2 = 'Tel 2'

        if user['lang'] == LANGS[1]:
            name = 'Имя'
            surname = 'Фамиля'
            phone = 'Тел номер 1'
            phone_2 = 'Тел номер 2'

        inline_keyboard = InlineKeyboard('user_data_keyboard', user['lang'])

        text = f"<b><i>{name}:</i></b> <u>{user['name']}</u> \n\n" \
               f"<b><i>{surname}:</i> <u>{user['surname']}</u></b> \n\n" \
               f"<b><i>{'-'.ljust(30, '-')}</i></b> \n" \
               f"<b><i>\U0000260E {phone}: </i><u>{user['phone_number']}</u></b> \n\n" \
               f"<b><i>\U0000260E {phone_2}: </i><u>{user['phone_number2']}</u></b> \n"

        callback_query.edit_message_text(text, reply_markup=inline_keyboard.get_keyboard(),
                                         parse_mode=ParseMode.HTML)

    elif data == BUTTONS_DATA_DICT[6]:

        inline_keyboard = InlineKeyboard('main_keyboard', user['lang'])

        callback_query.edit_message_text('MENU', reply_markup=inline_keyboard.get_keyboard())

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
