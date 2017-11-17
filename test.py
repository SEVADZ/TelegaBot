# -*- coding: utf-8 -*-
import constant
import telebot
import requests
'''
    тести тут шо хочешь
'''
bot = telebot.TeleBot(constant.token)
@bot.message_handler(content_types=['text'])
def answer(message):
    with open("info.txt", 'a+', encoding='utf-8') as f:
        st = str(message.chat.id) + " " + str(message.chat.username)
        f.seek(0, 0)
        t = True
        for line in f:
            if (line.find(str(message.chat.id)) != -1):
                t = False
        if (t):
            f.seek(0,2)
            f.write(st + "\n")
    if (message.text == 'закрой бля'):
        keyboard(message, 0)
    if (message.text == 'открой бля'):
        keyboard(message, 1)

def keyboard(message, x):
    if (x == 1):
        key_open = telebot.types.ReplyKeyboardMarkup()
        key_open.row('ДА ЭТО ЖЕСТКО', 'закрой бля')
        bot.send_message(message.chat.id,'здарова карова',reply_markup =  key_open)
    else:
        key_close = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'базАРУ НЕT', reply_markup = key_close)
bot.polling(none_stop = True, interval = 0)
