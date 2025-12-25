import os
from data.config import CHANNEL_ID
from aiogram import types
from loader import dp, db, bot
from aiogram.dispatcher.storage import FSMContext
from states.main import mainstate
from handlers.users.functions import generate_accounting_pdf
from keyboards.inline.main import keyboard




@dp.message_handler(text = "💵 Buxgalteriya", state=mainstate.menu)
async def my_account(message: types.Message, state: FSMContext):
    user = await db.select_user(telegram_id = message.from_user.id)
    file_path = f"buxgalteriya_{message.from_user.id}.pdf"
    

    generate_accounting_pdf(user, file_path)

    
    await message.answer_document(
        types.InputFile(file_path),
        caption="📄 Buxgalteriya hisoboti", reply_markup=keyboard
    )


    if os.path.exists(file_path):
        os.remove(file_path)


# Confirm callback
@dp.callback_query_handler(lambda c: c.data == "confirm_send")
async def confirm_send_pdf(callback_query: types.CallbackQuery):
    file_path = f"buxgalteriya_{callback_query.from_user.id}.pdf"

    await bot.send_document(
        chat_id=CHANNEL_ID,
        document=file_path,
        caption="📄 Hisobot"
    )

    # Foydalanuvchini o'chirish, agar kerak bo'lsa
    await db.delete_users(telegram_id=callback_query.from_user.id)

    if os.path.exists(file_path):
        os.remove(file_path)

    await callback_query.message.edit_reply_markup()
    await bot.send_message(callback_query.from_user.id, "✅ Hisobot kanalga yuborildi va hisobingiz o'chirildi.")

# Cancel callback
@dp.callback_query_handler(lambda c: c.data == "cancel_send")
async def cancel_send_pdf(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    await bot.send_message(callback_query.from_user.id, "❌ Hisobot yuborish bekor qilindi.")
