import json
import requests
from bs4 import BeautifulSoup

class BaseParser:
    def __init__(self, category):
        self.URL = 'https://upg.uz/ru/categories/'
        self.host = 'https://upg.uz'
        self.category = category

    def get_soup(self):
        req = requests.get(self.URL + self.category)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')
            return soup
        else:
            print('Xato!!!')


    def save_json(self, data):
        with open(f"{self.category}.json", mode='w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

