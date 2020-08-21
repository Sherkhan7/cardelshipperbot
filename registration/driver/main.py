import sys
sys.path.extend(['/home/sherzodbek/PycharmProjects/cardelshipperbot'])
import logging
import random
from registration.driver.DB.main import *
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler, CallbackContext)
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from config.config import TOKEN, ROOT_PATH


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

SPECIAL_CODE = {}
CHAT_ID, NAME, SURNAME, GENDER, REGION, TEL_NUM, CONFIRMATION, CODE = (
    'chat_id', 'name', 'surname', 'gender', 'region', 'tel_num', 'confirmation', 'code'
)


def do_register(update: Update, context):
    user = select(update.effective_user.id)
    if user is None:
        user_data = context.user_data
        user_data[CHAT_ID] = update.effective_user.id
        update.message.reply_text(
            text=f'Assalomu alaykum, {update.effective_user.first_name}\n\n'
                 f'Registratsiyaga xush kelibsiz !\n'
                 f'Ismingizni kiriting...',
        )
    else:
        update.message.reply_text("Siz registratsiyadan o'tgansiz \U0001F600")
        return ConversationHandler.END

    # writing update to the json file
    try:
        f = open("update.json", "w")
        f.write(update.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()
    # writing message to the json file
    try:
        f = open("message.json", "w")
        f.write(update.message.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    return NAME


def name_handler(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data[NAME] = update.message.text
    logger.info('user_data: %s', user_data)
    update.message.reply_text(
        text=f'Familyangizni kiriting...'
    )

    try:
        f = open("update.json", "w")
        f.write(update.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    try:
        f = open("message.json", "w")
        f.write(update.message.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    return SURNAME


def surname_handler(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data[SURNAME] = update.message.text
    logger.info('user_data: %s', user_data)

    update.message.reply_text(
        text=f'Jinsingiz...',
        reply_markup=ReplyKeyboardMarkup([['Erkak', 'Ayol']], resize_keyboard=True, one_time_keyboard=True)
    )

    try:
        f = open("update.json", "w")
        f.write(update.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    try:
        f = open("message.json", "w")
        f.write(update.message.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    return GENDER


def gender_handler(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data[GENDER] = update.message.text
    logger.info('user_data: %s', user_data)

    update.message.reply_text(
        text='Hududingiz kiriting...',
        reply_markup=ReplyKeyboardMarkup(
            [['Toshkent shahri', 'Toshkent viloyati']], resize_keyboard=True, one_time_keyboard=True
        )
    )

    try:
        f = open("update.json", "w")
        f.write(update.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    try:
        f = open("message.json", "w")
        f.write(update.message.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    return REGION


def region_handler(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data[REGION] = update.message.text
    logger.info('user_data: %s', user_data)

    update.message.reply_text(
        text=f'Telefon raqamingizni kiriting...\nMasalan:\n991234567',
        reply_markup=ReplyKeyboardRemove()
    )

    try:
        f = open("update.json", "w")
        f.write(update.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    try:
        f = open("message.json", "w")
        f.write(update.message.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    return TEL_NUM


def tel_num_handler(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data[TEL_NUM] = update.message.text
    logger.info('user_data: %s', user_data)

    update.message.reply_text(
        text=f"Quyidagi kiritgan ma'lumotlaringizni tasdiqlaysizmi?\n\n"
             f"Ism: {user_data[NAME]}\n"
             f"Familya: {user_data[SURNAME]}\n"
             f"Jinsi: {user_data[GENDER]}\n"
             f"Region: {user_data[REGION]}\n"
             f"TEL: {user_data[TEL_NUM]}\n",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton('Ha', callback_data='callback_button_yes'),
            InlineKeyboardButton("Yo'q", callback_data='callback_button_no')
        ]])
    )

    try:
        f = open("update.json", "w")
        f.write(update.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    try:
        f = open("message.json", "w")
        f.write(update.message.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    return CONFIRMATION


def keyboard_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    user_data = context.user_data
    user_data[CONFIRMATION] = data
    logger.info('user_data: %s', user_data)

    try:
        f = open("update.json", "w")
        f.write(update.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    try:
        f = open("callbackQuery.json", "w")
        f.write(query.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    if data == 'callback_button_yes':
        global SPECIAL_CODE
        SPECIAL_CODE[update.effective_user.id] = random.randint(100000, 999999)

        # context.bot.send_message(chat_id=-1001197724765,
        #                          text=f'Hurmatli, {update.effective_user.first_name}\nSiz uchun maxsus kod:\n{SPECIAL_CODE}')

        query.message.reply_text(
            f'Hurmatli, {update.effective_user.first_name}\nSiz uchun maxsus kod:\n{SPECIAL_CODE[update.effective_user.id]}')

        return CODE
    elif data == 'callback_button_no':
        query.message.reply_text(
            text='Siz registratsiyani bekor qildingiz \U0001F614'
        )

        return ConversationHandler.END


def code_handler(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data[CODE] = update.message.text
    logger.info('user_data: %s', user_data)

    with open("update.json", "w") as f:
        f.write(update.to_json())

    # try:
    #     f = open("update.json", "w")
    #     f.write(update.to_json())
    # except Exception as e:
    #     raise e
    # finally:
    #     f.close()

    try:
        f = open("message.json", "w")
        f.write(update.message.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    code = update.message.text
    if int(code) == SPECIAL_CODE[update.effective_user.id]:
        insert(user_data)
        update.message.reply_text(
            "Tabriklaymiz, siz registratsiyadan muvofaqqiyatli o'tdingiz\n\U0001F44F\U0001F44F\U0001F44F")
        return ConversationHandler.END
    else:
        update.message.reply_text("Maxsus kodni xato kiritdingiz.\nKodni qaytadan kiriting...")
        return CODE


def do_cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Siz registratsiyani bekor qildingiz \U0001F614'
    )

    return ConversationHandler.END


def do_commands(update: Update, context: CallbackContext):
    command = update.message.text
    if command == '/start':
        update.message.reply_text(
            text=f'Assalomu alaykum, {update.effective_user.first_name}\n\n'
                 f"Bot bilan ishlash uchun avval registratsiyadan o'ting\n"
                 f"Buning uchun /register kommandasini jo'nating",
        )
    elif command == '/getme':
        if not conn.is_connected():
            conn.reconnect()
            # mycursor.reset()
            update.message.reply_text("connection reconnected")
        # with conn.reconnect() as connection:

        user = select(update.effective_chat.id)
        # conn.close()

        if user is None:
            update.message.reply_text(
                "Bazadan topilmadi \U0001F62C\nSiz registratsiyadan o'tishingiz kerak. Buning uchun /register kommandasini jo'nating")
        else:
            update.message.reply_text(user)
    elif command == '/getall':
        users = select_all()
        update.message.reply_text(users)
    elif command == '/update':
        result = update_user_info(update.effective_user.id)
        update.message.reply_text(result)


def do_echo(update: Update, context: CallbackContext):
    try:
        f = open("update.json", "w")
        f.write(update.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()

    try:
        f = open("message.json", "w")
        f.write(update.message.to_json())
    except Exception as e:
        raise e
    finally:
        f.close()
        update.message.reply_text(update.to_json())


def main():
    updater = Updater(TOKEN, use_context=True)

    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('register', do_register)
        ],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, name_handler)],
            SURNAME: [MessageHandler(Filters.text & ~Filters.command, surname_handler)],
            GENDER: [MessageHandler(Filters.text & ~Filters.command, gender_handler)],
            REGION: [MessageHandler(Filters.text & ~Filters.command, region_handler)],
            TEL_NUM: [MessageHandler(Filters.text & ~Filters.command, tel_num_handler)],
            CONFIRMATION: [CallbackQueryHandler(keyboard_callback_handler)],
            CODE: [MessageHandler(Filters.text & ~Filters.command, code_handler)],
        },
        fallbacks=[
            CommandHandler('cancel', do_cancel)
        ]
    )

    message_handler = MessageHandler(Filters.text & ~Filters.command, do_echo)
    command_handler = CommandHandler(['start', 'getme', 'getall', 'update'], do_commands, Filters.text)

    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_handler(command_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

    # updater.start_webhook(listen='127.0.0.1', port=5000, url_path=TOKEN)
    # updater.bot.set_webhook(webhook_url='https://cardel.ml/' + TOKEN)


if __name__ == '__main__':
    main()
