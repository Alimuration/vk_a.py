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
            wordyes = ['да', ' дыа', 'д а ', ' согл', 'даа', ]
            wordno = ['нет', 'не-а', 'неа', 'не', 'нетушки', 'неть', 'не согласен']
            wordhi = ['йо', 'привет', 'здарова', 'здравствуйте', 'доброе', 'дорбый', 'йоу']
            wordblg = ['спасибо', 'благодарю', 'благодарствую', 'спс', 'пасибо', 'спасибки', 'спасибочки']
            words = 'мурат,срочно'
            idusers = []
            for x in range(len(wordhi)):
                if (event.from_user and (wordhi[x] in event.text.lower()
                                         or event.text.lower() == 'мурат')) and event.user_id not in idusers:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='сейчас занят и отвечает его автоответчик, если это срочно напишите !мурат,срочно!(Сол Гудмэн)',
                        attachment=','.join(attachments),
                        random_id=get_random_id()
                    )
                    print("message was send by: " + str(event.user_id),
                          "and his(er) was added on massive" + str(idusers))
                    break
                if event.from_chat and event.text.lower() == 'мурат':
                    vk.messages.send(
                        user_id=event.user_id,
                        message='сейчас занят и отвечает его автоответчик, если это срочно напишите !мурат,срочно!(Сол Гудмэн)',
                        attachment=','.join(attachments),
                        random=get_random_id()
                    )
                    print('сообщение привет 1')
                    break
                if event.from_user and event.text == 'да' or event.text == 'lf' or event.text == 'дыа' or event.text == 'дааа' or event.text == 'да!':
                    vk.messages.send(
                        user_id=event.user_id,
                        message='нет (Сол Гудмэн)',
                        random_id=get_random_id()
                    )
                    print('сообщение привет 2')
                    break
            idusers.append(event.user_id)
            for n in range(len(wordno)):
                if event.from_user and wordno[n] in event.text.lower():
                    vk.messages.send(
                        user_id=event.user_id,
                        message=choice(wordyes) + '(Сол Гудмэн)',
                        random_id=get_random_id()
                    )
                    print('сообщение привет 3')
                    break
            for x in range(len(wordblg)):
                if event.from_user and wordblg[x] in event.text.lower():
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Пожалуйста (Сол Гудмэн)' + 'https://www.youtube.com/watch?v=LvYG3jEkMlE',
                        random_id=get_random_id()
                    )
                    print('сообщение привет 4')
                    break
            if event.from_user and words in event.text.lower():
                print("ответь сейчас это важно")
                vk.messages.send(
                    user_id=event.user_id,
                    message='скоро он ответит (Сол Гудмэн)',
                    random_id=get_random_id()
                )
                print('сообщение привет 5')
                print(idusers)
                index = idusers.index(int(event.user_id))
                idusers.remove(idusers[index])
                print(idusers)
                for i in range(3):
                    chime.theme('mario')
                    chime.success()


if __name__ == '__main__':
    main()
