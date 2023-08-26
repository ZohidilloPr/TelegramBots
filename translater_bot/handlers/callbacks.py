from telebot.types import CallbackQuery


from bot import bot
from states import TranslaterState


langs = ['uz_ru', 'uz_en', 'uz_fr',  \
         'ru_uz', 'ru_en', 'ru_fr',  \
         'en_uz', 'en_ru', 'en_fr',  \
         'fr_uz', 'fr_ru', 'fr_en'   ]


@bot.callback_query_handler(func=lambda call: call.data in langs)
def reaction_call(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    from_lang, to_lang = call.data.split('_')
    bot.set_state(user_id, TranslaterState.word, chat_id)
    with bot.retrieve_data(user_id, chat_id) as data:
        data['from_lang'], data['to_lang'] = from_lang, to_lang
    bot.delete_message(chat_id, call.message.id)
    text = "!"
    if from_lang == 'uz':
        text = "So'z kiriting"
    elif from_lang == 'ru':
        text = "Введите слово"
    elif from_lang == 'en':
        text = "Input your word"

    bot.send_message(chat_id, text)

