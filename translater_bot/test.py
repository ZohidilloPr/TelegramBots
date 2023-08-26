langs=[
    [{"Uz-Ru": "uz_ru"}, {"Uz-En": "uz_en"}, {"Uz-Fr": "uz_fr"}],
    [{"Ru-Uz": "ru_uz"}, {"Ru-En": "ru_en"}, {"Ru-Fr": "ru_fr"}],
    [{"En-Uz": "en_uz"}, {"En-Ru": "en_ru"}, {"En-Fr": "en_fr"}],
    [{"Fr-Uz": "fr_uz"}, {"Fr-Ru": "fr_ru"}, {"Fr-En": "fr_en"}]
]
# print(langs)

# for l in langs:
#     for i in l:
#         for k in i:
#             print(k, i[k])

# row = [i.keys() for l in langs for i in l]

# print(row)

# for l in langs:
#     print([[n, i[n]] for i in l for n in i])

# for l in langs:
#     print([i[v] for i in l for v in i])

import wikipedia

wikipedia.set_lang("uz")
respond = input("savolni yoz: ")
try:
    print(wikipedia.summary(respond))
except:
    print(respond, "Mazgi bunaqa narsa yoq :)")