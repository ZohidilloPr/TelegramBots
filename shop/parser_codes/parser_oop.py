from .base_parser import *
from loader import db

class UPGParser(BaseParser):

    def get_data(self):
        soup = self.get_soup()
        box = soup.find('div', class_='row-viewed col-catalog-grid product-grid')
        data = []
        products = box.find_all('div', class_='col-lg-12 col-md-15 col-sm-20 col-xs-30 item-product')

        category_name = ''
        if self.category == 'kategory-mouses':
            category_name = 'Sichqonchalar 🖱'
        elif self.category == 'kategory-noutbuki':
            category_name = 'Noutbuklar 💻'
        elif self.category == 'kategory-klaviaturi':
            category_name = 'Klaviaturalar ⌨️'
        elif self.category == 'kategory-naushniki':
            category_name = 'Quloqchinlar 🎧'

        category_id = db.get_category_id_by_category(category_name)

        for product in products:
            mini_box = product.find('div', class_='item-product-inner')
            title = mini_box.find('a').get_text(strip=True)
            link = mini_box.find('a')['href']
            image = 'https://upg.uz' + mini_box.find('img')['src']
            price = int(mini_box.find('span', class_='item-price price-new').get_text(strip=True).replace(' ', '').replace('сум', ''))

            data.append({
                'product_name': title,
                'link': link,
                'image': image,
                'price': price,
                'category_id': category_id
            })

        return data


