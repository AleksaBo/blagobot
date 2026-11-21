# первый рабочий телеграмбот //aiogram 3.4.1//
# AlekSa_Bo
# 2/04/24
#########################################################################################
########################      попытка сделать бота-молитвенника  ########################
#########################################################################################
#========================================================================================

import asyncio
import logging  #для отладки 
import sys
from _ignn.ttken import ttn


from os import environ as env 
from aiogram import Dispatcher, Bot 
from app.hendlers import router


#обекты botа и диспетчера 
bot = Bot(ttn)#Bot(env.get('BUH_BOT'))
dp = Dispatcher()
 

# запросы к серверу
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
        #logging.basicConfig() #логирование бота
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
   
        asyncio.run(main())
    

 
