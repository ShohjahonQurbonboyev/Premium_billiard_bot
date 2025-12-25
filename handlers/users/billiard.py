import asyncio
from aiogram import types
from loader import dp, db
from keyboards.default.main import back_markup
from keyboards.inline.main import confirm
from aiogram.dispatcher.storage import FSMContext
from datetime import datetime
from zoneinfo import ZoneInfo
from states.main import mainstate, process
from handlers.users.functions import now_tashkent,  calculate_play_time





@dp.message_handler(text="🎱 Start stol", state=mainstate.menu)
async def click_billiard(message: types.Message, state: FSMContext):
    await message.answer("Qaysi stolga vaqt ochmoqchisiz?", reply_markup=back_markup)
    await process.table.set()



@dp.message_handler(state=process.table)
async def billiard_number(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        user = await db.select_user(telegram_id=message.from_user.id)

        if not user:
            await message.reply("Sizning akkauntingiz bazada topilmadi!")
            return

        activity_table = await db.select_billiard(table_name=message.text)
        now = now_tashkent().strftime("%Y-%m-%d %H:%M:%S")
        time = datetime.now(ZoneInfo("Asia/Tashkent"))
        hour = time.hour

        if 9 <= hour < 17:
            price = user[8]
        else:
            price = user[7]
        
        if activity_table is None:
            await db.add_billiard(
                table_name=message.text,
                start_time=now,
                finish_time=None,
                other=None,
                price=price,
                telegram_id=message.from_user.id
            )
            await message.reply(f"{message.text} - Stolga vaqt ochildi ✅")
            await message.answer(f"1 soati {price} somdan")
        else:
            await message.answer(f"{message.text} - stol band ❌")
    else:
        await message.reply("Stol raqami bilan ko‘rsating!")





@dp.message_handler(text="👥 Aktiv mijozlar", state=mainstate.menu)
async def my_account(message: types.Message, state: FSMContext):

    now = now_tashkent().strftime("%Y-%m-%d %H:%M:%S")

    active_tables = await db.select_all_billiard()
    sold_products = await db.select_all_products()

    if not active_tables:
        await message.answer("Hozir hech qanday stol band emas ✅")
        return

    for table in active_tables:
        
        minutes, table_price = calculate_play_time(
            table[2],  
            now,
            table[5]  
        )

    
        products_text = ""
        products_total_price = 0

        for prod in sold_products:
            if prod[2] == table[1]: 
                products_text += f"\n• {prod[4]} ta {prod[1]}"
                products_total_price += int(prod[5])


        total_price = int(table_price) + products_total_price

    
        if not products_text:
            products_text = "\n• Mahsulot olinmagan"

        await message.answer(
            f"<b>{table[1]} - Stol band</b>\n\n"
            f"<b>Boshlagan vaqt:</b> {table[2]}\n"
            f"<b>Sotib olingan:</b>{products_text}\n\n"
            f"<b>Hisoblangan vaqt:</b> {int(minutes)} minut\n"
            f"<b>Stol narxi:</b> {int(table_price)} so'm\n"
            f"<b>Mahsulotlar:</b> {products_total_price} so'm\n"
            f"<b>JAMI:</b> {total_price} so'm",
            reply_markup=confirm
        )

        await asyncio.sleep(0.4)



