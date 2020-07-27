import os
import shutil

from tgbot.config import START

def EraseDir(dirName):
    for filename in os.listdir(dirName):
        filePath = os.path.join(dirName, filename)
        try:
            if os.path.isfile(filePath) or os.path.islink(filePath):
                os.unlink(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (filePath, e))

def ProcessResetMessage(bot, message):
    #bot.send_message(message.from_user.id, "Reset")
    home = os.path.expanduser("~");
    tgbotDir = os.path.join(home, ".tgbot");
    audioDir = os.path.join(tgbotDir, "audio");
    photoDir = os.path.join(tgbotDir, "photo");

    EraseDir(audioDir)
    EraseDir(photoDir)

    bot.send_message(message.chat.id, "Файлы удалены с сервера")
