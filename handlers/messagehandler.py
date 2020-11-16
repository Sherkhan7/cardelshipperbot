from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update
from inlinekeyboards import InlineKeyboard
from layouts import get_new_cargo_layout, get_user_info_layout
from replykeyboards import ReplyKeyboard
from helpers import set_user_data_in_bot_data
from pprint import pprint
from DB import get_user_cargoes
from languages import LANGS
from replykeyboards.replykeyboardtypes import reply_keyboard_types
from replykeyboards.replykeyboardvariables import *
from inlinekeyboards.inlinekeyboardvariables import *
from globalvariables import *


def message_handler_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    full_text = update.message.text
    text = full_text.split(' ', 1)[-1]

    bot_data = context.bot_data
    chat_data = context.chat_data

    # set bot_data[update.effective_user.id] -> dict
    set_user_data_in_bot_data(update.effective_user.id, bot_data)
    user = bot_data[update.effective_user.id]
    pprint(bot_data)

    if user:

        if text == reply_keyboard_types[menu_keyboard][user[LANG]][3]:

            client_cargoes = get_user_cargoes(user[TG_ID])
            length = len(client_cargoes)

            if user[LANG] == LANGS[0]:
                reply_text = "Sizda hali e'lonlar mavjud emas"

            if user[LANG] == LANGS[1]:
                reply_text = "У вас нет объявлений пока"

            if user[LANG] == LANGS[2]:
                reply_text = "Сизда ҳали эълонлар мавжуд емас"

            reply_text = f'\U0001F615 {reply_text}'
            inline_keyboard = None

            if length > 0:
                chat_data['client_cargoes'] = client_cargoes
                wanted = 1

                wanted_cargo_data = client_cargoes[wanted - 1]

                shipping_datetime = wanted_cargo_data['shipping_datetime']
                wanted_cargo_data[DATE] = shipping_datetime.strftime('%d-%m-%Y')
                wanted_cargo_data[TIME] = shipping_datetime.strftime('%H:%M')
                wanted_cargo_data[NAME] = user[NAME]
                wanted_cargo_data[SURNAME] = user[SURNAME]
                wanted_cargo_data[USERNAME] = user[USERNAME]

                reply_text = get_new_cargo_layout(wanted_cargo_data, user[LANG])
                inline_keyboard = InlineKeyboard(paginate_keyboard, user[LANG],
                                                 data=(wanted, length, client_cargoes)).get_keyboard()

            update.message.reply_html(reply_text, reply_markup=inline_keyboard)

        elif text == reply_keyboard_types[menu_keyboard][user[LANG]][4]:

            reply_keyboard = ReplyKeyboard(settings_keyboard, user[LANG]).get_keyboard()
            update.message.reply_text(full_text, reply_markup=reply_keyboard)

        elif text == reply_keyboard_types[settings_keyboard][user[LANG]][1]:

            inline_keyboard = InlineKeyboard(user_data_keyboard, user[LANG]).get_keyboard()
            update.message.reply_html(get_user_info_layout(user), reply_markup=inline_keyboard)

        elif text == reply_keyboard_types[settings_keyboard][user[LANG]][2]:

            reply_text = 'Tilni tanlang\nВыберите язык\nТилни танланг'

            inline_keyboard = InlineKeyboard(langs_keyboard).get_keyboard()
            update.message.reply_text(reply_text, reply_markup=inline_keyboard)

        elif text == reply_keyboard_types[settings_keyboard][user[LANG]][3]:

            reply_keyboard = ReplyKeyboard(menu_keyboard, user[LANG]).get_keyboard()
            update.message.reply_text(full_text, reply_markup=reply_keyboard)

        else:

            thinking_emoji = '\U0001F914'

            reply_keyboard = ReplyKeyboard(menu_keyboard, user[LANG]).get_keyboard()
            update.message.reply_text(thinking_emoji, quote=True, reply_markup=reply_keyboard)

    else:

        reply_text = "\U000026A0 Siz ro'yxatdan o'tmagansiz !\nBuning uchun /start ni bosing.\n\n'" \
                     "\U000026A0 Вы не зарегистрированы !\nДля этого нажмите /start\n\n" \
                     "\U000026A0 Сиз рўйхатдан ўтмагансиз !\nБунинг учун /start ни босинг"

        update.message.reply_text(reply_text)


message_handler = MessageHandler(Filters.text & (~ Filters.command), message_handler_callback)
