import requests
import telebot
import constant
import os
from telebot import types
import pars as kk
def game_file_path(x):
    return "C:\\своя игра\\games\\" + str(x) + ".txt"
x = kk.Packislav("C:\\своя игра\\packs\\sadf\\content.xml")
bot = telebot.TeleBot(constant.token)
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

#-----------------------------------------------------------------------
@bot.message_handler(commands = ['start_game'])
def making_game(message):
    with open(game_file_path(message.chat.id), 'a+') as game:
        game.seek(0)
        if not game.readlines():
            game.write("2\n")
            start_keyboard = types.InlineKeyboardMarkup()
            join_button = types.InlineKeyboardButton(text="Присоедениться к игре", callback_data="join_game")
            start_keyboard.add(join_button)
            bot.send_message(message.chat.id, "чтобы начать игру еще раз введите /start_game", reply_markup = start_keyboard)
        else:
            game.seek(0)
            if (game.read().split()[0] == "2"):
                start_keyboard = types.InlineKeyboardMarkup()
                start_button = types.InlineKeyboardButton(text="Начать игру", callback_data="start_game")
                restart_button = types.InlineKeyboardButton(text="Пересоздать игру", callback_data="restart_game")
                start_keyboard.add(start_button, restart_button)
                bot.send_message(message.chat.id,"Начать игру?", reply_markup = start_keyboard)
            #вывести онлайн клавиатуру предлагающую начать игру с одной кнопкой, только если все записывшиеся в игру нажали на клавиатуру и еще добавить кнопку к пересозданию игры
            #если игра началась, то выводится выбор пака'''

def keyboard(round):
    keyboard = types.InlineKeyboardMarkup(row_width = 6)
    for j in range(x.theme_counter(round)):
        callback_button = []
        callback_button.append(types.InlineKeyboardButton(text=str(j + 1), callback_data="themeqqqq" + str(round) + "qqqq" + str(j)))
        for i in range(0, 5):
            k = x.question(round,j,i)
            if (k[0]):
                callback_button.append(types.InlineKeyboardButton(text=str(k[1]), callback_data="questionqqqq"  + str(round) + "qqqq" + str(j) + "qqqq" + str(i) ))
            else:
                callback_button.append(types.InlineKeyboardButton(text="TTR", callback_data="ignore"))
        keyboard.add(callback_button[0], callback_button[1], callback_button[2], callback_button[3], callback_button[4], callback_button[5])
    return keyboard

@bot.message_handler(commands = ['keyboard'])
def key(message):
    bot.send_message(message.chat.id, "выберете вопрос", reply_markup = keyboard(0))

@bot.callback_query_handler(func=lambda call: call.data == "join_game")
def joining_game(call):
    message = call.message
    with open(game_file_path(message.chat.id), '+rt') as game:
        game.seek(0)
        if not(not game.readlines()):
            game.seek(0)
            if(game.read().split()[0] == "2"):
                k = True
                players = game.read().split()
                if not(not players):
                    for player in players:
                        if player in x.players:
                            k = False
                if (k):
                    game.write(str(message.from_user.id) + " ")
                    x.add_player(str(message.from_user.id))


@bot.callback_query_handler(func=lambda call: call.data.split("qqqq")[0] == "question")
def callback_inline(call):
        k = call.data.split("qqqq")
        x.question_edit(int(k[1]),int(k[2]),int(k[3]))
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text ="Тема: " + x.theme_name(int(k[1]), int(k[2])) + "\n\n" + x.question(int(k[1]),int(k[2]),int(k[3]))[2])

@bot.callback_query_handler(func=lambda call: call.data.split("qqqq")[0] == "theme")
def callback_inline(call):
        k = call.data.split("qqqq")
        if(not x.theme_name(int(k[1]), int(k[2])) == call.message.text):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = x.theme_name(int(k[1]), int(k[2])), reply_markup = keyboard(0 ))

#dir /b "C:\своя игра\packs > C:\своя игра\packs.txt
bot.polling()
