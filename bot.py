import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7969209526:AAFCw18wdsESozuN7NXvoS85dlF5cj3_fwI"
ADMIN_ID = "1501045648"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Записаться")],
        [KeyboardButton(text="ℹ️ О нас")]
    ],
    resize_keyboard=True
)

# Выбор услуги
service_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✂️ Стрижка")],
        [KeyboardButton(text="🧔 Бритье")],
        [KeyboardButton(text="💇 Комплекс")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

# Хранилище (временно)
user_data = {}

# Старт
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Добро пожаловать! 👋", reply_markup=main_kb)

# О нас
@dp.message(lambda m: m.text == "ℹ️ О нас")
async def about(message: types.Message):
    await message.answer("Мы барбершоп. Работаем 24/7 💈")

# Записаться
@dp.message(lambda m: m.text == "📅 Записаться")
async def zapis(message: types.Message):
    await message.answer("Выберите услугу:", reply_markup=service_kb)

# Выбор услуги
@dp.message(lambda m: m.text in ["✂️ Стрижка", "🧔 Бритье", "💇 Комплекс"])
async def choose_service(message: types.Message):
    user_data[message.from_user.id] = {"service": message.text}
    await message.answer("Введите ваше имя:")

# Назад
@dp.message(lambda m: m.text == "⬅️ Назад")
async def back(message: types.Message):
    await message.answer("Главное меню", reply_markup=main_kb)

# Имя
@dp.message()
async def get_name(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        await message.answer("Нажмите 'Записаться' сначала")
        return

    user_data[user_id]["name"] = message.text

    data = user_data[user_id]

    # Ответ клиенту
    await message.answer(
        f"✅ Заявка принята!\n\n"
        f"👤 Имя: {data['name']}\n"
        f"💼 Услуга: {data['service']}\n\n"
        f"Мы скоро свяжемся с вами!"
    )

    # Отправка админу
    await bot.send_message(
        ADMIN_ID,
        f"🔥 Новая заявка:\n\n"
        f"👤 Имя: {data['name']}\n"
        f"💼 Услуга: {data['service']}"
    )

    # очистка
    user_data.pop(user_id)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())