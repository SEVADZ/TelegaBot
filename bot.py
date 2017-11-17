# -*- coding: utf-8 -*-
'''
МЕЙН ФАЙЛ БОТА ТЕСТИ В TEST.PY
'''
import telebot
import constant
bot = telebot.TeleBot(constant.token)
for i in range(50):
    bot.send_message(constant.xrom, str(i))
bot.send_message(constant.xrom, "ХАХА ЗАСПАМИЛ")
bot.polling(none_stop = True, interval = 0)
