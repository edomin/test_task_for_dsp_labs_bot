#!venv/bin/python

import os

import config
import telebot

home = os.path.expanduser("~");
tokenfile = os.path.join(home, ".tgbots/test_task_for_dsp_labs_bot");
with open(tokenfile) as file:
    token = file.read()

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.infinity_polling()
