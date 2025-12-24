from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from loader import dp, db
from keyboards.default.main import main, back_markup
from keyboards.inline.main import nakladnoy_keyboard
from aiogram.dispatcher.storage import FSMContext
from states.main import mainstate, AddProductFSM



@dp.message_handler(text="🍔 Stolga mahsulot qo'shish", state=mainstate.menu)
async def choose_table(message: types.Message, state: FSMContext):
    await message.answer("🪑 Stol raqamini yuboring:",reply_markup=ReplyKeyboardRemove() and back_markup)
    await AddProductFSM.table.set()




@dp.message_handler(state=AddProductFSM.table)
async def show_products(message: types.Message, state: FSMContext):
    if not message.text.isnumeric():
        return await message.reply("❌ Stol raqamini kiriting")

    await state.update_data(table=message.text)

    products = await db.select_all_nakladnoy()
    if not products:
        return await message.answer("📦 Nakladnoy bo‘sh", reply_markup= back_markup)
    
    table = await db.select_billiard(table_name= message.text)
    if table is None:
        return await message.answer(f"{message.text} - stol bo'sh", reply_markup=back_markup)

    await message.answer("Mahsulotlarni qoshish uchun", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "🛒 Mahsulotni tanlang (har bosish = 1 dona):",
        reply_markup=nakladnoy_keyboard(products)
    )




@dp.callback_query_handler(lambda c: c.data.startswith("addprod_") or c.data == "cancel_add", state=AddProductFSM.table)
async def add_or_cancel_callback(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    if call.data == "cancel_add":
        try:
            await call.message.delete()
            await call.message.answer("mahsulot stoli olib tashlandi",reply_markup=main())
            await mainstate.menu.set()
        except Exception as e:
            print(f"Xatolik: {e}")
        await call.answer("Bekor qilindi ❌")
        return

    # Mahsulot qo'shish
    product_name = call.data.replace("addprod_", "")
    data = await state.get_data()
    table = data["table"]

    naklad = await db.select_nakladnoy(product_name=product_name)
    if not naklad or naklad[2] <= 0:
        return await call.answer("❌ Mahsulot tugagan", show_alert=True)

    sell_price = naklad[4]

    product = await db.select_product(
        table_name=table,
        product_name=product_name
    )

    # 🟩 Agar stolga hali qo'shilmagan bo'lsa
    if product is None:
        await db.add_product(
            product_name=product_name,
            table_name=table,
            waiting_person=None,
            product_number="1",
            product_price=str(sell_price)
        )
    else:
        await db.update_product_number(str(int(product[4]) + 1), product[0])
        await db.update_product_price(str(int(product[5]) + sell_price), product[0])
    


    # 🟥 Nakladnoydan kamaytirish
    await db.update_nakladnoy_have(naklad[2] - 1, product_name)

    await call.answer(f"➕ {product_name} qo‘shildi")
