
from random import choice as ch
from asyncio import sleep

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery    #  
from aiogram.filters import CommandStart, Command   #  
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.middlewares import TestMiddleware

#texts constant...
from util.textsss import txtsss
from util.bibl_txt_week import week_pr


import app.keyboard as kb
#вместо DefaultBotProperties
router = Router()
router.message.middleware(TestMiddleware())

#создадим класс текстов бибилии
bi_wi = week_pr()


#  Создадим состояния бота
class Reg(StatesGroup):
    name = State()
    number = State()

#  Создадим состояния бота при тестировани 
# 1 - номер вопроса ?? задает бот ??
# 2 - ответ вводит пользователь
# доучить !!!!!!!!!!!!!!!!!!!!!! там где про пицерию
        
        
@router.message(CommandStart())
async def cmd_start(message: Message):
       
    await message.reply(f'Приветствую тебя, дорогой друг, {message.from_user.first_name}',
                        reply_markup=kb.main_action1)
    # await message.answer( - если ловим сообщение /для колбэка -сверху
                        #reply_markup=await kb.inline_cars())
                        #reply_markup=kb.seting)   #инлайн кейборд
                        # или reply_markup=kb.main) маркап кейборд
    

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(""" Это бот-помочник, его цель наладить твою молитвенную жизнь, 
помочь через Слово Божие лучше понять Творца и Его замысел, 
последовательно выбирай предлагаемые темы, читай и выполняй рекомендации. 
    Благословений тебе от Господа ...""")



# @router.message(F.text == 'как дела?')
# async def how_are_you(message: Message):
#     await message.answer('Ok! Very good.')


# # передаю картинку на бот...
# @router.message(F.photo)
# async def get_photo(message: Message):
#     await message.answer(f'ID фото: {message.photo[-1].file_id}')


# #отправка картинки
# @router.message(Command('get_photo'))
# async def get_photo(message: Message):
#     await message.answer_photo(photo='AgACAgIAAxkBAAICUmYMEdSIw-OJ18RHf3xQ9mhtYVqtAAJL1zEbv0RgSP874AFM0S4wAQADAgADeQADNAQ',
#                                caption='Это Я')

 
# обработчик инлайн кнопок меню 2
@router.callback_query(F.data == 'about_action')
async def about(callback: CallbackQuery):
    
    await callback.message.answer(txtsss['about'], show_alert=False)  #выводит всплывающее сообщение из словаря в файле textsss.py
    await sleep(15)                                                    # 15-ти секундная задержка для прочтения сообщения, после меню...
    await callback.message.answer('Выбери опцию и погрузись в чтение, рассуждение, поклонение и молитву...')
    await sleep(3)                                                    # 3х секундная задержка для прочтения сообщения, после меню...
    await callback.message.answer('...', reply_markup=kb.main_action2)
    # можно добавить- , show_alert=True) - тогда придет уведомление как сообщение и будет висеть.
#   await callback.message.answer('Привет!')  # посылает сообщение
#    await callback.message.edit_text('Привет!', reply_markup=await kb.inline_cars())  # посылает сообщение



# обработчик инлайн кнопок меню 2
@router.callback_query(F.data == 'weekly')
async def about(callback: CallbackQuery):
    await callback.message.answer(f'{txtsss['intro_wwek']}', reply_markup=kb.main_action3)
    # можно добавить- , show_alert=True) - тогда придет уведомление как сообщение и будет висеть.
#   await callback.message.answer('Привет!')  # посылает сообщение
#    await callback.message.edit_text('Привет!', reply_markup=await kb.inline_cars())  # посылает сообщение


# обработчик инлайн кнопок меню 3
@router.callback_query(F.data == 'today')
async def about(callback: CallbackQuery):
    await callback.message.answer(f'{bi_wi.get_week_txt(bi_wi.get_week_day())}', reply_markup=kb.main_action3)
    # можно добавить- , show_alert=True) - тогда придет уведомление как сообщение и будет висеть.
#   await callback.message.answer('Привет!')  # посылает сообщение
#    await callback.message.edit_text('Привет!', reply_markup=await kb.inline_cars())  # посылает сообщение


@router.callback_query(F.data == 'all7days')
async def about(callback: CallbackQuery):
    await callback.message.answer('* * *', reply_markup=kb.main_action4)

#вывод кнопки возврата 'retry_main'
@router.callback_query(F.data == 'retry_main')
async def about(callback: CallbackQuery):
    await callback.message.answer('_  *  *  *  _\n', reply_markup=kb.main_action2)

# 6 урок FSM
#
@router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Ввожу имя ')
    await state.update_data(name="Жора")
    await state.set_state(Reg.number)
    await message.answer('Введи номер телефона ')


# @router.message(Reg.name)
# async def reg_two(message: Message, state: FSMContext):
#     await state.update_data(name="Жора")
#     await state.set_state(Reg.number)
#     await message.answer('Введи номер телефона ')


    
@router.message(Reg.number)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f'Спсб, регистрация завершена... \nИмя: {data["name"]}\n Номер: {data["number"]}')
    await state.clear()


#obrabotchik proizvolnogo texta
#@router.message(F.text)
#async def get_answer(message: Message):
#    await message.answer(f'Извини, ты не понят, даю случайный ответ - {ch(listaswer)}')
