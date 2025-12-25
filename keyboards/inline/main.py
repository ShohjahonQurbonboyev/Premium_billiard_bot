from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types



def nakladnoy_keyboard(products):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for p in products:
        keyboard.insert(
            InlineKeyboardButton(
                text=f"{p[1]} ({p[2]})",
                callback_data=f"addprod_{p[1]}"
            )
        )
    keyboard.add(
        InlineKeyboardButton("❌ Olib tashlash", callback_data="cancel_add")
    )
    return keyboard



confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="confirm"),
            InlineKeyboardButton(text="❌", callback_data="cancel")
        ]
    ]
)

confirm_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="confirm_admin"),
            InlineKeyboardButton(text="❌", callback_data="cancel_admin")
        ]
    ]
)


refresh_markup = InlineKeyboardMarkup().add(
    InlineKeyboardButton("🔄 Yangilash", callback_data="refresh")
).add(
    InlineKeyboardButton("⚙️ Sozlamalar", callback_data="setting")
).add(
    InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_refresh")
)



def delete_nakladnoy_keyboard(products):
    kb = InlineKeyboardMarkup(row_width=2)
    for p in products:
        kb.insert(
            InlineKeyboardButton(
                text=f"{p[1]} ({p[2]} ta)",
                callback_data=f"deleteprod_{p[1]}"
            )
        )
    kb.add(
        InlineKeyboardButton("↩️ Bekor qilish", callback_data="cancel_delete")
    )
    return kb



def sell_nakladnoy_keyboard(products, sold_products=None):
    sold_products = sold_products or {}
    buttons = []

    for p in products:
        name = p[1]  
        available_qty = p[2]  
        sold_qty = sold_products.get(name, 0)
        text = f"{name} ({sold_qty}/{available_qty})"
        buttons.append(types.InlineKeyboardButton(text=text, callback_data=f"sellprod_{name}"))

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)


    keyboard.add(
        types.InlineKeyboardButton(text="✅ Sotish", callback_data="finish_sell"),
        types.InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_sell")
    )

    return keyboard




keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Xisobni yopish ✅", callback_data="confirm_send"),
            InlineKeyboardButton(text="Bekor qilish ❌", callback_data="cancel_send")
        ]
    ]
)
