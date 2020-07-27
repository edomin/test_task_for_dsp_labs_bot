import os
import face_recognition

def ProcessPhoto(bot, message, token):
    uid = message.from_user.id
    #bot.send_message(uid, "Photo")

    maxHeight = 0

    for photoSize in message.photo:
        if photoSize.height > maxHeight:
            maxHeight = photoSize.height
            maxHeightPhotoSize = photoSize

    fileId = maxHeightPhotoSize.file_id
    tgFile = bot.get_file(fileId).file_path
    link = "https://api.telegram.org/file/bot{token}/{tgFile}".format(
     token=token, tgFile=tgFile)
    wgetCommand = "wget \"{link}\" -O /tmp/tgbot_photo".format(link=link)
    os.system(wgetCommand)

    image = face_recognition.load_image_file("/tmp/tgbot_photo")
    faceLocations = face_recognition.face_locations(image)

    if len(faceLocations) > 0:
        home = os.path.expanduser("~");
        uidDir = os.path.join(home, ".tgbot/photo", str(uid));

        if not os.path.exists(uidDir):
            os.system("mkdir -p {dir}".format(dir=uidDir))

        _, _, files = next(os.walk(uidDir))
        filesCount = len(files)

        cpCommand = "cp {src} {dstDir}/photo_{num}.jpeg".format(
         src="/tmp/tgbot_photo", dstDir=uidDir, num=filesCount)
        os.system(cpCommand)
