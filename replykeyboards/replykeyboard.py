from telegram import ReplyKeyboardMarkup, KeyboardButton

replykeyboard_uz = ReplyKeyboardMarkup([[
    KeyboardButton("\U0001F464 Kontaktimni yuborish", request_contact=True)
]], resize_keyboard=True)

replykeyboard_ru = ReplyKeyboardMarkup([[
    KeyboardButton("\U0001F464 Отправить мой контакт", request_contact=True)
]], resize_keyboard=True)