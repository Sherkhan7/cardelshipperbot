from telegram import Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, CallbackContext
from inlinekeyboards import InlineKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from DB.main import *
from languages import LANGS
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def main_inline_keyboard_callback(update: Update, context: CallbackContext):
    print('main_inline_keyboard')
    callback_query = update.callback_query
    data = callback_query.data
    user_input_data = context.user_data

    user = get_user(update.effective_user.id)

    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    #
    # with open('callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())
    # logger.info('user_input_data: %s', user_input_data)


    # if int(data) in range(0, 24):
    #     print(data)
    #     inline_keyboard = []
    #     for i in range(10, 60, 20):
    #         inline_keyboard.append([
    #             InlineKeyboardButton(f'{data}:{i}', callback_data=f'{data}:{i}')
    #         ])
    #         if i == 50:
    #             inline_keyboard[len(inline_keyboard)-1].append(InlineKeyboardButton('orqaga', callback_data='back'))
    #         else:
    #             inline_keyboard[len(inline_keyboard) - 1].append(
    #                 InlineKeyboardButton(f'{data}:{i + 10}', callback_data=f'{data}:{i + 10}'))
    #
    #     callback_query.edit_message_reply_markup(InlineKeyboardMarkup(inline_keyboard))

    # print(x)

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


inline_keyboard_handler = CallbackQueryHandler(main_inline_keyboard_callback, pattern='')
