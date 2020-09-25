# import sys
# sys.path.extend(['/home/sherzodbek/PycharmProjects/cardelshipperbot'])
from telegram.ext import Updater, ConversationHandler, CallbackQueryHandler, CallbackContext, CommandHandler, \
    MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from config.config import TOKEN
from hadlers import (message_handler, inline_keyboard_handler, conversation_handler,
                     changedataconversation_handler, new_cargo_conversation_handler)
from layouts import *
from inlinekeyboards import InlineKeyboard
from replykeyboards import ReplyKeyboard
from hadlers import edit_conversation_handler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

f = open('jsons/cargo.json', 'r')
cargo_data = json.loads(f.read())


def cargo_callback(update: Update, context: CallbackContext):
    # print('cargo_callback')
    user_input_data = context.user_data
    user_input_data.update(cargo_data)

    logger.info('user_input_data: %s', user_input_data)

    user = get_user(update.effective_user.id)
    layout = get_new_cargo_layout(user_input_data, user)

    inline_keyboard = InlineKeyboard('confirm_keyboard', user['lang'], data=user_input_data)

    if user_input_data[PHOTO]:
        update.message.reply_photo(user_input_data[PHOTO].get('file_id'), layout,
                                   reply_markup=inline_keyboard.get_keyboard(), parse_mode=ParseMode.HTML
                                   )
    else:
        update.message.reply_html(text=layout, reply_markup=inline_keyboard.get_keyboard())

    user_input_data['state'] = CONFIRMATION
    return CONFIRMATION


def confirmation_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_input_data = context.user_data
    user = get_user(update.effective_user.id)

    logger.info('user_input_data: %s', user_input_data)

    if data == 'confirm':

        if user['lang'] == LANGS[0]:
            text = 'Tasdiqlandi !'

        if user['lang'] == LANGS[1]:
            text = 'Подтверждено !'

        user_input_data['state'] = 'confirmed'

        reply_keyboard = ReplyKeyboard('menu_keyboard', user['lang'])
        callback_query.message.reply_text(text, reply_markup=reply_keyboard.get_keyboard())

        lastrow_id = insert_cargo(dict(user_input_data))

        if user_input_data['receiver_phone_number']:

            receiver = get_user(phone_number=user_input_data['receiver_phone_number'])

            if receiver:

                if receiver['lang'] == LANGS[0]:
                    text_1 = "Sizga yuk jo'natildi:"
                    text_2 = "Yukni qabul qildim"

                if receiver['lang'] == LANGS[1]:
                    text_1 = 'Вам груз отправлен:'
                    text_2 = 'Я получил груз'

                context.bot.send_message(receiver['user_id'], text_1)

                inline_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text_2, callback_data=f"received_{user['user_id']}_{lastrow_id}")]
                ])

                layout = get_new_cargo_layout(user_input_data, user)
                if user_input_data[PHOTO]:
                    context.bot.send_photo(receiver['user_id'], user_input_data[PHOTO].get('file_id'), layout,
                                           reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
                else:
                    context.bot.send_message(receiver['user_id'], layout, reply_markup=inline_keyboard,
                                             parse_mode=ParseMode.HTML)

        user_input_data.clear()
        return ConversationHandler.END

    if data == 'edit':
        # with open('jsons/callback_query.json', 'w') as cargo:
        #     cargo.write(callback_query.to_json())

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Manzilni tahrirlash', callback_data='edit_address')],
            [InlineKeyboardButton("Yuk ma'lumotlarini tahrirlash", callback_data='edit_cargo_info')],
            [InlineKeyboardButton('Kun va vaqtni tahrirlash', callback_data='edit_date_and_time')],
            [InlineKeyboardButton('« Tahrirni yakunlash', callback_data='terminate_editing')]
        ])

        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        user_input_data['state'] = 'EDIT'
        return 'EDIT'


def message_callback(update: Update, context: CallbackContext):
    print('message_callback')

    user_input_data = context.user_data

    if user_input_data['state'] == 'EDIT':
        print('EDIT STATE')
    if user_input_data['state'] == CONFIRMATION:
        print(f'{CONFIRMATION} STATE')



def message_callback_in_edit(update: Update, context: CallbackContext):
    print('message callback in edit')

    # return ConversationHandler.END


def main():
    conv_1_handler = ConversationHandler(
        entry_points=[CommandHandler('cargo', cargo_callback)],
        states={
            CONFIRMATION: [CallbackQueryHandler(confirmation_callback, pattern='confirm|edit'),
                           MessageHandler(Filters.text & ~Filters.command, message_callback)],
            'EDIT': [edit_conversation_handler,
                     MessageHandler(Filters.text & ~Filters.command | Filters.photo, message_callback_in_edit)]
        },
        fallbacks=[]

    )

    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(conv_1_handler)

    # updater.dispatcher.add_handler(conversation_handler)
    #
    # updater.dispatcher.add_handler(new_cargo_conversation_handler)
    #
    # updater.dispatcher.add_handler(changedataconversation_handler)
    #
    # updater.dispatcher.add_handler(message_handler)
    #
    # updater.dispatcher.add_handler(inline_keyboard_handler)

    # updater.start_polling()
    # updater.idle()

    updater.start_webhook(listen='127.0.0.1', port=5001, url_path=TOKEN)
    updater.bot.set_webhook(url='https://cardel.ml/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
