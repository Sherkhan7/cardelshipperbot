from telegram import ReplyKeyboardMarkup, KeyboardButton

replykeyboard = ReplyKeyboardMarkup([[
    KeyboardButton("\U0001F464 Kontaktimni yuborish", request_contact=True)
]], resize_keyboard=True)

replykeyboard_russ = ReplyKeyboardMarkup([[
    KeyboardButton("\U0001F464 Отправить мой контакт", request_contact=True)
]], resize_keyboard=True)
