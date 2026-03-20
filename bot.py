import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = os.getenv("TOKEN")
ADMIN_ID = "1501045648"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# 🔥 Состояния
class Form(StatesGroup):
    choosing_service = State()
    waiting_name = State()

# Главное меню
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Записаться")],
        [KeyboardButton(text="О нас")]
    ],
    resize_keyboard=True
)

# Выбор услуги
service_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Стрижка")],
        [KeyboardButton(text="Заставь меня сиять, дядя")],
        [KeyboardButton(text="Комплекс")],
        [KeyboardButton(text="⬅ Назад")]
    ],
    resize_keyboard=True
)

# Старт
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Добро пожаловать!", reply_markup=main_kb)

# О нас
@dp.message(lambda m: m.text == "О нас")
async def about(message: types.Message):
    await message.answer("Барбершоп анас. Работаем 24/7 💈")

# Записаться
@dp.message(lambda m: m.text == "Записаться")
async def zapis(message: types.Message, state: FSMContext):
    await state.set_state(Form.choosing_service)
    await message.answer("Выберите услугу:", reply_markup=service_kb)

# Назад
@dp.message(lambda m: m.text == "⬅ Назад")
async def back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню", reply_markup=main_kb)

# Выбор услуги
@dp.message(Form.choosing_service)
async def choose_service(message: types.Message, state: FSMContext):
    if message.text not in ["Стрижка", "Заставь меня сиять, дядя", "Комплекс"]:
        await message.answer("Выберите услугу кнопкой 👇")
        return

    await state.update_data(service=message.text)
    await state.set_state(Form.waiting_name)
    await message.answer("Введите ваше имя:")

# Имя
@dp.message(Form.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = message.text

    await message.answer(
        f"✅ Заявка принята!\n\n"
        f"👤 Имя: {name}\n"
        f"💼 Услуга: {data['service']}\n\n"
        f"Мы скоро свяжемся с вами!"
    )

    await bot.send_message(
        ADMIN_ID,
        f"🔥 Новая заявка:\n\n"
        f"👤 Имя: {name}\n"
        f"💼 Услуга: {data['service']}"
    )

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())