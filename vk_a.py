import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from random import choice

session = requests.Session()


def auth_handler():
    key = input("Enter authentication code: ")

    remember_device = True
    return key, remember_device


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def main():
    login, password = 'phonenumber', 'password'
    vk = vk_api.VkApi(
        login, password, app_id=2685278,
        auth_handler=auth_handler,
        captcha_handler=captcha_handler
    )
    try:
        vk.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    longpoll = VkLongPoll(vk)
    vk = vk.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            wordyes = ['да', ' дыа', ' д а ', ' согл', 'даа', ]
            wordno = ['нет', 'не-а', 'неа', 'не', 'нетушки', 'неть', 'не согласен']
            wordhi = ['йо', 'привет', 'здарова', 'здравствуйте', 'доброе', 'дорбый', 'йоу']
            for x in range(len(wordhi)):
                if event.from_user and wordhi[x] in event.text.lower():
                    vk.messages.send(
                        user_id=event.user_id,
                        message='привет, сейчас занят (от бота)',
                        random_id=get_random_id()
                    )
                    break
            for i in range(len(wordyes)):  # Если написали заданную фразу
                if event.from_user and wordyes[i] in event.text.lower():
                    vk.messages.send(
                        user_id=event.user_id,
                        message='нет (от бота)',
                        random_id=get_random_id()
                    )
                    break
            for n in range(len(wordno)):
                if event.from_user and wordno[n] in event.text.lower():
                    vk.messages.send(
                        user_id=event.user_id,
                        message=choice(wordyes) + '(от бота)',
                        random_id=get_random_id()
                    )
                    break


if __name__ == '__main__':
    main()
