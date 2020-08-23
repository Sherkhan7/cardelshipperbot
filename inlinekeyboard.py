from telegram import InlineKeyboardMarkup, InlineKeyboardButton

inlinekeyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("O'zbekcha", callback_data='uzbek'),
    InlineKeyboardButton("Русский", callback_data='russian')
]])
