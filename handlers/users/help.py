from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Я понимаю следующие команды:",
            "/start - Начать диалог\n",
            "/help - Получить справку\n",
            "/trip - предложить поездку")

    await message.answer("\n".join(text))