from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from loader import dp, db
from keyboards.default.main import main, back_markup, product_del_btns
from keyboards.inline.main import delete_nakladnoy_keyboard
from aiogram.dispatcher.storage import FSMContext
from states.main import mainstate, process, delete_nakladnoy




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
    await message.answer("Product o'chirish tartibini tanlang ?", reply_markup= product_del_btns())
    await delete_nakladnoy.delete_nakladnoy_choose.set()



@dp.message_handler(text="Son bilan olib tashlash", state=delete_nakladnoy.delete_nakladnoy_choose)
async def delete_by_amount_start(message: types.Message, state: FSMContext):
    try:
        products = await db.select_all_nakladnoy()

        if not products:
            await message.answer("📦 Omborda mahsulot yo‘q!")
            return
        await message.answer("Pastdan", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            "Qaysi mahsulotdan olib tashlaysiz?",
            reply_markup=delete_nakladnoy_keyboard(products)
        )

        await delete_nakladnoy.choose_product.set()
    except Exception as ex:
        await message.answer(ex)



@dp.callback_query_handler(
    lambda c: c.data.startswith("deleteprod_"),
    state=delete_nakladnoy.choose_product
)
async def choose_product_for_amount(call: types.CallbackQuery, state: FSMContext):
    product_name = call.data.replace("deleteprod_", "")
    product = await db.select_nakladnoy(product_name=product_name)

    if not product:
        await call.message.answer("Mahsulot topilmadi ❌")
        return

    await state.update_data(product_name=product_name)
    
    await call.message.answer(
        f"📦 {product_name}\n"
        f"Omborda: {product[2]} ta\n\n"
        f"Nechta olib tashlaysiz?"
    )
    await delete_nakladnoy.input_amount.set()


@dp.message_handler(state=delete_nakladnoy.input_amount)
async def remove_amount(message: types.Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer("❗️ Iltimos, son kiriting")
        return

    remove_count = int(message.text)
    data = await state.get_data()
    product_name = data["product_name"]

    product = await db.select_nakladnoy(product_name=product_name)
    have = int(product[2])

    if remove_count > have:
        await message.answer(
            f"❌ Omborda buncha yo‘q!\n"
            f"Mavjud: {have} ta"
        )
        return

    new_have = have - remove_count

    if new_have == 0:
        await db.delete_nakladnoy(product_name)
        await message.answer(
            f"🗑 {product_name} ombordan to‘liq olib tashlandi",
            reply_markup=main()
        )
    else:
        # SENING FUNKSIYANG ISHLATILYAPTI 👇
        await db.update_nakladnoy_have(new_have, product_name)

        await message.answer(
            f"✅ {product_name} dan {remove_count} ta olib tashlandi\n"
            f"📦 Qoldi: {new_have} ta",
            reply_markup=main()
        )

    await mainstate.menu.set()






@dp.message_handler(text="Productni olib tashlash", state=delete_nakladnoy.delete_nakladnoy_choose)
async def delete_product_name(message: types.Message, state: FSMContext):
    try:

        products = await db.select_all_nakladnoy()
        if not products:
            await message.answer("📦 Omborda hech qanday mahsulot yo‘q!")
            return
        await message.answer("Pastdan", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            "O‘chirmoqchi bo‘lgan mahsulotni tanlang:",
            reply_markup= delete_nakladnoy_keyboard(products)
        )
    except Exception as ex:
        await message.answer(ex)

    
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
        await mainstate.menu.set()
    except Exception as ex:
        await call.message.answer(ex)
