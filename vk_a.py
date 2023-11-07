import requests
import vk_api
import chime
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from random import choice
from vk_api import VkUpload
from itertools import groupby
#Если вы хотите, что бы он у вас работал, тогда придётся скачивать через pip желательно requests и vk_api ибо всё это сюда не добавить))
session = requests.Session()
wordyes = ['да', ' дыа', 'д а ', ' согл', 'даа', ]
wordno = ['нет', 'не-а', 'неа', 'не', 'нетушки', 'неть', 'не согласен']
wordhi = ['йо', 'привет', 'здарова', 'здравствуйте', 'доброе', 'дорбый', 'йоу']
wordblg = ['спасибо', 'благодарю', 'благодарствую', 'спс', 'пасибо', 'спасибки', 'спасибочки']
words = 'мурат,срочно'
idusers = []

def auth_handler():
    key = input("Enter authentication code: ")

    remember_device = True
    return key, remember_device

def main():
    login, password = 'phonenumber', 'password'
    global vk, idusers
    vk = vk_api.VkApi(
        login, password, app_id=2685278,
        auth_handler=auth_handler
    )
    try:
        vk.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    longpoll = VkLongPoll(vk)
    vk = vk.get_api()
    attachments = []
    upload = VkUpload(vk)
    image_url = 'https://www.meme-arsenal.com/memes/0dad556c3aaa0fb4a164c0a890e3e569.jpg'
    image = session.get(image_url, stream=True)
    photo = upload.photo_messages(photos=image.raw)[0]
    attachments.append(
        'photo{}_{}'.format(photo['owner_id'], photo['id'])
    )
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            answer_message(event,
                           'сейчас занят и отвечает его автоответчик, если это срочно напишите !мурат,срочно!(Сол Гудмэн)',
                           wordhi, attachments)
            send_message(event, 'нет (Сол Гудмэн)', wordyes)
            send_message(event, choice(wordyes) + ' (Сол Гудмэн)', wordno)
            send_message(event, 'Пожалуйста (Сол Гудмэн)' + 'https://www.youtube.com/watch?v=LvYG3jEkMlE', wordblg)
            idusers.append(event.user_id)
            if event.from_user and words in event.text.lower():
                vk.messages.send(
                    user_id=event.user_id,
                    message='скоро он ответит (Сол Гудмэн)',
                    random_id=get_random_id()
                )
                idusers = [el for el, _ in groupby(idusers)]
                index = idusers.index(int(event.user_id))
                idusers.remove(idusers[index])
                print("ответь сейчас это важно")
                for i in range(3):
                    chime.theme('mario')
                    chime.success()

def send_message(event, message, words_type):
    for n in range(len(words_type)):
        if event.from_user and words_type[n] in event.text.lower():
            vk.messages.send(
                user_id=event.user_id,
                message=message,
                random_id=get_random_id()
            )
            break

def answer_message(event, message, word_type, attachments):
    for i in range(len(word_type)):
        if (event.from_user or event.from_chat) and word_type[i] in event.text.lower() and event.user_id not in idusers:
            vk.messages.send(
                user_id=event.user_id,
                message=message,
                attachment=','.join(attachments),
                random_id=get_random_id()
            )
            break

if __name__ == '__main__':
    main()
