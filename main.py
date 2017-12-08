import requests
import telebot
import constant
import os
import time
from telebot import types
import pars as kk

bot = telebot.TeleBot(constant.token)
x = kk.Packislav()
#----------------------------------------------------
def game_file_path(x):
    return "C:\\своя игра\\games\\" + str(x)[1:] + ".txt"


def check(username):
    if username in x.players:
        return True
    else:
        return False

def final():
    keyboard = types.InlineKeyboardMarkup(row_width = 1)
    callback_button = []
    for i in x.score:
        print(i)
        callback_button.append(types.InlineKeyboardButton(text = str(str(i[0]) + " " + str(i[1])), callback_data = "gg"))
    for i in callback_button:
        keyboard.add(i)
    os.system(str('del "' + game_file_path(message.chat.id) + '"'))
    return(keyboard)

def keyboard1(round, id, theme = None, message_id = None, result = True):
    keyboard = types.InlineKeyboardMarkup(row_width = 6)
    if not(not theme):
        print(str(theme) + " " + str(message_id))
    x.IsAlive = False
    x.IsClear = True;
    print(x.round_name(round))
    '''x.theme_counter(round)'''
    for j in range(1):
        callback_button = []
        callback_button.append(types.InlineKeyboardButton(text = str(j + 1), callback_data="themeqqqq" + str(round) + "qqqq" + str(j)))
        for i in range(0, 5):
            k = x.question(round, j, i)
            if (k[0]):
                x.IsAlive = True
                callback_button.append(types.InlineKeyboardButton(text=str(k[1]), callback_data="questionqqqq"  + str(round) + "qqqq" + str(j) + "qqqq" + str(i) ))
            else:
                x.IsClear = False
                callback_button.append(types.InlineKeyboardButton(text=":)", callback_data="ignore"))
        keyboard.add(callback_button[0], callback_button[1], callback_button[2], callback_button[3], callback_button[4], callback_button[5])
    if result:
        result_button = types.InlineKeyboardButton(text = "Узнать счет", callback_data="show_result")
        keyboard.add(result_button)
    if x.IsAlive:
        if theme != None:
            bot.edit_message_text(chat_id = id, message_id = message_id, text = x.round_name(round) + "\n" + x.theme_name(round, theme) + "\nВыбирает вопрос: " + x.ved, reply_markup = keyboard)
        else:
            if x.IsClear:
                bot.send_message(id, text = x.round_name(round) + "\n" + x.round_themes(round) + "\nВыбирает вопрос: " + x.ved, reply_markup = keyboard)
            else:
                bot.send_message(id, text = x.round_name(round) +  "\nВыбирает вопрос: " + x.ved, reply_markup = keyboard)
    else:
        x.next_round()
        if not x.end_game:
            keyboard1(x.c_r, id, result = result)
        else:
            bot.send_message(id, "Результаты игры\n" + x.score_table())
'''    if x.IsAlive:
        TTR
    else:
        x.next_round()
        if not x.end_game:
            return keyboard1(x.c_r)s
        else:
            return final()'''

def show_result(id):
    bot.send_message(id, x.score_table())
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
            start_keyboard = types.InlineKeyboardMarkup(row_width = 1)
            join_button = types.InlineKeyboardButton(text="Присоединиться к игре", callback_data="join_game")
            start_keyboard.add(join_button)
            start_button = types.InlineKeyboardButton(text="Начать игру", callback_data="start_game")
            start_keyboard.add(start_button)
            bot.send_message(message.chat.id, "Лобби\n" + x.show_players(), reply_markup = start_keyboard)
        else:
            game.seek(0)
            if (game.readline().split()[0] == "2"):
                start_keyboard = types.InlineKeyboardMarkup()
                start_button = types.InlineKeyboardButton(text="Начать игру", callback_data="start_game")
                restart_button = types.InlineKeyboardButton(text="Пересоздать игру", callback_data="restart_game")
                start_keyboard.add(start_button, restart_button)
                bot.send_message(message.chat.id,"Начать игру?", reply_markup = start_keyboard)

@bot.message_handler(commands = ['delete_game'])
def key(message):
    os.system(str('del "' + game_file_path(message.chat.id) + '"'))
    x = kk.Packislav()
    x.players = {}
    print(x.players)
    print(x.show_players())

