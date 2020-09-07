# import sys
# sys.path.extend(['/home/sherzodbek/PycharmProjects/cardelshipperbot'])

from telegram.ext import Updater, CallbackQueryHandler
from config.config import TOKEN
from hadlers import (message_handler, inline_keyboard_handler, conversation_handler,
                     changedataconversation_handler, new_cargo_conversation_handler)


def main():
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(new_cargo_conversation_handler)
    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_handler(changedataconversation_handler)

    updater.dispatcher.add_handler(inline_keyboard_handler)
    updater.dispatcher.add_handler(message_handler)

    # updater.dispatcher.add_handler(handler_2)
    # updater.dispatcher.add_handler(handler_1)
    # updater.dispatcher.add_handler(regions_callback_query_handler)
    # hendler1 = CommandHandler('new', do_new, filters=Filters.update.edited_message)
    # hendler2 = CommandHandler('new', do_new2, filters=Filters.update.edited_message)
    # hendler1 = CommandHandler('new', do_new)
    # hendler2 = MessageHandler(Filters.text, do_new2)
    # hendler2 = CommandHandler('new', do_new2, filters=Filters.update.edited_message)
    # hendler1 = MessageHandler(Filters.text&~Filters.command, do_new)
    # updater.dispatcher.add_handler(hendler2)
    # updater.dispatcher.add_handler(hendler1)

    updater.start_polling()
    updater.idle()

    # updater.start_webhook(listen='127.0.0.1', port=5001, url_path=TOKEN)
    # updater.bot.set_webhook(url='https://cardel.ml/' + TOKEN)
    # updater.idle()


if __name__ == '__main__':
    main()
