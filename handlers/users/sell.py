from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from loader import dp, db, bot
from data.config import CHANNEL_ID
from keyboards.default.main import main
from keyboards.inline.main import sell_nakladnoy_keyboard
from aiogram.dispatcher.storage import FSMContext
from states.main import mainstate, sell_product
from handlers.users.functions import calculate_benefit_sell




@dp.message_handler(text="🍔🥃 Product sotish", state=mainstate.menu)
async def choose_table(message: types.Message, state: FSMContext):
    try:
        products = await db.select_all_nakladnoy()

        if not products:
            return await message.answer("📦 Omborda mahsulot yo‘q")

        await state.update_data(sold_products={})

        await message.answer(
            "Mahsulotni tanlang (1 bosish = 1 dona):",
            reply_markup=sell_nakladnoy_keyboard(products)
        )

        await sell_product.sell.set()
    except Exception as ex:
        await message.answer(ex)


@dp.callback_query_handler(lambda c: c.data.startswith("sellprod_"), state=sell_product.sell)
async def add_product_to_sell(call: types.CallbackQuery, state: FSMContext):
    try:

        product_name = call.data.replace("sellprod_", "")
        data = await state.get_data()
        sold_products = data.get("sold_products", {})


        naklad = await db.select_nakladnoy(product_name=product_name)
        if not naklad:
            return await call.answer("❌ Mahsulot topilmadi", show_alert=True)

        available_qty = naklad[2] 
        current_qty_sold = sold_products.get(product_name, 0)


        if current_qty_sold + 1 > available_qty:
            return await call.answer(f"❌ Omborda faqat {available_qty} ta mavjud", show_alert=True)


        sold_products[product_name] = current_qty_sold + 1
        await state.update_data(sold_products=sold_products)


        products = await db.select_all_nakladnoy()
        new_markup = sell_nakladnoy_keyboard(products, sold_products)
    except Exception as ex:
        await call.message.answer(ex)


    try:
        await call.message.edit_reply_markup(reply_markup=new_markup)
    except MessageNotModified:
        pass

    await call.answer(f"➕ {product_name} qo‘shildi")




@dp.callback_query_handler(lambda c: c.data in ["finish_sell", "cancel_sell"], state=sell_product.sell)
async def sell_finish_or_cancel(call: types.CallbackQuery, state: FSMContext):
    try:

        telegram_id = call.from_user.id
        

        if call.data == "cancel_sell":
            await state.finish()
            await call.message.delete()
            await call.message.answer("❌ Sotuv bekor qilindi", reply_markup=main())
            await mainstate.menu.set()
            return


        data = await state.get_data()
        sold_products = data.get("sold_products", {})


        if not sold_products:
            return await call.answer("❌ Hech narsa tanlanmagan", show_alert=True)

        user = await db.select_user(telegram_id=telegram_id)
        nakladnoy = await db.select_all_nakladnoy()
        
        

        old_product_price = int(user[5])
        old_all_price = int(user[6])
        old_benefit = int(user[9])  

        total_sum = 0
        text = "🧾 <b>CHEK</b>\n\n"


        for name, qty in sold_products.items():
            naklad = await db.select_nakladnoy(product_name=name)
            sell_price = int(naklad[4])

            summa = sell_price * qty
            total_sum += summa

            await db.add_product(
                product_name=name,
                table_name="Odam",
                waiting_person="Bar",
                product_number=str(qty),
                product_price=str(summa)
            )

            await db.update_nakladnoy_have(naklad[2] - qty, name)

            text += f"• {name} x{qty} = {summa} so‘m\n"


        benefit = calculate_benefit_sell(sold_products, nakladnoy)


        new_product_price = old_product_price + total_sum
        new_all_price = old_all_price + total_sum
        new_benefit = old_benefit + benefit


        await db.update_user_product(str(new_product_price), telegram_id)
        await db.update_user_all_price(str(new_all_price), telegram_id)
        await db.update_user_benefit(new_benefit, telegram_id)
        

        damage = 0
        for name, qty1 in sold_products.items():
            for product in nakladnoy:
                if product[1] == name:
                    damage += int(product[3]) * int(qty1)

        await db.update_user_damage(damage, telegram_id)

        for name in sold_products.keys():
            await db.delete_product(table_name="Odam", product_name=name)

        text += f"\n💰 <b>JAMI:</b> {total_sum} so‘m"
        text += f"\n📈 <b>FOYDA:</b> {benefit} so‘m"

        await bot.send_message(CHANNEL_ID, text)

        await call.message.delete()
        await call.message.answer("✅ Sotuv yakunlandi", reply_markup=main())
        await mainstate.menu.set()
    except Exception as ex:
        await call.message.answer(ex)
