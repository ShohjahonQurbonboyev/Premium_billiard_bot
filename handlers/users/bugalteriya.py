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
    

    generate_accounting_pdf(user, file_path)

    
    await message.answer_document(
        types.InputFile(file_path),
        caption="📄 Buxgalteriya hisoboti"
    )


    if os.path.exists(file_path):
        os.remove(file_path)
