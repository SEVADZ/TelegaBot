import requests
import telebot
import constant
import os

bot = telebot.TeleBot(constant.token)

#хэндлер скачивания архива с паком в папку
@bot.message_handler(content_types = ["document"])
def download_pack(message):
    pack_info = bot.get_file(message.document.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(constant.token, pack_info.file_path))
    path = "C:\\своя игра\\packs\\сырые\\" + message.document.file_name
    with open(path,'wb') as pack:
        pack.seek(0)
        pack.write(file.content)
        bot.send_message(message.chat.id, "downloaded")
    path = '""C:\\Program Files\\7-Zip\\7z.exe" x -r "' + path + '" u "-oc:\\своя игра\\packs\\' + message.document.file_name[:len(message.document.file_name) - 4] + '""'
    os.system(path)

bot.polling()
