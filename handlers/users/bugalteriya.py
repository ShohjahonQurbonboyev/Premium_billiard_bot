import os
import time
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loader import dp, db, bot
from data.config import CHANNEL_ID
from states.main import mainstate
from handlers.users.functions import generate_accounting_pdf
from keyboards.inline.main import keyboard

PDF_DIR = "pdf_reports"

# Papka mavjud bo‘lmasa yaratamiz
os.makedirs(PDF_DIR, exist_ok=True)


@dp.message_handler(text="💵 Buxgalteriya", state=mainstate.menu)
async def my_account(message: types.Message, state: FSMContext):
    try:
        user = await db.select_user(telegram_id=message.from_user.id)

        file_path = os.path.join(PDF_DIR, "buxgalteriya.pdf")

        generate_accounting_pdf(user, file_path)

        await message.answer_document(
            types.InputFile(file_path),
            caption="📄 Buxgalteriya hisoboti",
            reply_markup=keyboard
        )

    except Exception as ex:
        await message.answer(f"Xatolik: {ex}")


@dp.callback_query_handler(lambda c: c.data == "confirm_send", state="*")
async def confirm_send_pdf(callback_query: types.CallbackQuery):
    try:
        file_path = os.path.join(PDF_DIR, "buxgalteriya.pdf")

        await bot.send_document(
            chat_id=CHANNEL_ID,
            document=types.InputFile(file_path),
            caption=(
                "⚠️ Diqqat:\n"
                "Bu buxgalteriya hisobotida soliq va boshqa xarajatlar hisobga olinmagan."
            )
        )

        await db.delete_users()

        
        for file in os.listdir(PDF_DIR):
            if file.endswith(".pdf"):
                try:
                    os.remove(os.path.join(PDF_DIR, file))
                except PermissionError:
                    time.sleep(0.5)
                    os.remove(os.path.join(PDF_DIR, file))

        await callback_query.message.delete()
        await bot.send_message(
            callback_query.from_user.id,
            "✅ Hisobot kanalga yuborildi va barcha PDF fayllar o‘chirildi."
        )

    except Exception as ex:
        await callback_query.message.answer(f"Xatolik: {ex}")


@dp.callback_query_handler(lambda c: c.data == "cancel_send", state="*")
async def cancel_send_pdf(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.delete()
        await bot.send_message(
            callback_query.from_user.id,
            "❌ Hisobot yuborish bekor qilindi."
        )
    except Exception as ex:
        await callback_query.message.answer(f"Xatolik: {ex}")
