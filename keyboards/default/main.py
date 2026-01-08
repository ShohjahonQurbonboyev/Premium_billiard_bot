from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

back_btn = "🔙 Orqaga"
back_markup = ReplyKeyboardMarkup(resize_keyboard=True)
back_markup.add(back_btn)


def main():
    buttons = [
        "🎱 Start stol",
        "🍔 Stolga mahsulot qo'shish",
        "👥 Aktiv mijozlar",
        "💵 Buxgalteriya",
        "➖ Product O'chirish",
        "➕ Nakladnoyga Qo'shish",
        "🍔🥃 Product sotish"
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for button in buttons:
        markup.insert(KeyboardButton(button))  

    return markup

    

def product():
    buttons = ["Stol", "Ojidaniya"]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for button in buttons:
        markup.insert(KeyboardButton(button))
    markup.add(KeyboardButton(back_btn))

    return markup
    


def product_del_btns():
    buttons = ["Productni olib tashlash", "Son bilan olib tashlash"]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        markup.insert(KeyboardButton(button))
    markup.add(KeyboardButton(back_btn))
    
    return markup