@bot.callback_query_handler(func=lambda call: call.data == "restart_game")
def restarting_game(call):
    message = call.message
    start_keyboard = types.InlineKeyboardMarkup()
    os.system(str('del "' + game_file_path(message.chat.id) + '"'))
    with open(game_file_path(message.chat.id), 'a+') as game:
        game.write("2\n")
    join_button = types.InlineKeyboardButton(text="Присоединиться к игре", callback_data="join_game")
    start_keyboard.add(join_button)
    start_button = types.InlineKeyboardButton(text="Начать игру", callback_data="start_game")
    start_keyboard.add(start_button)
    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Лобби\n" + x.show_players(), reply_markup = start_keyboard)



@bot.callback_query_handler(func=lambda call: call.data == "start_game")
def starting_game(call):
    if check(call.from_user.username):
        message = call.message
        chose_keyboard = types.InlineKeyboardMarkup()
        with open("c:\\своя игра\\packs.txt", "r") as packs:
            for pack in packs.readlines():
                chose_keyboard.add(types.InlineKeyboardButton(text=pack, callback_data="packqqqq" +pack))
                bot.send_message(message.chat.id,"Выбирайте пак", reply_markup = chose_keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "join_game")
def joining_game(call):
    message = call.message
    with open(game_file_path(message.chat.id), 'a+') as game:
        game.seek(0)
        if not(not game.readlines()):
            game.seek(0)
            if(game.readline().split()[0] == "2"):
                k = True
                players = game.readline().split()
                print(x.players)
                print(call.from_user.username)
                if not(not players):
                    for player in players:
                        print(player)
                        if player == call.from_user.username:
                            k = False
                if (k):
                    game.write(str(call.from_user.username) + " ")
                    x.add_player(call)
                    start_keyboard = types.InlineKeyboardMarkup()
                    join_button = types.InlineKeyboardButton(text="Присоединиться к игре", callback_data="join_game")
                    start_keyboard.add(join_button)
                    start_button = types.InlineKeyboardButton(text="Начать игру", callback_data="start_game")
                    start_keyboard.add(start_button)
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Лобби\n" + x.show_players(), reply_markup = start_keyboard)

@bot.callback_query_handler(func=lambda call: call.data.split("qqqq")[0] == "pack")
def callback_inline(call):
    with open(game_file_path(call.message.chat.id), "r+") as game1:
        if int(game1.readline()[0]) == 2:
            k = True
        else:
            k = False
        if check(call.from_user.username) and k:
            for i in x.players.items():
                x.set_ved(i[0])
                break
            with open(game_file_path(call.message.chat.id), "r+") as game:
                game.write("1")
            path = 'c:\\своя игра\\packs\\' + call.data.split("qqqq")[1][:-1] + '\\content.xml'
            x.chose_pack(path)
            x.start_game()
            keyboard1(x.c_r, call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.split("qqqq")[0] == "answer")
def answering(call):
    if check(call.from_user.username):
        if x.start_answer:
            x.start_answer = False;
            k = call.data.split("qqqq")
            x.player_answer = call.from_user.username
            x.end_qustion = True
            bot.send_message(call.message.chat.id, "@" + str(call.from_user.username) + " Отвечает на вопрос")

@bot.message_handler(func=lambda message: message.from_user.username == x.player_answer)
def check_answer(message):
    if x.end_qustion:
        x.end_qustion = False
        x.Posted = True
        x.last_answer = message.text
        result_keyboard = types.InlineKeyboardMarkup()
        if (message.text == x.c_q[3]):
            dispute = types.InlineKeyboardButton(text="Ответ неверный", callback_data="dispute_unright")
            result_keyboard.add(dispute)
            bot.send_message(message.chat.id, str("Верно!\n[+" +  str(x.c_q[1]) + "]\nОтвет: " + str(x.c_q[3])), reply_markup = result_keyboard)
            x.players[message.from_user.username] += int(x.c_q[1])
            x.set_ved(message.from_user.username)
        else:
            dispute = types.InlineKeyboardButton(text="Ответ верный", callback_data="dispute_right")
            result_keyboard.add(dispute)
            bot.send_message(message.chat.id, "Неверно\n[-" +  str(x.c_q[1]) + "]\nОтвет: " + str(x.c_q[3]), reply_markup = result_keyboard)
            x.players[message.from_user.username] -= int(x.c_q[1])
        keyboard1(x.c_r, message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.split("qqqq")[0] == "question")
