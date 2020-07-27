from tgbot.config import HELP

def ProcessHelpMessage(bot, message):
    bot.send_message(message.chat.id, HELP)
