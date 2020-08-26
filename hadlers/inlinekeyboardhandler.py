from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import CallbackQueryHandler, CallbackContext, ConversationHandler, Filters, MessageHandler, \
    CommandHandler
from inlinekeyboards import InlineKeyboard, BUTTONS_DATA_DICT
from DB.main import *
from languages import LANGS
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def inline_keyboard_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    user_input_data = context.user_data
    user_input_data['lang'] = data

    user = get_user(update.effective_user.id)

    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    #
    # with open('callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())
    # print('inline keyboard callback')
    logger.info('user_input_data: %s', user_input_data)
    # logger.info('BUTTONS_DATA_DICT: %s', BUTTONS_DATA_DICT)


    if data == BUTTONS_DATA_DICT[1]:
        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('user_data_keyboard', 'uz')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text(f"Ism: {user['name']}\n"
                                             f"Familya: {user['surname']}",
                                             reply_markup=inline_keyboard)
        elif user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('user_data_keyboard', 'ru')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text(f"Имя: {user['name']}\n"
                                             f"Фамиля: {user['surname']}",
                                             reply_markup=inline_keyboard)

    elif data == BUTTONS_DATA_DICT[2]:
        pass

    elif data == BUTTONS_DATA_DICT[3]:

        if user['lang'] == LANGS[0]:

            callback_query.edit_message_text('Ismningizni kiriting:')

        elif user['lang'] == LANGS[1]:
            callback_query.edit_message_text('Введите ваше имя:')

        return 'new_name'

    elif data == BUTTONS_DATA_DICT[4]:
        if user['lang'] == LANGS[0]:

            callback_query.edit_message_text('Familyangizni kiriting:')

        elif user['lang'] == LANGS[1]:
            callback_query.edit_message_text('Введите свою фамилию:')

        return 'new_surname'

    elif data == BUTTONS_DATA_DICT[5]:

        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('langs_keyboard', 'uz')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text('Tilni tanlang:', reply_markup=inline_keyboard)

        elif user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('langs_keyboard', 'ru')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text('Выберите язык:', reply_markup=inline_keyboard)

    elif data == BUTTONS_DATA_DICT[6]:

        if user['lang'] == LANGS[0]:
            inline_keyboard = InlineKeyboard('main_keyboard', 'uz')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text('MENU', reply_markup=inline_keyboard)

        elif user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('main_keyboard', 'ru')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text('MENU', reply_markup=inline_keyboard)

    elif data == BUTTONS_DATA_DICT[7]:
        update_user_info(user['user_id'], lang='uz')

        if user['lang'] == LANGS[1]:
            inline_keyboard = InlineKeyboard('langs_keyboard', 'uz')

            inline_keyboard = inline_keyboard.get_keyboard()

            callback_query.edit_message_text('Tilni tanlang:', reply_markup=inline_keyboard)

            context.bot.answer_callback_query(callback_query.id, "Til: O'zbekcha")

    elif data == BUTTONS_DATA_DICT[8]:
        update_user_info(user['user_id'], lang='ru')
        inline_keyboard = InlineKeyboard('langs_keyboard', 'ru')

        inline_keyboard = inline_keyboard.get_keyboard()
        callback_query.edit_message_text('Выберите язык:', reply_markup=inline_keyboard)
        context.bot.answer_callback_query(callback_query.id, "Язык: русский")


inline_keyboard_handler = CallbackQueryHandler(inline_keyboard_callback)
