from telegram import InlineKeyboardMarkup, InlineKeyboardButton

lang_inlinekeyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("O'zbekcha", callback_data='uz'),
    InlineKeyboardButton("Русский", callback_data='ru')
]])