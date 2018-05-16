#!/usr/bin/python3
import fileinput
from rocketchat.api import RocketChatAPI
from pathlib import Path
import sys

user = ''
password = ''
chat = ''
chat_url = ''
file_read = ''

show_help = False
if len(sys.argv) == 1:
    show_help = True

if len(sys.argv) > 1:
    if (sys.argv[1] == '--help') or (sys.argv[1] == '-h'): 
        show_help = True

if show_help == 1:
    print ('Отправка сообщений в групповые чаты Rocket.Chat')
    print ('Например: echo "Сообщение!" | ./rocketsend.py send')
    print ('')
    print ('Отправляемое сообщение получается из stdin или используйте ключ -f=<Имя файла сообщения>.')
    print ('Используйте ключи: -u=<Имя пользователя> -p=<Пароль пользователя> -c=<Наименование группового чата> -url=<URL-подключения>')
    print ('так же вы можете задать часть параметров в конфигурационном файле /etc/rocketsend/rocket.conf в виде:')
    print ('USER = Имя пользователя')
    print ('PASSWORD = Пароль')
    print ('GROUP_CHAT = Наименование группового чата')
    print ('CHAT_URL = URL-подключения к сервису')
    print ('Обратите внимание, что параметры командной строки переопределяют конфигурацию по умолчанию из файла')
    sys.exit()

config_file = Path("/etc/rocketsend/rocket.conf")
if config_file.is_file():
    conf_file=open("/etc/rocketsend/rocket.conf",'r')
    for line in conf_file.read().split('\n'):
        if line.startswith('USER'):
            if line.count('=')>0:
                user = line.split('=')[1].strip().replace('"','')

        if line.startswith('PASSWORD'):
            if line.count('=')>0:
                password = line.split('=')[1].strip().replace('"','')  

        if line.startswith('GROUP_CHAT'):
            if line.count('=')>0:
                chat = line.split('=')[1].strip().replace('"','') 

        if line.startswith('CHAT_URL'):
            if line.count('=')>0:
                chat_url = line.split('=')[1].strip().replace('"','') 

    conf_file.close()
    

for param in sys.argv:
    if param.startswith('-u='):
        user = param.split('-u=')[1].strip().replace('"','')

    if param.startswith('-p='):
        password = param.split('-p=')[1].strip().replace('"','')

    if param.startswith('-c='):
        chat = param.split('-c=')[1].strip().replace('"','')

    if param.startswith('-url='):
        chat_url = param.split('-url=')[1].strip().replace('"','')        

    if param.startswith('-f'):
        file_read = param.split('-f=')[1].strip().replace('"','') 

if user == '':
    print ('Не задано имя пользователя (параметр -u=<Имя пользователя> или конфигурационный параметр USER = <Имя пользователя>)')
    sys.exit()

if password == '':
    print ('Не задан пароль пользователя (параметр -p=<Пароль пользователя> или конфигурационный параметр PASSWORD = <Имя пользователя>)')
    sys.exit()

if chat == '':
    print ('Укажите групповой чат (параметр -c=<Наименование группового чата> или конфигурационный параметр GROUP_CHAT = <Наименование группового чата>)')
    sys.exit()

if chat_url == '':
    print ('Укажите URL-подключения Rocket.Chat (параметр -url=<URL-подключения к сервису> или конфигурационный параметр CHAT_URL = URL-подключения к сервису)')
    sys.exit()

api = RocketChatAPI(settings={'username': user, 'password': password, 'domain': chat_url})
room_id = ''
for room in api.get_private_rooms():
    if room['name'] == chat:
        room_id = room['id']

if room_id == '':
    print ('Общий чат с таким именем не зарегистрирован')

if file_read == '':
    input_message = ''
    for line in  sys.stdin:
        input_message = input_message + line
else:
    message_file = open(file_read,'r')
    input_message = message_file.read()
    message_file.close()

api.send_message(input_message, room_id)
print ('Сообщение отправлено!')
