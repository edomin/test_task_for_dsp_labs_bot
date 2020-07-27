import math
import os
import requests

from tgbot.working_dir import WorkingDir

def getDirSize(startPath):
    totalSize = 0
    for dirpath, _, filenames in os.walk(startPath):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                totalSize += os.path.getsize(fp)

    if totalSize == 0:
        return "0B"
    size_name = ("B", "KiB", "MiB", "GiB", "TiB", "PiB")
    i = int(math.floor(math.log(totalSize, 1024)))
    p = math.pow(1024, i)
    s = round(totalSize / p, 2)
    return "%s %s" % (s, size_name[i])

def ProcessDownloadMessage(bot, message, token):
    #bot.send_message(message.from_user.id, "Download")

    home = os.path.expanduser("~");
    tgbotDir = os.path.join(home, ".tgbot");
    archiveDir = "/tmp/tgbotArchive"

    if os.path.exists(archiveDir):
        os.system("rm -rf {dir}".format(dir=archiveDir))

    os.system("mkdir -p {dir}".format(dir=archiveDir))

    archiveFilename = os.path.join(archiveDir, "saved_data.zip")

    with WorkingDir(tgbotDir):
        zipCommand = (""
         "zip {archiveFilename} -r -0 -s 48m {audioDir} {photoDir}"
         "").format(
            archiveFilename=archiveFilename,
            audioDir="audio",
            photoDir="photo"
         )
        os.system(zipCommand)

    _, _, files = next(os.walk(archiveDir))
    filesCount = len(files)

    sendingMessage = (""
        "Отправляю {count} файл(а, ов) объёмом {size}. Пожалуйста, подождите..."
        "").format(count=filesCount, size=getDirSize(archiveDir))
    bot.send_message(message.chat.id, sendingMessage)

    for filename in os.listdir(archiveDir):
        filePath = os.path.join(archiveDir, filename)
        # Я хз почему, но через библиотеку pyTelegramBotAPI не получается
        # отправлять файлы больше 512кб. По текстам исключений ни фига не ясно,
        # в чем дело. И автор либы в issue всегда пишет на отъебись, мол, это у
        # тебя инет кривой и т. д. Даже разбираться с этим не хочу. Для
        # отправки файлов используем модуль requests
        with open(filePath, "rb") as file:
            url = "https://api.telegram.org/bot{token}/sendDocument".format(
             token=token)
            postData = {'chat_id': message.chat.id}
            postFile = {'document': file}
            response = requests.post(url, data=postData, files=postFile)

    bot.send_message(message.chat.id, "Файлы загружены")
