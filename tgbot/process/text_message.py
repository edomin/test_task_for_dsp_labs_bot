from tgbot.config import UNKNOWN

def ProcessTextMessage(bot, message):
    bot.send_message(message.chat.id, UNKNOWN)
