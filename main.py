# import sys
# sys.path.extend(['/home/sherzodbek/PycharmProjects/cardelshipperbot'])
from telegram.ext import Updater
from config.config import TOKEN
from conversation import conversation_handler
from menu import menu_handler


def main():
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_handler(menu_handler)
    # updater.dispatcher.add_handler(user_data_menu_hadler)

    # updater.dispatcher.add_handler(message_handler)
    # updater.dispatcher.add_handler(command_handler)
    # updater.dispatcher.add_handler(callback_query_handler)
    # updater.dispatcher.add_handler(contact_handler)

    # updater.start_polling()
    # updater.idle()

    updater.start_webhook(listen='127.0.0.1', port=5001, url_path=TOKEN)
    updater.bot.set_webhook(url='https://cardel.ml/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
