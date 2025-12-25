from aiogram import types
from loader import dp, db, bot
from data.config import CHANNEL_ID
from aiogram.dispatcher.storage import FSMContext
from handlers.users.functions import now_tashkent,  calculate_play_time, calculate_benefit, calculate_damage_for_add




@dp.callback_query_handler(lambda c: c.data in ['confirm', 'cancel'], state="*")
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    telegram_id = callback_query.from_user.id

    if callback_query.data == "confirm":

        lines = callback_query.message.text.splitlines()
        table_number = lines[0].split(" ")[0]  

        
        table = await db.select_billiard(table_name=table_number)
        user = await db.select_user(telegram_id=telegram_id)
        nakladnoy = await db.select_all_nakladnoy()

        if not table or not user:
            await callback_query.answer("Bu xizmat allaqachon yopilgan", show_alert=True)
            return

        
        playing_minutes, table_cost = calculate_play_time(
            table[2],
            now_tashkent().strftime("%Y-%m-%d %H:%M:%S"),
            table[5]
        )
        table_cost = int(table_cost)


        products = await db.select_products_by_table(table_number)
        product_cost = sum(int(p[5]) for p in products) if products else 0

        benefit = calculate_benefit(products, nakladnoy)

        old_table_price = int(user[4])
        old_product_price = int(user[5])
        old_all_price = int(user[6])
        old_benefit =  user[9]


        new_table_price = old_table_price + table_cost
        new_product_price = old_product_price + product_cost
        new_all_price = old_all_price + table_cost + product_cost
        new_benefit = old_benefit + table_cost + benefit


        await db.update_user_table(str(new_table_price), telegram_id)
        await db.update_user_product(str(new_product_price), telegram_id)
        await db.update_user_all_price(str(new_all_price), telegram_id)
        await db.update_user_benefit(new_benefit, telegram_id)


        damage = 0

        for p in products:
            product_name = p[1] 
            qty = int(p[4])        
            damage += await calculate_damage_for_add(product_name, qty)


        user = await db.select_user(telegram_id=telegram_id)
        old_damage = int(user[10]) if user[10] else 0  
        new_damage = int(old_damage) + int(damage)
        await db.update_user_damage(new_damage, telegram_id)



    
        await db.delete_billiard(table_number, telegram_id)
        for p in products:
            await db.delete_product(table_number, p[1])


        txt = f"✅ Hisob yopildi\n"f"💵 Stol: {table_cost} so‘m\n"f"🕒 Xisoblangan vaqt: {int(playing_minutes)} min\n"f"🛒 Product: {product_cost} so‘m\n"f"📈 Productdan ko'rilgan foyda : {benefit} so'm\n"f"💰 Jami: {table_cost + product_cost} so‘m"
        await callback_query.answer(txt, show_alert=True)
        await bot.send_message(chat_id=CHANNEL_ID, text=txt)
        await callback_query.message.delete()

    else:
        await callback_query.message.delete()
        await callback_query.answer("Bekor qilindi ❌")
