import csv

import requests
from bs4 import BeautifulSoup

from scraps.model import Product

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
}


def parser(url: str, max_item: int):
    create_cvs()

    page = 1
    count_items = 0
    while max_item > count_items:

        list_product = []
        res = requests.get(f'{url}&p={page}', headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        products = soup.find_all('div', class_='list-item list-item--row')

        for product in products:
            if count_items >= max_item:
                break
            count_items += 1
            name = product.find('a', class_='item-title text-md link link--black').text.strip()
            link = 'https://hotline.ua' + product.find('a', class_='list-item__img').get('href')
            price = product.find('div', class_="list-item__value-price text-md text-orange text-lh--1").text.strip()
            list_product.append(Product(name=name, link=link, price=price))
        write_cvs(list_product)
        page += 1


def create_cvs():
    with open(f'hotline_va.csv', mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'name', 'link', 'price'
        ])


def write_cvs(products: list[Product]):
    with open(f'hotline_va.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        for product in products:
            writer.writerow([
                product.name, product.link, product.price
            ])


if __name__ == '__main__':
    parser(url='https://hotline.ua/ua/computer/videokarty/', max_item=1325)
