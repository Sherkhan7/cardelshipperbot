# import sys
# sys.path.extend(['/home/sherzodbek/PycharmProjects/cardelshipperbot'])
import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler, CallbackContext)
from telegram.update import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from config.config import TOKEN

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def do_commands(update: Update, context: CallbackContext):
    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    command = update.message.text

    if command == '/start':
        inline_keyboard_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("\U0001F1FF O'zbekcha", callback_data='uzbek'),
            InlineKeyboardButton("\U0001F1FA Русский", callback_data='russian')
        ]])
        update.message.reply_text('Tilni tanlang. Выберите язык.',
                                  reply_markup=inline_keyboard_markup)


def keyboard_callback_handler(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data
    user_data = context.user_data
    user_data['LANG'] = data
    logger.info('user_data: %s', user_data)

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    with open('callback_query.json', 'w') as callback_query_file:
        callback_query_file.write(callback_query.to_json())

    if data == 'uzbek':
        reply_keyboard_markup = ReplyKeyboardMarkup([[
            KeyboardButton("\U0001F464 Kontaktimni yuborish", request_contact=True)
        ]], resize_keyboard=True)

        callback_query.message.reply_text(f'\U0001F44B Salom, {update.effective_user.first_name}\n'
                                  f'Davom etish uchun menga kontaktingizni yuboring \U0001F60A',
                                  reply_markup=reply_keyboard_markup)

    else:
        reply_keyboard_markup = ReplyKeyboardMarkup([[
            KeyboardButton("\U0001F464 Отправить мой контакт", request_contact=True)
        ]], resize_keyboard=True)

        callback_query.message.reply_text(f'\U0001F44B  Привет, {update.effective_user.first_name}\n'
                                  f'Чтобы продолжить, отправьте мне свой контакт \U0001F60A',
                                  reply_markup=reply_keyboard_markup)


def contact_callback(update: Update, context: CallbackContext):

    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.message.contact)

    user_data = context.user_data

    if user_data['LANG'] == 'uzbek':
        update.message.reply_text('Kontaktingiz qabul qilindi', reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text('Ваш контакт был принят', reply_markup=ReplyKeyboardRemove())


def main():
    updater = Updater(TOKEN, use_context=True)

    commands_handler = CommandHandler(['start'], do_commands, ~Filters.update.edited_message)
    callback_query_handler = CallbackQueryHandler(keyboard_callback_handler)
    contact_handler = MessageHandler(Filters.contact, contact_callback)

    # updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_handler(commands_handler)
    updater.dispatcher.add_handler(contact_handler)
    updater.dispatcher.add_handler(callback_query_handler)

    # updater.dispatcher.add_handler(message_handler)

    # updater.start_polling()
    # updater.idle()

    updater.start_webhook(listen='127.0.0.1', port=5001, url_path=TOKEN)
    updater.bot.set_webhook(webhook_url='https://cardel.ml/' + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()
