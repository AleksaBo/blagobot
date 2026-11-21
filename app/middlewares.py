from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable 


class TestMiddleware(BaseMiddleware):
    async def __call__(self,
                        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                        event: TelegramObject,
                        data: Dict[str, Any]):
                       
        ##print('Действия обработчика после события и до фильтра!!!')
        result = await handler(event, data)
        #print(data['event_from_user'])
        print(f'Действия обработчика после фильтра перед выходом из события\
              \n ===============================') #после-\n {event.}\n
        return result

