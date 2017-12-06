import requests
import telebot
import constant
import os

bot = telebot.TeleBot(constant.token)
def game_file_path(x):
    return "C:\\своя игра\\games\\" + str(x) + ".txt"
#хэндлер скачивания архива с паком в папку
@bot.message_handler(content_types = ["document"])
def download_pack(message):
    pack_info = bot.get_file(message.document.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(constant.token, pack_info.file_path))
    path = "C:\\своя игра\\сырые\\" + message.document.file_name
    with open(path,'wb') as pack:
        pack.seek(0)
        pack.write(file.content)
        bot.send_message(message.chat.id, "downloaded")
    path = '""C:\\Program Files\\7-Zip\\7z.exe" x -r "' + path + '" u "-oc:\\своя игра\\packs\\' + message.document.file_name[:len(message.document.file_name) - 4] + '""'
    os.system(path)
    os.system('dir /b "C:\своя игра\packs" > "C:\своя игра\packs.txt"')


@bot.message_handler(commands = ['start_game'])
def making_game(message):
    with open(game_file_path(message.chat.id), 'a+') as game:
        game.seek(0)
        if not game.readlines():
            game.write("2\n")
            bot.send_message(message.chat.id, "чтобы присоедениться к игре введите /join_game, чтобы начать игру введите /start_game")
    '''    else:
            game.seek(0)
        if (game.read().split()[0] == "2"):
            #вывести онлайн клавиатуру предлагающую начать игру с одной кнопкой, только если все записывшиеся в игру нажали на клавиатуру и еще добавить кнопку к пересозданию игры
            #если игра началась, то выводится выбор пака'''
@bot.message_handler(commands = ['join_game'])
def joining_game(message):
    with open(game_file_path(message.chat.id), '+rt') as game:
        game.seek(0)
        if not(not game.readlines()):
            game.seek(0)
            if(game.read().split()[0] == "2"):
                k = True
                for i in game.readlines():
                    if (i.split()[0] == str(message.from_user.id)):
                        k = False
                if (k):
                    game.write(str(message.from_user.id) + "\n")

#dir /b "C:\своя игра\packs > C:\своя игра\packs.txt
bot.polling()
