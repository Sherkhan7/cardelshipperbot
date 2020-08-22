from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardRemove
from DB.main import *


def contact_callback(update: Update, context: CallbackContext):
    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    contact = update.message.contact
    # print(contact.to_json())

    insert_user_contact(contact)

    user_data = context.user_data

    if user_data['LANG'] == 'uzbek':
        update.message.reply_text('Kontaktingiz qabul qilindi', reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text('Ваш контакт был принят', reply_markup=ReplyKeyboardRemove())