def callback_inline(call):
    if x.ved == call.from_user.username and not x.start_dispute:
        x.c_q = None
        x.Posted = False
        x.player_answer = None
        x.start_dispute = False
        k = call.data.split("qqqq")
        x.question_edit(int(k[1]),int(k[2]),int(k[3]))
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text ="Тема: " + x.theme_name(int(k[1]), int(k[2])) + "\n\n" + x.question(int(k[1]),int(k[2]),int(k[3]))[2])
        ''' tut был sleep'''
        answer_keyboard = types.InlineKeyboardMarkup()
        answer_button = types.InlineKeyboardButton(text="Ответить на вопрос", callback_data="answerqqqq" + call.data)
        answer_keyboard.add(answer_button)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text ="Тема: " + x.theme_name(int(k[1]), int(k[2])) + "\n\n" + x.question(int(k[1]),int(k[2]),int(k[3]))[2], reply_markup =answer_keyboard)
        x.start_answer = True
        x.c_q = x.question(int(k[1]),int(k[2]),int(k[3]))

@bot.callback_query_handler(func=lambda call: call.data == "dispute_right")
def golosovanie(call):
    print("1")
    if check(x.player_answer) and x.Posted:
        x.Posted = False
        dispute_keyboard = types.InlineKeyboardMarkup()
        answer_right = types.InlineKeyboardButton(text="Ответ верный", callback_data="++")
        answer_unright = types.InlineKeyboardButton(text="Ответ неверный", callback_data="+-")
        dispute_keyboard.add(answer_right, answer_unright)
        x.start_dispute = True
        bot.send_message(call.message.chat.id, "Аппеляция Ответа" + "\nВерный Ответ : " + x.c_q[3] + "\nОтвет @" + x.player_answer + " : " + x.last_answer, reply_markup = dispute_keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "dispute_unright")
def golosovanie(call):
    print("1")
    if check(x.player_answer) and x.Posted:
        x.Posted = False
        dispute_keyboard = types.InlineKeyboardMarkup()
        answer_right = types.InlineKeyboardButton(text="Ответ неверный", callback_data="-+")
        answer_unright = types.InlineKeyboardButton(text="Ответ верный", callback_data="--")
        dispute_keyboard.add(answer_right, answer_unright)
        x.start_dispute = True
        bot.send_message(call.message.chat.id, "Аппеляция Ответа\nВерный Ответ : " + x.c_q[3] + "\nОтвет @" + x.player_answer + " : " + x.last_answer, reply_markup = dispute_keyboard)


#-------------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "++")
def overall(call):
    if check(call.from_user.username) and (not call.from_user.username == x.player_answer) and x.start_dispute:
        x.players[x.player_answer] += 2*int(x.c_q[1])
        x.set_ved(x.player_answer)
        x.player_answer = ''
        x.start_dispute = False;
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Аппеляция принята\n[+" +  str(x.c_q[1]) + "]")

@bot.callback_query_handler(func=lambda call: call.data == "+-")
def overall(call):
    if check(call.from_user.username) and (not call.from_user.username == x.player_answer) and x.start_dispute:
        x.player_answer = ''
        x.start_dispute = False;
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Аппеляция отклонена")

@bot.callback_query_handler(func=lambda call: call.data == "-+")
def overall(call):
    if check(call.from_user.username) and (not call.from_user.username == x.player_answer) and x.start_dispute:
        x.players[x.player_answer] -= 2*int(x.c_q[1])
        x.set_ved(x.ved_last)
        x.player_answer = ''
        x.start_dispute = False;
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Аппеляция принята\n[-" +  str(x.c_q[1]) + "]")

@bot.callback_query_handler(func=lambda call: call.data == "--")
def overall(call):
    if check(call.from_user.username) and (not call.from_user.username == x.player_answer) and x.start_dispute:
        x.player_answer = ''
        x.start_dispute = False;
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Аппеляция отклонена")

#--------------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "show_result")
def show_table(call):
    if check(call.from_user.username):
        show_result(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.split("qqqq")[0] == "theme")
def callback_inline(call):
        if (check(call.from_user.username)):
            k = call.data.split("qqqq")
            print("1")
            print(x.theme_name(int(k[1]), int(k[2])) + " " + call.message.text.split("\n")[1])
            if (not x.theme_name(int(k[1]), int(k[2])) == call.message.text.split("\n")[1]):
                keyboard1(round = int(k[1]), id = call.message.chat.id, theme = int(k[2]), message_id = call.message.message_id)
#dir /b "C:\своя игра\packs > C:\своя игра\packs.txt
bot.polling()
