from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def languages_list():
    """ languages list inline murkup buttons """
    langs=[
        [{"Uz-Ru": "uz_ru"}, {"Uz-En": "uz_en"}, {"Uz-Fr": "uz_fr"}],
        [{"Ru-Uz": "ru_uz"}, {"Ru-En": "ru_en"}, {"Ru-Fr": "ru_fr"}],
        [{"En-Uz": "en_uz"}, {"En-Ru": "en_ru"}, {"En-Fr": "en_fr"}],
        [{"Fr-Uz": "fr_uz"}, {"Fr-Ru": "fr_ru"}, {"Fr-En": "fr_en"}]
    ]
    murkub = InlineKeyboardMarkup()
    for l in langs:
        murkub.row(*[InlineKeyboardButton(n, callback_data=i[n]) for i in l for n in i])
    return murkub