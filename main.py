import asyncio
from aiogram import Bot, Router, F, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (Message, FSInputFile, KeyboardButton,
                           ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
from config import TOKEN
from keyboards import create_keyboard, create_keyboard_inline
from core.service.database import korzinka_btn, korzinka_retrieve

bot = Bot(TOKEN)
rr = Router()
dp = Dispatcher()


class Register(StatesGroup):
    main_menu = State()


@rr.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await state.set_state(Register.main_menu)
    text_info = korzinka_retrieve()
    text, image_path = text_info[0][1], text_info[0][2]
    photo = FSInputFile(path='greeting.jpg')
    btn_info = korzinka_btn()
    keyboard = create_keyboard(btn_info)
    await message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)


@rr.message(F.text == korzinka_btn()[1][1])
async def aboutUs(message: Message, state: FSMContext):
    info = korzinka_retrieve()
    inline_keyboard = create_keyboard_inline(info[0])
    text = info[0][1]
    await message.answer(text, reply_markup=inline_keyboard)


@rr.message(F.text == korzinka_btn()[4][1])
async def vacancy(message: Message, state: FSMContext):
    info = korzinka_retrieve()
    inline_keyboard = create_keyboard_inline(info[0])
    text = info[0][1]
    await message.answer(text, reply_markup=inline_keyboard)


#
# async def check_start_buttons(message:Message):
#     user_id = message.from_user.id
#     data[user_id]['state'] = ''
#     print(2,data)
#     print(message.text)
#
#     if message.text == 'Biz haqimizda':
#         del data[user_id]['state']
#         button = [
#             [InlineKeyboardButton(text="Sayt", callback_data="sayt", url="https://rabota.korzinka.uz/")]
#         ]
#         keyboard = InlineKeyboardMarkup(inline_keyboard=button)
#         await message.answer("Biz o‘zimiz uchun eng qiziqarli missiyani tanladik - odatiy xarid sayohatini yanada yoqimli va hayajonli narsaga aylantirish.", reply_markup=keyboard)
#     elif message.text == "🔥Yangi do'konlar" or message.text == 'orqaga':
#         data[user_id]['state'] = 'new_shops'
#         print(message.text)
#         buttons = []
#         for i in addresses:
#             buttons.append([KeyboardButton(text=i)])
#         button = [KeyboardButton(text='Bosh menu'), KeyboardButton(text='orqaga')]
#         buttons.append(button)
#         keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
#         await message.answer("Keling, anketagizni yaratamiz.")
#         await message.answer("Ishlamoqchi bo'lgan do'kon/bo'limni tanlang", reply_markup=keyboard)
#
#     elif message.text == "Bo'sh ish o'rinlari":
#         pass
#
#     elif message.text == "Til 🇺🇿/🇷🇺":
#         data[user_id]['state'] = 'lang'
#         pass
#
# async def check_new_shops(message:Message):
#     user_id = message.from_user.id
#     address = message.text
#     data[user_id]['state'] = 'vacancy'
#     print(3, data)
#     if address in addresses:
#         adr = addresses[address]['address']
#         lat = addresses[address]['lat']
#         long = addresses[address]['long']
#         vacancies = addresses[address]['vacancy']
#         buttons = []
#         for i in vacancies:
#             button = [KeyboardButton(text=i)]
#             buttons.append(button)
#         button = [KeyboardButton(text='Bosh menu'), KeyboardButton(text='orqaga')]
#         buttons.append(button)
#         keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
#         await message.answer(adr)
#         await bot.send_location(user_id, lat, long)
#         await message.answer("Qaysi lavozimda ishlamoqchisiz?", reply_markup=keyboard)

dp.include_router(rr)


async def main():
    await dp.start_polling(bot)


print('The bot is working...')
asyncio.run(main())
