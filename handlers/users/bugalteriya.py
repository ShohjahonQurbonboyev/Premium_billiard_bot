import os
from data.config import CHANNEL_ID
from aiogram import types
from loader import dp, db, bot
from aiogram.dispatcher.storage import FSMContext
from states.main import mainstate
from handlers.users.functions import generate_accounting_pdf
from keyboards.inline.main import keyboard
import time, os




@dp.message_handler(text = "💵 Buxgalteriya", state=mainstate.menu)
async def my_account(message: types.Message, state: FSMContext):
    try:
        user = await db.select_user(telegram_id = message.from_user.id)
        file_path = f"buxgalteriya.pdf"
        

        generate_accounting_pdf(user, file_path)

        
        await message.answer_document(
            types.InputFile(file_path),
            caption="📄 Buxgalteriya hisoboti", reply_markup=keyboard
        )
    except Exception as ex:
        await message.answer(ex)

  


# Confirm callback
@dp.callback_query_handler(lambda c: c.data == "confirm_send", state="*")
async def confirm_send_pdf(callback_query: types.CallbackQuery):
    try:

        file_path = f"buxgalteriya.pdf"

        await bot.send_document(
            chat_id=CHANNEL_ID,
            document=types.InputFile(file_path),
            caption="Diqqat:\nBu Buxgalteriya hisobotida soliq xarajatlari va boshqa harajatlar xisobga olinmagan."
        )

        await db.delete_users()
        

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except PermissionError:
            time.sleep(0.5)  
            os.remove(file_path)


        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, "✅ Hisobot kanalga yuborildi va hisobingiz o'chirildi.")
    except Exception as ex:
        await callback_query.message.answer(ex)


# Cancel callback
@dp.callback_query_handler(lambda c: c.data == "cancel_send", state="*")
async def cancel_send_pdf(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, "❌ Hisobot yuborish bekor qilindi.")
    except Exception as ex:
        await callback_query.message.answer(ex)