import os

def ProcessAudio(bot, message, token):
    uid = message.from_user.id
    #bot.send_message(uid, "Audio")
    fileId = message.voice.file_id
    tgFile = bot.get_file(fileId).file_path
    link = "https://api.telegram.org/file/bot{token}/{tgFile}".format(
     token=token, tgFile=tgFile)
    wgetCommand = "wget \"{link}\" -O /tmp/tgbot_audio.ogg".format(link=link)
    os.system(wgetCommand)

    ffmpegCommand = ("ffmpeg -y -i /tmp/tgbot_audio.ogg -acodec pcm_s16le "
     "-ar 16000  /tmp/tgbot_audio.wav")
    os.system(ffmpegCommand)

    home = os.path.expanduser("~");
    uidDir = os.path.join(home, ".tgbot/audio", str(uid));

    if not os.path.exists(uidDir):
        os.system("mkdir -p {dir}".format(dir=uidDir))

    _, _, files = next(os.walk(uidDir))
    filesCount = len(files)

    cpCommand = "cp {src} {dstDir}/audio_message_{num}.wav".format(
     src="/tmp/tgbot_audio.wav", dstDir=uidDir, num=filesCount)
    os.system(cpCommand)
