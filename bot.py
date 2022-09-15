#!venv/bin/python
import logging
from aiogram import Bot, Dispatcher, executor, types
from auth_data import token
from aiogram.dispatcher.filters import Text

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
name_of_file = "test1"


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Получить таблицу")
    keyboard.add(button_1)


@dp.message_handler(Text(equals="Получить таблицу"))
async def cmd_answer(message: types.Message):
    await message.answer_document(open(name_of_file + ".xlsx", 'rb'))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
