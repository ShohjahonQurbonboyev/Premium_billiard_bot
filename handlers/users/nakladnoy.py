from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from loader import dp, db
from keyboards.default.main import main, back_markup
from keyboards.inline.main import delete_nakladnoy_keyboard
from aiogram.dispatcher.storage import FSMContext
from states.main import mainstate, process




@dp.message_handler(text = "➕ Nakladnoyga Qo'shish", state=mainstate.menu)
async def my_account(message: types.Message, state: FSMContext):
    await message.answer("Mahsulot nomini kiriting", reply_markup=back_markup)
    await process.nakladnoy.set()



@dp.message_handler(state=process.nakladnoy)
async def my_account(message: types.Message, state: FSMContext):
    try:

        name = message.text
        products = await db.select_nakladnoy(product_name=name)
        if products is None:
            await  state.update_data(data={"product_name" : name})
            await message.answer(f"Nechta {name} olib kelindi ?", reply_markup=back_markup)
            await process.number_nakladnoy.set()
        else:
            await  state.update_data(data={"product_name" : name})
            await message.answer(f"Nechta olib kelindi ?", reply_markup=back_markup)
            await process.number_nakladnoy.set()
    except Exception as ex:
        await message.answer(ex)



@dp.message_handler(state=process.number_nakladnoy)
async def my_account(message: types.Message, state: FSMContext):
    try:

        old_damage = await db.select_user(telegram_id=message.from_user.id)
        number = message.text
        if number.isnumeric():
            data = await state.get_data()
            name =  data.get("product_name")
            products = await db.select_nakladnoy(product_name=name)
            if products is None:
                await  state.update_data(data={"have_product" : number})
                await message.answer(f"{name} necha sumdan  keldi ?", reply_markup=back_markup)
                await process.nakladnoy_price.set()
            else:
                
                
                new_number_nakladnoy = int(products[2]) + int(number)
                damage_price = int(number) * int(products[3])
                new_damage = int(old_damage[10]) + int(damage_price)

                await db.update_user_damage(new_damage, message.from_user.id)
                await db.update_nakladnoy_have(new_number_nakladnoy, name)
                await message.reply(f"{name} {new_number_nakladnoy} ta bo'ldi ✅", reply_markup=main())
                await mainstate.menu.set()
        else:
            await message.answer("Mahsulot nechta ekanini son bilan korsating !", reply_markup=back_markup)
    except Exception as ex:
        await message.answer(ex)

    

@dp.message_handler(state=process.nakladnoy_price)
async def my_account(message: types.Message, state: FSMContext):
    try:
        number = message.text
        if number.isnumeric():
            await  state.update_data(data={"original_price" : number})
            await message.answer("necha sumdan sotiladi ?", reply_markup=back_markup)
            await  process.nakladnoy_sell_price.set()
        else:
            await message.answer("Mahsulot necha sum ekanini son bilan korsating !", reply_markup=back_markup)
    except Exception as ex:
        await message.answer(ex)

    

@dp.message_handler(state=process.nakladnoy_sell_price)
async def my_account(message: types.Message, state: FSMContext):
    try:

        number = message.text
        if number.isnumeric():
            data = await state.get_data()
            name_product = data.get("product_name")
            product_have = data.get("have_product")
            price_original = data.get("original_price")
            await db.add_nakladnoy(
                product_name=name_product,
                have_product=int(product_have),
                original_price=int(price_original),
                sell_price=int(number)
            )

            await message.answer("Mahsulot bazaga saqlandi ✅", reply_markup=main())
            await mainstate.menu.set()
        else:
            await message.answer("Mahsulot necha sum ekanini son bilan korsating !", reply_markup=back_markup)
    except Exception as ex:
        await message.answer(ex)




@dp.message_handler(text="➖ Product O'chirish", state=mainstate.menu)
async def delete_product_start(message: types.Message, state: FSMContext):
    products = await db.select_all_nakladnoy()
    if not products:
        await message.answer("📦 Omborda hech qanday mahsulot yo‘q!")
        return
    await message.answer("Pastdan", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "O‘chirmoqchi bo‘lgan mahsulotni tanlang:",
        reply_markup= delete_nakladnoy_keyboard(products)
    )

    
@dp.callback_query_handler(lambda c: c.data.startswith("deleteprod_") or c.data=="cancel_delete", state="*")
async def delete_product_callback(call: types.CallbackQuery):
    try:
        if call.data == "cancel_delete":
            await call.message.delete()
            await call.message.answer("Bekor qilindi ❌", reply_markup=main())
            await mainstate.menu.set()
            return

        product_name = call.data.replace("deleteprod_", "")
        await db.delete_nakladnoy(product_name)
        await call.message.answer(f"{product_name} o‘chirildi ❌", reply_markup=main())
        await call.message.edit_text(f"{product_name} ombordan o‘chirildi ❌")
    except Exception as ex:
        await call.message.answer(ex)
