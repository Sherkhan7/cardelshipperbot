from telegram.ext import Filters, MessageHandler, CallbackContext
from telegram import Update
from inlinekeyboards import InlineKeyboard
from layouts import *
from replykeyboards import ReplyKeyboard
from helpers import set_user_data_in_bot_data
from pprint import pprint
from DB import get_client_cargoes


def message_handler_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    # context.bot.edit_message_text('edited_text', -1001384173376, 315)
    full_text = update.message.text
    text = full_text.split(' ', 1)[-1]

    bot_data = context.bot_data
    chat_data = context.chat_data

    # set bot_data[update.effective_user.id] -> dict
    set_user_data_in_bot_data(update.effective_user.id, bot_data)
    user = bot_data[update.effective_user.id]
    pprint(bot_data)

    if user:

        if text == 'Mening e\'lonlarim' or text == 'Мои объявления':

            client_cargoes = get_client_cargoes(user['id'])
            length = len(client_cargoes)

            if user['lang'] == LANGS[0]:
                reply_text = 'Sizda hali e\'lonlar mavjud emas'

            if user['lang'] == LANGS[1]:
                reply_text = 'У вас нет объявлений пока'

            if user['lang'] == LANGS[2]:
                reply_text = 'Сизда ҳали еълонлар мавжуд емас'

            reply_text = f'\U0001F615 {reply_text}'
            inline_keyboard = None

            if length > 0:
                chat_data['client_cargoes'] = client_cargoes
                wanted = 1

                wanted_cargo_data = client_cargoes[wanted - 1]
                shipping_datetime = wanted_cargo_data['shipping_datetime']
                wanted_cargo_data[DATE] = shipping_datetime.strftime('%d-%m-%Y')
                wanted_cargo_data[TIME] = shipping_datetime.strftime('%H:%M')

                reply_text = get_new_cargo_layout(wanted_cargo_data, user)
                inline_keyboard = InlineKeyboard('paginate_keyboard', user['lang'],
                                                 data=(wanted, length, client_cargoes)).get_keyboard()

            update.message.reply_html(reply_text, reply_markup=inline_keyboard)

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

            thinking_emoji = '\U0001F914'

            reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang']).get_keyboard()
            update.message.reply_text(thinking_emoji, quote=True, reply_markup=reply_keyboard)

    else:

        reply_text = '\U000026A0 Siz ro\'yxatdan o\'tmagansiz !\nBuning uchun /start ni bosing.\n\n' \
                     '\U000026A0 Вы не зарегистрированы !\nДля этого нажмите /start.'

        update.message.reply_text(reply_text)


message_handler = MessageHandler(Filters.text & (~ Filters.command), message_handler_callback)
