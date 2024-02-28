from bs4 import BeautifulSoup
import requests


def scrape_and_write_data(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    products = soup.find_all(class_='goods-tile__inner')

    with open("rozetka_monitor.txt", "a", encoding="utf-8") as file:
        for product in products:
            title = product.find(class_='goods-tile__title').get_text(strip=True)
            price = product.find(class_='goods-tile__price-value').get_text(strip=True)
            file.write(f'{title}: {price}\n')


def get_url(n):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    for page_num in range(1, n):
        url = f'https://rozetka.com.ua/ua/all-tv/c80037/page={page_num}/'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            page_content = response.content
            scrape_and_write_data(page_content)
        else:
            print(f'Failed to fetch page {page_num}')


# Количество прогонов страниц (n + 1) можно передать в get_url, столько будет прогонов
n = 5
get_url(n + 1)
