from subprocess import Popen, PIPE, STDOUT
import telebot
import yaml
import os

with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

termit = telebot.TeleBot(config['token'])
allowedUsers = config['allowedUsers']
rootUser = None
directory = '/'

@termit.message_handler(commands=["start"])
def start(message, res=False):
    termit.send_message(message.chat.id, "You can check IP of bot host by /ip command, also you can check your ID by /id. To open shell use /shell, to close it /close. May the force be with you, it's root.")

@termit.message_handler(commands=["ip"])
def start(message, res=False):
    if message.chat.id in allowedUsers:
        ip = os.popen('wget -O - -q icanhazip.com').read()
        termit.send_message(message.chat.id, f'Bot host IP: {ip}')
    else:
       termit.send_message(message.chat.id, f'You are not allowed to be here.') 

@termit.message_handler(commands=["id"])
def start(message, res=False):
    ip = os.popen('wget -O - -q icanhazip.com').read()
    termit.send_message(message.chat.id, f'Your TG ID is: {message.chat.id}')

@termit.message_handler(commands=["shell"])
def start(message, res=False):
    if message.chat.id in allowedUsers:
        global rootUser
        global directory
        if rootUser:
            termit.send_message(message.chat.id, f'User {rootUser} is already use root.')
        else:
            rootUser = message.chat.id
            directory = '/'
    else:
       termit.send_message(message.chat.id, f'You are not allowed to be here.')

@termit.message_handler(commands=["close"])
def start(message, res=False):
    global rootUser
    global directory
    if rootUser == message.chat.id:
        rootUser = None
        directory = '/'
    else:
        termit.send_message(message.chat.id, f'You have no sessions to close.')

@termit.message_handler(commands=["root"])
def start(message, res=False):
    global rootUser
    termit.send_message(message.chat.id, f'{rootUser} is now root in shell')
    
@termit.message_handler(content_types=["text"])
def handler(message):
    global directory
    if rootUser == message.chat.id:
        print(directory)
        os.chdir(directory)
        command = message.text.strip()
        process = Popen(f'{command} ; echo CURRENTDIR: ; pwd ', shell=True, stdout=PIPE, stderr=STDOUT, close_fds=True)
        result = process.stdout.read().decode().split('CURRENTDIR:')
        directory = result[1].strip()
        if result:
            termit.send_message(message.chat.id, f'{result[0]}')
        
    else:
        termit.send_message(message.chat.id, f'You are not in shell mode!')

# start bot
termit.polling(none_stop=True, interval=0)
