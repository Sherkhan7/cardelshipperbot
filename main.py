# import sys
# sys.path.extend(['/home/sherzodbek/PycharmProjects/cardelshipperbot'])
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler, CallbackContext, )
from telegram import Update, ReplyKeyboardRemove
from inlinekeyboard import inlinekeyboard, keyboard_callback_handler
from config.config import TOKEN
from contact import contact_callback
from DB.main import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def do_command(update: Update, context: CallbackContext):
    command = update.message.text

    if command == '/start':
        inline_keyboard_markup = inlinekeyboard
        update.message.reply_text('Tilni tanlang. Выберите язык.',
                                  reply_markup=inline_keyboard_markup)

    if command == '/getme':
        user = select(update.effective_user.id)
        update.message.reply_text(user)


def main():
    updater = Updater(TOKEN, use_context=True)

    command_handler = CommandHandler(['start', 'getme'], callback=do_command, filters=~Filters.update.edited_message)
    callback_query_handler = CallbackQueryHandler(keyboard_callback_handler)
    contact_handler = MessageHandler(Filters.contact, contact_callback)

    # updater.dispatcher.add_handler(conversation_handler)
    # updater.dispatcher.add_handler(message_handler)

    updater.dispatcher.add_handler(command_handler)
    updater.dispatcher.add_handler(callback_query_handler)
    updater.dispatcher.add_handler(contact_handler)

    # updater.start_polling()
    # updater.idle()

    updater.start_webhook(listen='127.0.0.1', port=5001, url_path=TOKEN)
    updater.bot.set_webhook(url='https://cardel.ml/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
