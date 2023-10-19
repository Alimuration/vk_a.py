import requests
import vk_api
from vk_api.utils import get_random_id

session = requests.Session()
vk = vk_api.VkApi(login='login', password='password', app_id=2685278)
vk.auth()
try:
    vk.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

from vk_api.longpoll import VkLongPoll, VkEventType


longpoll = VkLongPoll(vk)
vk = vk.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        # Слушаем longpoll, если пришло сообщение то:
        if event.text == 'Да' or event.text == 'да':  # Если написали заданную фразу
            if event.from_user:  # Если написали в ЛС
                vk.messages.send(  # Отправляем сообщение
                    user_id=event.user_id,
                    message='нет (от бота)',
                    random_id=get_random_id()
                )
            elif event.from_chat: # Если написали в Беседе
                vk.messages.send(  # Отправляем собщение
                    chat_id=event.chat_id,
                    message='NO'
            )
