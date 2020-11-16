from telegram import Update
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters,
                          CallbackQueryHandler)
from inlinekeyboards import InlineKeyboard
from filters import *
from replykeyboards import ReplyKeyboard
from DB import insert_user
from helpers import set_user_data_in_bot_data
from languages import LANGS
from globalvariables import *
from replykeyboards.replykeyboardvariables import *
from inlinekeyboards.inlinekeyboardvariables import *
from helpers import wrap_tags
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

FULLNAME, LANG = ('fullname', 'lang')


def do_command(update: Update, context: CallbackContext):
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    command = update.message.text

    user_input_data = context.user_data
    bot_data = context.bot_data

    # set bot_data[update.effective_user.id] -> dict
    set_user_data_in_bot_data(update.effective_user.id, bot_data)
    user = bot_data[update.effective_user.id]

    # logger.info('user_input_data: %s', user_input_data)

    if command == '/start' or command == '/menu':

        if user:

            if user['lang'] == LANGS[0]:
                text = "Siz ro'yxatdan o'tgansiz"

            if user['lang'] == LANGS[1]:
                text = "Вы зарегистрированы"

            if user['lang'] == LANGS[2]:
                text = "Сиз рўйхатдан ўтгансиз"

            text = f'\U000026A0 {text} !'

            if command == '/menu':

                if user['lang'] == LANGS[0]:
                    reply_text = "Menyu"

                if user['lang'] == LANGS[1]:
                    reply_text = "Меню"

                if user['lang'] == LANGS[2]:
                    reply_text = "Меню"

                text = f'\U0001F4D6 {reply_text}'

            reply_keyboard = ReplyKeyboard(menu_keyboard, user['lang']).get_keyboard()
            update.message.reply_text(text, reply_markup=reply_keyboard)

            return ConversationHandler.END

        else:

            user_input_data[TG_ID] = update.effective_user.id
            user_input_data[USERNAME] = update.effective_user.username

            inline_keyboard = InlineKeyboard(langs_keyboard).get_keyboard()
            update.message.reply_text('Tilni tanlang\nВыберите язык\nТилни танланг', reply_markup=inline_keyboard)

        return LANG


def lang_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    callback_query = update.callback_query

    if callback_query:

        data = callback_query.data

        user_input_data = context.user_data
        user_input_data[LANG] = data

        logger.info('user_input_data: %s', user_input_data)

        if data == LANGS[0]:
            edit_text = "Til: \U0001F1FA\U0001F1FF"
            text = "Salom !\n" \
                   "Ism va familyangizni quyidagi formatda yuboring"
            example = "Misol: Sherzod Esanov"

        if data == LANGS[1]:
            edit_text = 'Язык: \U0001F1F7\U0001F1FA'
            text = 'Привет !\n' \
                   'Отправьте свое имя и фамилию в формате ниже'
            example = 'Пример: Шерзод Эсанов'

        if data == LANGS[2]:
            edit_text = "Тил: \U0001F1FA\U0001F1FF"
            text = "Салом !\n" \
                   "Исм ва фамилянгизни қуйидаги форматда юборинг"
            example = "Мисол: Шерзод Эсанов"

        text = f'\U0001F44B {text}:\n\n {wrap_tags(example)}'

        callback_query.edit_message_text(edit_text)
        callback_query.message.reply_html(text)

        return FULLNAME

    else:

        update.message.reply_text('Tilni tanlang. Выберите язык. Тилни танланг', quote=True)

        return LANG


def fullname_callback(update: Update, context: CallbackContext):
    # with open('../update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    text = update.message.text

    user_input_data = context.user_data
    bot_data = context.bot_data

    logger.info('user_input_data: %s', user_input_data)

    fullname = fullname_filter(text)

    if fullname:

        user_input_data[NAME] = fullname[0]
        user_input_data[SURNAME] = fullname[1]

        insert_user(user_input_data)
        set_user_data_in_bot_data(update.effective_user.id, bot_data)

        if user_input_data[LANG] == LANGS[0]:
            text = "Tabriklaymiz !\n" \
                   "Siz ro'yxatdan muvofaqqiyatli o'tdingiz\n\n" \
                   "E'lon berishingiz mumkin"

        if user_input_data[LANG] == LANGS[1]:
            text = "Поздравляем !\n" \
                   "Вы успешно зарегистрировались\n\n" \
                   "Вы можете помешать объявление"

        if user_input_data[LANG] == LANGS[2]:
            text = "Табриклаймиз !\n" \
                   "Сиз рўйхатдан мувофаққиятли ўтдингиз\n\n" \
                   "Эълон беришингиз мумкин"

        text = '\U0001F44F\U0001F44F\U0001F44F ' + text

        reply_keyboard = ReplyKeyboard(menu_keyboard, user_input_data[LANG]).get_keyboard()
        update.message.reply_text(text, reply_markup=reply_keyboard)

        user_input_data.clear()
        return ConversationHandler.END

    else:

        if user_input_data[LANG] == LANGS[0]:
            text = "Ism va familya xato yuborildi !\n" \
                   "Qaytadan quyidagi formatda yuboring"
            example = "Misol: Sherzod Esanov"

        if user_input_data[LANG] == LANGS[1]:
            text = 'Имя и фамилия введено неверное !\n' \
                   'Отправьте еще раз в следующем формате'
            example = 'Пример: Шерзод Эсанов'

        if user_input_data[LANG] == LANGS[2]:
            text = "Исм ва фамиля хато юборилди !\n" \
                   "Қайтадан қуйидаги форматда юборинг"
            example = "Мисол: Шерзод Эсанов"

        text = f'\U000026A0 {text}:\n\n {wrap_tags(example)}'

        update.message.reply_html(text, quote=True)

        return FULLNAME


conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler(['start', 'menu'], do_command, filters=~Filters.update.edited_message),
    ],
    states={
        LANG: [CallbackQueryHandler(lang_callback), MessageHandler(Filters.text, lang_callback)],

        FULLNAME: [MessageHandler(Filters.text, fullname_callback)],
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ], )
