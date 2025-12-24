import os
from aiogram import types
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from states.main import mainstate
from handlers.users.functions import generate_accounting_pdf




@dp.message_handler(text = "💵 Buxgalteriya", state=mainstate.menu)
async def my_account(message: types.Message, state: FSMContext):
    user = await db.select_user(telegram_id = message.from_user.id)
    file_path = f"buxgalteriya_{message.from_user.id}.pdf"
    
    # PDF yaratish
    generate_accounting_pdf(user, file_path)

    # PDF yuborish
    await message.answer_document(
        types.InputFile(file_path),
        caption="📄 Buxgalteriya hisoboti"
    )

    # Faylni o'chirish
    if os.path.exists(file_path):
        os.remove(file_path)



    # await message.answer(f"Ism: {user[1]}\nUsername : {user[2]}\n\nTelegram_id: {user[3]}\n\nUmumiy stoldan kelgan foyda : {user[4]} so'm\nUmumiy productdan kelgan foyda : {user[5]} so'm\nUmumiy kirim : {user[6]} so'm\nUmumiy ko'rilgan foyda : {user[9]} so'm\nUmumiy xarajat summasi : {user[10]} so'm\n\nKechki stavka : {user[7]} so'm\nKunduzgi stavka : {user[8]} so'm")
