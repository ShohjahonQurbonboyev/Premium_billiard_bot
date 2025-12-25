from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db
from data.config import ADMINS
from keyboards.default.main import main
from aiogram.dispatcher.storage import FSMContext
from states.main import mainstate



@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    user = await db.select_user(telegram_id = message.from_user.id)
    if message.from_user.id == int(ADMINS[0]):
        
        if user is None:
            await db.add_user(
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                telegram_id=message.from_user.id,
                table_price=str(0),
                product_price=str(0),
                all_price=str(0),
                hour_table_night=str(35000),
                hour_table_day=str(35000),
                benefit=0,
                damage=0
                )
            await message.reply("Asosiy menu", reply_markup=main())
            await mainstate.menu.set()
        else:
            await message.reply("Asosiy menu", reply_markup=main())
            await mainstate.menu.set()
    else:
        await message.answer(f"Bu bot xususiy tarzda {user[1]} ga tegishli siz kira olmaysiz !")
        




