from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton )

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text= '1'),
     KeyboardButton(text= '2'),
     KeyboardButton(text= '3'),
     KeyboardButton(text= '4'),
     KeyboardButton(text= '5')],
    [KeyboardButton(text= 'Корзина'), 
     KeyboardButton(text= 'Контакты')]
],

                    resize_keyboard=True,                          # кнопки минимального размера
                    input_field_placeholder = '1/2/3/4 или 5?' ,    # подпись над кнопками (в строке сообщений)
                    one_time_keyboard=True                          # исчезающие после нажатия
                    ##???? нет не уходит 
)


seting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='мой insta: ', 
        url='https://www.instagram.com/ales_barych/',)]
])


cars = [
        ['about_action','https://cars.av.by/tesla'],
        ['Mercedes', 'https://www.ixbt.com/news/2023/10/08/mercedes-benz-amg-g-63-187.html'],
        ['Jeely', 'https://ru.made-in-china.com/co_jxtrailer/product_2023-Geely-Xingyue-L-Monjaro-Gas-Powered-Cars-5seats-Jeely-SUV-Price_ysshuuosey.html']
]


async def inline_cars():
    # если нужно реплай keyboard = ReplyKeyboardBuilder()
    keyboard = InlineKeyboardBuilder()
    for car, urla in cars:
        keyboard.add(InlineKeyboardButton(text=car, url=urla,))
    #   keyboard.add(KeyboardButton(text=car))
    return keyboard.adjust(3).as_markup()


main_action1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Недельный молитвенный путеводитель', callback_data='weekly')], 
    [InlineKeyboardButton(text='Молитвенный ежедневник (на 3 месяца)', callback_data='everyday')],
    [InlineKeyboardButton(text='Библейский ежедневника(места для чтения))', callback_data='readbible')],
    [InlineKeyboardButton(text='Благословения', callback_data='blessings')],
    [InlineKeyboardButton(text='Чем полезен Worship&PrayerBot', callback_data='about_action')],            # идем на строку - 68 hendlers.py
    [InlineKeyboardButton(text='help', callback_data='help')],
])

# , callback_data='about_action'


main_action2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Недельный молитвенный путеводитель', callback_data='weekly')], 
    [InlineKeyboardButton(text='Молитвенный ежедневник (на 3 месяца)', callback_data='everyday')],
    [InlineKeyboardButton(text='Библейский ежедневника(места для чтения))', callback_data='readbible')],
    [InlineKeyboardButton(text='Благословения', callback_data='blessings')]
])


main_action3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Стихи для сегодняшней молитвы', callback_data='today')], 
    [InlineKeyboardButton(text='Посмотреть другие дни', callback_data='all7days')],
    [InlineKeyboardButton(text='в главное меню', callback_data='retry_main')]
])


main_action4 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='1', callback_data='day_1'), 
        InlineKeyboardButton(text='2', callback_data='day_2'),
        InlineKeyboardButton(text='3', callback_data='day_3')],
    
        [InlineKeyboardButton(text='4', callback_data='day_4'),
        InlineKeyboardButton(text='5', callback_data='day_5'),
        InlineKeyboardButton(text='6', callback_data='day_6')],
        [InlineKeyboardButton(text='7', callback_data='day_7')]
    
])



# ret_main, кнопка вызова меню - main_action2
retry_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='в главное меню', callback_data='retry_main')]
])
