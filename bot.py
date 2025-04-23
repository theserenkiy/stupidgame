import requests
import random
import time
from db import sqlUser


class Bot:
    def __init__(self):
        self.token = ""
        with open('token.json') as t:
            self.token = eval(t.read())['token']

    def execute(self, method: str):
        req = f"https://api.telegram.org/bot{self.token}/{method}"
        a = requests.post(req).json()
        return a


def BotC():
    bot = Bot()
    lastOffset = 0
    random.seed(time.time())
    print(sqlUser.execute("SELECT * FROM Players"))
    while True:
        a = bot.execute(f"getUpdates?offset={lastOffset}")
        for i in a['result']:  # основной код обработки команд
            if 'entities' in i['message']:
                if i['message']['entities'][0]['type'] == 'bot_command':

                    if i['message']['text'].split(':')[0] == '/start':
                        text = ("это - чат для создания персонажа. вы можете настроить здесь имя и фотографию" +
                                "своего персонажа \n что бы создать персонажа отправьте команду /createUser и через " +
                                "пробел введите имя \n что бы удалить пользователя введите /destroyUser и через " +
                                "пробел ID пользователя")
                        bot.execute(f"sendMessage?chat_id={i['message']['chat']['id']}&text={text}")

                    if i['message']['text'].split()[0] == '/createUser':
                        args = i['message']['text'].split()
                        if len(args) > 1:
                            uID = f'{random.randint(1, 10 ** 10)}'
                            cm = f"INSERT INTO Players (id, name) VALUES ('{uID}', '{args[1]}')"
                            sqlUser.execute(cm)
                            bot.execute(f"sendMessage?chat_id={i['message']['chat']['id']}&text=пользователь создан")
                            ans = f'ID пользователя: "{uID}"'
                            bot.execute(f"sendMessage?chat_id={i['message']['chat']['id']}&text={ans}")
                        else:
                            bot.execute(f"sendMessage?chat_id={i['message']['chat']['id']}&text=введите имя")
                    if i['message']['text'].split()[0] == '/destroyUser':
                        args = i['message']['text'].split()
                        if len(args) > 1:
                            name = sqlUser.execute(f"SELECT name FROM Players WHERE id='{args[1]}'")
                            cm = f"DELETE FROM Players WHERE id='{args[1]}'"
                            sqlUser.execute(cm)
                            bot.execute(f"sendMessage?chat_id={i['message']['chat']['id']}&text=пользователь {name} удален")
                        else:
                            bot.execute(f"sendMessage?chat_id={i['message']['chat']['id']}&text=введите ID")

        if a['result']:
            lastOffset = a['result'][-1]['update_id'] + 1
        time.sleep(1)


BotC()
