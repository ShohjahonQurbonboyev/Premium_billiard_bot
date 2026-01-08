from aiogram import types
from loader import dp
from keyboards.default.main import main, back_markup
from states.main import mainstate, process, AddProductFSM, delete_nakladnoy
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(text="🔙 Orqaga", state=process.table)
async def main_menu_redirect(message: types.Message, state: FSMContext):
    await message.answer("Siz asosiy menudasiz 🏠", reply_markup=main())
    await mainstate.menu.set()

@dp.message_handler(text="🔙 Orqaga", state=process.nakladnoy)
async def main_menu_redirect(message: types.Message, state: FSMContext):
    await message.answer("Siz asosiy menudasiz 🏠", reply_markup=main())
    await mainstate.menu.set()

@dp.message_handler(text="🔙 Orqaga", state=process.number_nakladnoy)
async def main_menu_redirect(message: types.Message, state: FSMContext):
    await message.answer("Mahsulot nomini kiriting", reply_markup=back_markup)
    await process.nakladnoy.set()

@dp.message_handler(text="🔙 Orqaga", state=process.nakladnoy_price)
async def main_menu_redirect(message: types.Message, state: FSMContext):
    await message.answer("Nechta keldi ?", reply_markup=back_markup)
    await process.number_nakladnoy.set()


@dp.message_handler(text="🔙 Orqaga", state=process.nakladnoy_sell_price)
async def main_menu_redirect(message: types.Message, state: FSMContext):
    await message.answer("Necha sumdan keldi ?", reply_markup=back_markup)
    await process.nakladnoy_price.set()


@dp.message_handler(text="🔙 Orqaga", state=AddProductFSM.table)
async def main_menu_redirect(message: types.Message, state: FSMContext):
    await message.answer("Siz asosiy menudasiz 🏠", reply_markup=main())
    await mainstate.menu.set()


@dp.message_handler(text="🔙 Orqaga", state=delete_nakladnoy.delete_nakladnoy_choose)
async def main_menu_redirect(message: types.Message, state: FSMContext):
    await message.answer("Siz asosiy menudasiz 🏠", reply_markup=main())
    await mainstate.menu.set()