from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup
import os

load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot)

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add('Каталог').add('Корзина').add('Контакты')

main_admin_keyboard = main_keyboard
main_admin_keyboard.add('Админка')

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add('Add object').add("Delete object").add('Create spam')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer_sticker("CAACAgIAAxkBAAMLZOj8IVIdiKT7X70EwpHNpJeDHisAAggfAAI_e3BIMYkv6waWJLswBA")
    await message.answer(f'{message.from_user.first_name}, hello!', reply_markup=main_keyboard)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Вы админ, кароче", reply_markup=main_admin_keyboard)


@dp.message_handler(text='Контакты')
async def cmd_start(message: types.Message):
    await message.answer("Писать ему: @Dusheskas")


@dp.message_handler(text='Корзина')
async def cmd_start(message: types.Message):
    await message.answer("Корзина пуста")


@dp.message_handler(text='Каталог')
async def cmd_start(message: types.Message):
    await message.answer("Каталог пуст")


@dp.message_handler(text='Админка')
async def cmd_start(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Hello, admin", reply_markup=admin_keyboard)
    else:
        await message.reply("I don't understand")

@dp.message_handler(content_types=['sticker'])
async def check_sticker(message: types.Message):
    await message.answer(message.sticker.file_id)
    await bot.send_message(message.from_user.id, message.chat.id)


@dp.message_handler(content_types=['document', 'photo'])
async def forward_message(message: types.Message):
    await bot.forward_message(os.getenv("GROUP_ID"), message.from_user.id, message.message_id)


@dp.message_handler()
async def cmd_start(message: types.Message):
    await message.reply("I don't understand")


if __name__ == '__main__':
    executor.start_polling(dp)
