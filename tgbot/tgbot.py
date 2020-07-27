import os

import telebot

from tgbot.process.start_message import ProcessStartMessage
from tgbot.process.help_message import ProcessHelpMessage
from tgbot.process.audio import ProcessAudio
from tgbot.process.photo import ProcessPhoto
from tgbot.process.download_message import ProcessDownloadMessage
from tgbot.process.reset_message import ProcessResetMessage
from tgbot.process.text_message import ProcessTextMessage

class Tgbot:
    def __init__(self):
        home = os.path.expanduser("~");
        tokenfile = os.path.join(home, ".tgbot/token");
        with open(tokenfile) as file:
            self.token = file.read()

        if self.token[-1] == "\n":
            self.token = self.token[0:-1]

        self.bot = telebot.TeleBot(self.token)

        @self.bot.message_handler(commands=['start'])
        def GetStartMessage(message):
            ProcessStartMessage(self.bot, message)

        @self.bot.message_handler(commands=['help'])
        def GetHelpMessage(message):
            ProcessHelpMessage(self.bot, message)

        @self.bot.message_handler(content_types=['voice'])
        def GetAudio(message):
            ProcessAudio(self.bot, message, self.token)

        @self.bot.message_handler(content_types=['photo'])
        def GetPhoto(message):
            ProcessPhoto(self.bot, message, self.token)

        @self.bot.message_handler(commands=['reset'])
        def GetResetMessage(message):
            ProcessResetMessage(self.bot, message)

        @self.bot.message_handler(commands=['download'])
        def GetDownloadMessage(message):
            ProcessDownloadMessage(self.bot, message, self.token)

        @self.bot.message_handler(content_types=["text"])
        def get_text_message(message):
            ProcessTextMessage(self.bot, message)

    def Polling(self):
        self.bot.infinity_polling()
