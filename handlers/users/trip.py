from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import callback_data
from aiogram.utils.markdown import hlink

from loader import dp, bot
from states.trip import Trip

@dp.callback_query_handler(text="take_drive", state=None)
async def go_ord(message: types.Message):
    driver_id = message.from_user.id
    await bot.send_message(chat_id=driver_id,text="Регистрируем вашу поездку. \n "
                                             "Напишите маршрут. \n Например: Из Арска в Казань")
    await Trip.Q1.set()

@dp.message_handler(Command("trip"), state=None)
async def enter_trip(message: types.Message):
    await message.answer("Регистрируем вашу поездку. \n\n"
                         "Напишите маршрут. \n Например: Из Арска в Казань")
    await Trip.Q1.set()

@dp.message_handler(state=Trip.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer1 = message.text
    message_id = message.message_id
    await state.update_data({"answer_date": answer1})
    await state.update_data({"message_id": message_id})
    await message.answer("Напишите дату и время поездки \n"
                         "Например: 11.04.2021 в 08:00")
    await Trip.next()

@dp.message_handler(state=Trip.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer_time = message.text
    await state.update_data({"answer_time": answer_time})
    #Достаем
    data = await state.get_data()
    answer_date = data.get("answer_date")
    await message.answer(f'Маршрут: {answer_date}\n' 
                         f'Время и дата: {answer_time}\n'
                         f'Всё верно?')
    await Trip.next()

@dp.message_handler(state=Trip.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    if (answer in "Да" or answer in "да" or answer in "Все" or answer in "все"):
        await message.answer("Ваша поездка зарегистрирована.\n "
                             "<b>Опубликовать в беседе?</b> \n")
        await Trip.next()
    else:
        await message.answer("В таком случае пройдите процедуру регистрации с начала :) \n")
        await state.finish()


@dp.message_handler(state=Trip.Q4)
async def answer_q4(message: types.Message, state: FSMContext):
    name_client = message.from_user.full_name
    data = await state.get_data()
    answer_date = data.get("answer_date")
    answer_time = data.get("answer_time")
    message_id = data.get("message_id")
    user_id = int(message.from_user.id)
    click = hlink('Откликнуться', f'tg://user?id={user_id}')

    await bot.send_message(-1001138699096,
                           f'<b>ПОЕЗДКА</b>\n'
                           f'Водитель: {name_client}\n'
                           f'Маршрут: {answer_date}\n'
                           f'Время отправления: {answer_time}\n'
                           f'{click}')
    await message.answer("Ваша поездка успешно опубликована.")
    await state.finish()