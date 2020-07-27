from tgbot.config import START

def ProcessStartMessage(bot, message):
    bot.send_message(message.chat.id, START)
