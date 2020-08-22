import importlib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


class Lang(object):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        """
            args is tuple of Update and CallbackContext objects
            (Update, CallbackContext)
        """
        self.__update = args[0]
        self.__callback_context = args[1]

        self.__do_command()

    def create_file(self, filename, data):
        with open(filename, 'w') as file:
            file.write(data)

    def __do_command(self):
        update = self.__update
        context = self.__callback_context

        self.create_file('update.json', update.to_json())
        command = update.message.text

        if command == '/start':
            inline_keyboard_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton("\U0001F1FF O'zbekcha", callback_data='uzbek'),
                InlineKeyboardButton("\U0001F1FA Русский", callback_data='russian')
            ]])
            update.message.reply_text('Tilni tanlang. Выберите язык.',
                                      reply_markup=inline_keyboard_markup)

# def keyboard_callback_handler(update: Update, context: CallbackContext):
#     callback_query = update.callback_query
#     data = callback_query.data
#     user_data = context.user_data
#     user_data['LANG'] = data
#     logger.info('user_data: %s', user_data)
#
#     with open('update.json', 'w') as update_file:
#         update_file.write(update.to_json())
#
#     with open('callback_query.json', 'w') as callback_query_file:
#         callback_query_file.write(callback_query.to_json())
#
#     if data == 'uzbek':
#         reply_keyboard_markup = ReplyKeyboardMarkup([[
#             KeyboardButton("\U0001F464 Kontaktimni yuborish", request_contact=True)
#         ]], resize_keyboard=True)
#
#         # callback_query.edit_message_reply_markup(InlineKeyboardMarkup([[InlineKeyboardButton('test', callback_data='test_data')]]))
#
#         callback_query.edit_message_text(f'\U0001F44B Salom, {update.effective_user.first_name}\n'
#                                          f'Davom etish uchun menga kontaktingizni yuboring \U0001F60A',)
#
#         callback_query.message.reply_text(reply_markup=reply_keyboard_markup)
#
#     else:
#         reply_keyboard_markup = ReplyKeyboardMarkup([[
#             KeyboardButton("\U0001F464 Отправить мой контакт", request_contact=True)
#         ]], resize_keyboard=True)
#
#         callback_query.message.reply_text(f'\U0001F44B  Привет, {update.effective_user.first_name}\n'
#                                           f'Чтобы продолжить, отправьте мне свой контакт \U0001F60A',
#                                           reply_markup=reply_keyboard_markup)


# def contact_callback(update: Update, context: CallbackContext):
#     with open('update.json', 'w') as update_file:
#         update_file.write(update.to_json())
#
#     # with open('update.json', 'w') as update_file:
#     #     update_file.write(update.message.contact)
#
#     user_data = context.user_data
#
#     if user_data['LANG'] == 'uzbek':
#         update.message.reply_text('Kontaktingiz qabul qilindi', reply_markup=ReplyKeyboardRemove())
#     else:
#         update.message.reply_text('Ваш контакт был принят', reply_markup=ReplyKeyboardRemove())
