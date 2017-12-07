import telebot
import constant
import pars as kk
from telebot import types

bot = telebot.TeleBot(constant.token)
x = kk.Packislav("C:\\своя игра\\packs\\sadf\\content.xml", 1)
current_round = 1

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

bot.polling()
