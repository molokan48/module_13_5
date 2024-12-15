from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ""
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())
kb = ReplyKeyboardMarkup()
but_1 = KeyboardButton(text= "Информация")
but_2 = KeyboardButton(text= 'Рассчитать')
kb.row(but_1, but_2)
kb.resize_keyboard = True

class UserState(StatesGroup):

    age = State()
    growth = State()
    weight = State()

def is_number(val):
    try:
        float(val)
        return True
    except ValueError:
        return False

@dp.message_handler(text = "Информация")
async def information(message):
    await message.answer('Мне пока нечего рассказать о себе, возможно я создан передавать масло')


@dp.message_handler(text = "Рассчитать")
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth= message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight= message.text)
    data = await state.get_data()
    err = False

    if not is_number(data['weight']):
        await message.answer(f"{data['weight']}  не похоже на цифры, и как это посчитать???")
        err = True
        # await state.finish()
    if not is_number(data['age']):
        await message.answer(f"{data['age']}  не похоже на цифры, и как это посчитать???")
        err = True
        # await state.finish()
    if not is_number(data['growth']):
        await message.answer(f"{data['growth']}  не похоже на цифры, и как это посчитать???")
        err = True
        # await state.finish()
    if err:
        await state.finish()
        await message.answer("Попробуем еще раз??? " , reply_markup= kb)
    else:
        x_for_send = (float(data['weight'])*10) + (float(data['growth'])*6.25) - (float(data['age'])*5) - 5
        await message.answer(f'Ваша норма калорий {x_for_send}')
        await state.finish()
        await message.answer("Введите команду /start, чтобы начать общение.")

@dp.message_handler(commands= ['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup= kb)

@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates= True)