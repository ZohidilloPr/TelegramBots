import wikipedia
from translate import Translator
from telebot.types import Message, ReplyKeyboardRemove

from bot import bot
from keyboards.replayMarkup import start_btn
from keyboards.inlineMurkup import languages_list
from states import TranslaterState, WikipideaState


@bot.message_handler(regexp="Tarjima")
def reaction_translater(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Tilni tanlang", reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id, "Mavjud tillar", reply_markup=languages_list())


@bot.message_handler(content_types=['text'], state=TranslaterState.word)
def reaction_word(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        from_lang, to_lang = data['from_lang'], data['to_lang']
    word = message.text
    translated_word = Translator(from_lang=from_lang, to_lang=to_lang).translate(word)
    bot.send_message(chat_id, translated_word, reply_markup=start_btn())
    bot.delete_state(user_id, chat_id)


@bot.message_handler(regexp="Wikipidea")
def reaction_wiki(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, WikipideaState.word, chat_id)
    bot.send_message(chat_id, "Nimani qidirmoqchisiz", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=["text"], state=WikipideaState.word)
def reaction_wiki_word(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    wikipedia.set_lang("uz")
    print(message.text)
    try:
        bot.send_message(chat_id, wikipedia.summary(message.text), reply_markup=start_btn())
        bot.delete_state(user_id, chat_id)
    except Exception as e:
        bot.send_message(chat_id, "Siz soragan ma'lumot mavjud emas\nIltimos aniqroq yozing", reply_markup=start_btn())
        bot.delete_state(user_id, chat_id)
