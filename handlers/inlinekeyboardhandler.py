from telegram import Update, ParseMode, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, CallbackContext
from replykeyboards import ReplyKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from DB.main import *
from languages import LANGS
from helpers import set_user_data_in_bot_data
from layouts import get_new_cargo_layout
from inlinekeyboards import InlineKeyboard
from config import GROUP_ID
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
    chat_data = context.chat_data

    # set bot_data[update.effective_user.id] -> dict
    set_user_data_in_bot_data(update.effective_user.id, bot_data)
    user = bot_data[update.effective_user.id]

    match_obj = re.search(r'^(\d+_(opened|closed))$', data)

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
        bot_data[update.effective_user.id]['lang'] = lang

        reply_keyboard = ReplyKeyboard('menu_keyboard', lang).get_keyboard()
        callback_query.edit_message_text(edited_text)
        callback_query.message.reply_text(text, reply_markup=reply_keyboard)

    elif match_obj:

        data = match_obj.string
        # print(data)
        cargo_id = data.split('_')[0]
        new_cargo_status = data.split('_')[-1]

        if update_cargo_status(cargo_id, new_cargo_status) == 'updated':

            cargo_data = get_cargo_by_id(cargo_id)
            chat_data['client_cargoes'] = get_client_cargoes(user['id'])

            shipping_datetime = cargo_data['shipping_datetime']
            cargo_data['date'] = shipping_datetime.strftime('%d-%m-%Y')
            cargo_data['time'] = shipping_datetime.strftime('%H:%M')

            if user['lang'] == LANGS[0]:
                close_text = 'E\'lonni yopish'
                open_text = 'E\'lonni qayta ochish'

            if user['lang'] == LANGS[1]:
                close_text = 'Закрыть объявление'
                open_text = 'Повторно открыть объявление'

            if user['lang'] == LANGS[2]:
                close_text = 'Еълонни ёпиш'
                open_text = 'Еълонни қайта очиш'

            if cargo_data['state'] == 'opened':
                button4_text = f'\U0001F534 {close_text}'
                button4_data = f'{cargo_data["id"]}_closed'

            elif cargo_data['state'] == 'closed':
                button4_text = f'\U0001F7E2 {open_text}'
                button4_data = f'{cargo_data["id"]}_opened'

            cargo_data['from_location'] = None
            cargo_data['to_location'] = None

            layout = get_new_cargo_layout(cargo_data, user['lang'])

            inline_keyboard = callback_query.message.reply_markup
            inline_keyboard['inline_keyboard'][-1][0] = InlineKeyboardButton(button4_text, callback_data=button4_data)

            if cargo_data['from_latitude'] or cargo_data['to_latitude']:

                if cargo_data['from_latitude']:
                    cargo_data['from_location'] = {
                        'latitude': cargo_data['from_latitude'],
                        'longitude': cargo_data['from_longitude']
                    }

                if cargo_data['to_latitude']:
                    cargo_data['to_location'] = {
                        'latitude': cargo_data['to_latitude'],
                        'longitude': cargo_data['to_longitude']
                    }

                inline_keyboard_2 = InlineKeyboard('geolocation_keyboard', lang='cy', data=cargo_data).get_keyboard()

            else:
                inline_keyboard_2 = None

            callback_query.answer()
            callback_query.edit_message_text(layout, parse_mode=ParseMode.HTML, reply_markup=inline_keyboard)

            layout_2 = get_new_cargo_layout(cargo_data, 'cy')

            if cargo_data['photo_id']:

                context.bot.edit_message_caption(GROUP_ID, cargo_data['message_id'], caption=layout_2,
                                                 reply_markup=inline_keyboard_2, parse_mode=ParseMode.HTML)
            else:
                context.bot.edit_message_text(layout_2, GROUP_ID, cargo_data['message_id'],
                                              reply_markup=inline_keyboard_2, parse_mode=ParseMode.HTML)

    else:
        callback_query.answer()

        match_obj_2 = re.search(r'^(w_\d+)$', data)

        if match_obj_2:
            data = match_obj_2.string.split('_')[-1]
        else:
            data = ''

        if data.isdigit():

            chat_data['client_cargoes'] = get_client_cargoes(user['id'])

            length = len(chat_data['client_cargoes'])
            wanted = int(data[0])
            client_cargoes = chat_data['client_cargoes']

            wanted_cargo_data = chat_data['client_cargoes'][wanted - 1]

            # print(wanted_cargo_data)

            shipping_datetime = wanted_cargo_data['shipping_datetime']
            wanted_cargo_data['date'] = shipping_datetime.strftime('%d-%m-%Y')
            wanted_cargo_data['time'] = shipping_datetime.strftime('%H:%M')

            layout = get_new_cargo_layout(wanted_cargo_data, user['lang'])
            inline_keyboard = InlineKeyboard('paginate_keyboard', user['lang'],
                                             data=(wanted, length, client_cargoes)).get_keyboard()

            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)


inline_keyboard_handler = CallbackQueryHandler(main_inline_keyboard_callback, pattern='')
