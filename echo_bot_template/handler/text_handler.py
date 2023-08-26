# installing packedges
from telebot.types import Message

# local variables and functions
from loader import bot

@bot.message_handler(regexp="Assalomu aleykum")
def replay_greating(message: Message):
    """ aniq bir sozga javob qaytarish 1-part """
    chat_id = message.chat.id # request.user
    bot.send_message(chat_id, "Valeykum Assalom")


# @bot.message_handler(func=lambda message: message.text == "Assalomu Aleykum")
# def replay_greating(message: Message):
#     """ aniq bir sozga javob qaytarish 2-part """
#     chat_id = message.chat.id # request.user
#     bot.send_message(chat_id, "Valeykum Assalom")


content_types = ["text", "photo", "document", "voice", "sticker", "animation", "video", "audio"]

@bot.message_handler(content_types=content_types)
def reaction_text(message: Message):
    """ when user send any things return himself """
    chat_id = message.chat.id # request.user
    
    if message.content_type == "text":
        data = f"You write word is: {message.text}\n\nLength: {len(message.text)}\nTitle: {message.text.title()}\nUpperCase: {message.text.upper()}\nLowercase: {message.text.lower()}\nSplite: {message.text.split()}" # text data type
        bot.send_message(chat_id, data) # return data
    
    elif message.content_type == "photo":
        data = message.photo[0].file_id # get photo data 
        caption = f"FileUniqueId: {message.photo[0].file_unique_id} \nFileSize: {message.photo[0].file_size} kb\nFileHeight: {message.photo[0].height}\nFileWidth: {message.photo[0].width}"
        print(message)
        bot.send_photo(chat_id, data, caption) # return data
    
    elif message.content_type == "document":
        data = message.document.file_id # get document data
        caption = f"FileName: {message.document.file_name}\nFileUniqueId: {message.document.file_unique_id}\nFileSize: {message.document.file_size} B\nFileType: {message.document.mime_type}"
        bot.send_document(chat_id, data, caption=caption) # return data
    
    elif message.content_type == "voice":
        data = message.voice.file_id # get voice data
        caption = f"FileUniqueId: {message.voice.file_unique_id}\nFileSize: {message.voice.file_size}\nFileType: {message.voice.mime_type}"
        bot.send_voice(chat_id, data, caption=caption) # return data
    
    elif message.content_type == "sticker":
        data = message.sticker.file_id # get sticker data
        print(message.sticker)
        caption = f"Setname: {message.sticker.set_name}\nFileSize: {message.sticker.file_size}\nType: {message.sticker.type}\nFileWidth: {message.sticker.width}\nFileHeight: {message.sticker.height}\nAnimation: {message.sticker.is_animated}\nFileEmoiji: {message.sticker.emoji}"
        bot.send_sticker(chat_id, data) # return data
        bot.send_message(chat_id, caption)
    
    elif message.content_type == "animation":
        data = message.animation.file_id # get animation video data (gif)
        caption = f"FileName: {message.animation.file_name}\nFileSize: {message.animation.file_size}\nDuration: {message.animation.duration}s\nFileHeight: {message.animation.height}\nFileWidth: {message.animation.width}"
        bot.send_animation(chat_id, data, caption=caption) # return data
    
    elif message.content_type == "video":
        data = message.video.file_id # get video id in telegram server
        caption = f"FileName: {message.video.file_name}\nFileSize: {message.video.file_size}kb\nDuration: {message.video.duration}s\nFileWidth: {message.video.width}\nFileHeight: {message.video.height}\nFileType: {message.video.mime_type}"
        bot.send_video(chat_id, data, caption=caption) # return data
    
    elif message.content_type == "audio":
        data = message.audio.file_id # get audio id in telegram server
        caption = f"FileName: {message.audio.file_name}\nFileSize: {message.audio.file_size}kb\nDuration: {message.audio.duration}s\nFileType: {message.audio.mime_type}\nTitle: {message.audio.title}\nPerformer: {message.audio.performer}"
        bot.send_audio(chat_id, data, caption=caption) # return data
    
    

