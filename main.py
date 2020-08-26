# import sys
# sys.path.extend(['/home/sherzodbek/PycharmProjects/cardelshipperbot'])
from telegram.ext import Updater
from config.config import TOKEN
from hadlers import (message_handler, conversation_handler,
                     changedataconversation_handler, inline_keyboard_handler)


# def do_menu(update, context):
#     command = update.message.text
#
#     if command == '/menu':
#
#         if user:
#
#             user = get_user(update.effective_user.id)
#
#             if user['lang'] == LANGS[0]:
#                 inline_keyboard = InlineKeyboard('main_keyboard', 'uz')
#
#                 update.message.reply_text("MENU", reply_markup=inline_keyboard.get_keyboard())
#
#             elif user['lang'] == LANGS[1]:
#                 inline_keyboard = InlineKeyboard('main_keyboard', 'ru')
#
#                 update.message.reply_text("MENU", reply_markup=inline_keyboard.get_keyboard())
#
#             return ConversationHandler.END
#
#         else:
#             update.message.reply_text("Avval ro'yxatdan o'ting.\nСначала зарегистрируйтесь.")
#
#             update.message.reply_text('Tilni tanlang. Выберите язык.', reply_markup=lang_inlinekeyboard)
#
#             return LANG

def do_new(update, context):
    print('Inside do_new')


def do_new2(update, context):
    print('Inside do_new2')


def main():
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_handler(changedataconversation_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(inline_keyboard_handler)
    # hendler1 = CommandHandler('new', do_new, filters=Filters.update.edited_message)
    # hendler2 = CommandHandler('new', do_new2, filters=Filters.update.edited_message)
    # hendler1 = CommandHandler('new', do_new)
    # hendler2 = MessageHandler(Filters.text, do_new2)
    # hendler2 = CommandHandler('new', do_new2, filters=Filters.update.edited_message)
    # hendler1 = MessageHandler(Filters.text&~Filters.command, do_new)
    # updater.dispatcher.add_handler(hendler2)
    # updater.dispatcher.add_handler(hendler1)

    # updater.start_polling()
    # updater.idle()

    updater.start_webhook(listen='127.0.0.1', port=5001, url_path=TOKEN)
    updater.bot.set_webhook(url='https://cardel.ml/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
