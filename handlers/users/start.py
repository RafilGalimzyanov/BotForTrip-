from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    '''
    Сохраняем id-шник водителя для обратной связи
    '''
    driver_id = message.from_user.id

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Предложить поездку", callback_data="take_drive", messages="one"))
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f"Здесь ты сможешь набрать попутчиков\n"
                         f"Чтобы отправить поездку, нажмите на кнопку ниже или напишите мне: /trip ", reply_markup=keyboard)