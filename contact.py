from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardRemove
from DB.main import *


def contact_callback(update: Update, context: CallbackContext):
    with open('update.json', 'w') as update_file:
        update_file.write(update.to_json())

    contact = update.message.contact
    # print(contact.to_json())
    user_data = context.user_data

    user = select(contact.user_id)

    if user:
        if user_data['LANG'] == 'uzbek':
            # context.bot.edit_message_text("Kontaktingiz ma'lumotlar bazasidan topildi",
            #                               update.effective_chat.id, update.effective_message.message_id)

            # update.edited_message_text("Kontaktingiz ma'lumotlar bazasidan topildi")
            update.message.reply_text("Kontaktingiz ma'lumotlar bazasidan topildi", reply_markup=ReplyKeyboardRemove())
        else:
            # context.bot.edit_message_text("Ваш контакт был найден в базе",
            #                               update.effective_chat.id, update.effective_message.message_id)

            # update.edited_message("Ваш контакт был найден в базе")
            update.message.reply_text('Ваш контакт был найден в базе', reply_markup=ReplyKeyboardRemove())
    else:
        insert_user_contact(contact)

        if user_data['LANG'] == 'uzbek':
            update.message.reply_text('Kontaktingiz qabul qilindi', reply_markup=ReplyKeyboardRemove())
        else:
            update.message.reply_text('Ваш контакт был принят', reply_markup=ReplyKeyboardRemove())
