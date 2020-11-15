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
from inlinekeyboards.inlinekeyboardtypes import inline_keyboard_types
from inlinekeyboards.inlinekeyboardvariables import *
from globalvariables import *
from replykeyboards.replykeyboardvariables import *
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def main_inline_keyboard_callback(update: Update, context: CallbackContext):
    # with open('callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())

    # logger.info('user_input_data: %s', user_input_data)
    callback_query = update.callback_query
    data = callback_query.data

    bot_data = context.bot_data
    chat_data = context.chat_data

    # set bot_data[update.effective_user.id] -> dict
    set_user_data_in_bot_data(update.effective_user.id, bot_data)
    user = bot_data[update.effective_user.id]

    match_obj = re.search(r'^(\d+_(opened|closed))$', data)

    if data == BUTTONS_DATA_DICT[7] or data == BUTTONS_DATA_DICT[8] or data == BUTTONS_DATA_DICT[9]:

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

        elif data == BUTTONS_DATA_DICT[9]:
            lang = LANGS[2]
            text = "Тил: Ўзбекча"
            reply_text = "Тил ўзгартирилди"
            edited_text = '\U0001F1FA\U0001F1FF'

        context.bot.answer_callback_query(callback_query.id, reply_text)
        update_user_info(user['user_id'], lang=lang)
        bot_data[update.effective_user.id]['lang'] = lang

        reply_keyboard = ReplyKeyboard(menu_keyboard, lang).get_keyboard()
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
            cargo_data[DATE] = shipping_datetime.strftime('%d-%m-%Y')
            cargo_data[TIME] = shipping_datetime.strftime('%H:%M')
            cargo_data[FROM_LOCATION] = None
            cargo_data[TO_LOCATION] = None
            cargo_data[NAME] = user[NAME]
            cargo_data[SURNAME] = user[SURNAME]
            cargo_data[USERNAME] = user[USERNAME]

            close_text = inline_keyboard_types[paginate_keyboard][user[LANG]][0]
            open_text = inline_keyboard_types[paginate_keyboard][user[LANG]][1]

            layout = get_new_cargo_layout(cargo_data, user[LANG])
            layout_2 = get_new_cargo_layout(cargo_data, 'cy')

            if cargo_data[STATE] == 'opened':
                button4_text = f'\U0001F534 {close_text}'
                button4_data = f'{cargo_data[ID]}_closed'

            elif cargo_data[STATE] == 'closed':
                button4_text = f'\U0001F7E2 {open_text}'
                button4_data = f'{cargo_data[ID]}_opened'
                layout_2 = get_new_cargo_layout(cargo_data, 'cy', hide_user_data=True)

            inline_keyboard = callback_query.message.reply_markup
            inline_keyboard['inline_keyboard'][-1][0] = InlineKeyboardButton(button4_text, callback_data=button4_data)

            if cargo_data['from_latitude'] or cargo_data['to_latitude']:

                if cargo_data['from_latitude']:
                    cargo_data[FROM_LOCATION] = {
                        'latitude': cargo_data['from_latitude'],
                        'longitude': cargo_data['from_longitude']
                    }

                if cargo_data['to_latitude']:
                    cargo_data[TO_LOCATION] = {
                        'latitude': cargo_data['to_latitude'],
                        'longitude': cargo_data['to_longitude']
                    }

                inline_keyboard_2 = InlineKeyboard(confirm_keyboard, lang='cy', data=cargo_data,
                                                   geolocation=True).get_keyboard()

            else:
                inline_keyboard_2 = None

            callback_query.answer()
            callback_query.edit_message_text(layout, parse_mode=ParseMode.HTML, reply_markup=inline_keyboard)

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
            wanted_cargo_data[DATE] = shipping_datetime.strftime('%d-%m-%Y')
            wanted_cargo_data[TIME] = shipping_datetime.strftime('%H:%M')
            wanted_cargo_data[NAME] = user[NAME]
            wanted_cargo_data[SURNAME] = user[SURNAME]
            wanted_cargo_data[USERNAME] = user[USERNAME]

            layout = get_new_cargo_layout(wanted_cargo_data, user[LANG])
            inline_keyboard = InlineKeyboard(paginate_keyboard, user[LANG],
                                             data=(wanted, length, client_cargoes)).get_keyboard()

            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)


inline_keyboard_handler = CallbackQueryHandler(main_inline_keyboard_callback)
