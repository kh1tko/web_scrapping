from bs4 import BeautifulSoup
import requests
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def get_url():
    for count in range(1, 2):
        url = f'https://scrapingclub.com/exercise/list_basic/?page={count}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')  # html.parser
        data = soup.find_all('div', class_='w-full rounded border')
        for i in data:
            card_url = 'https://scrapingclub.com' + i.find('a').get('href')
            yield card_url


all_items = []
for card_url in get_url():
    response = requests.get(card_url, headers=headers)
    sleep(3)
    soup = BeautifulSoup(response.text, 'html.parser')  # html.parser
    data = soup.find('div', class_='my-8 w-full rounded border')
    name = soup.find('h3', class_='card-title').text
    price = soup.find('h4', class_='my-4 card-price').text
    text = soup.find('p', class_='card-description').text
    url_img = 'https://scrapingclub.com' + soup.find('img', class_='card-img-top').get('src')
    string_ = f'{name}\n{price}\n{text}\n{url_img}\n\n'
    all_items.append(string_)
with open("scrap_club.txt", "w", encoding="utf-8") as file:
    file.writelines(all_items)
