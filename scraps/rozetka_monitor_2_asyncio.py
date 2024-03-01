import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape_and_write_data(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    products = soup.find_all(class_='goods-tile__inner')

    items = []
    for product in products:
        title = product.find(class_='goods-tile__title').get_text(strip=True)
        price = product.find(class_='goods-tile__price-value').get_text(strip=True)
        items.append(f'{title}: {price}\n')
    return items


async def get_urls(n):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    tasks = []
    async with aiohttp.ClientSession() as session:
        for page_num in range(1, n):
            url = f'https://rozetka.com.ua/ua/all-tv/c80037/page={page_num}/'
            tasks.append(fetch(session, url))
        return await asyncio.gather(*tasks)


async def main():
    n = 50
    pages = await get_urls(n + 1)
    all_items = []
    for page_content in pages:
        items = await scrape_and_write_data(page_content)
        all_items.extend(items)

    with open("rozetka_monitor_2_asyncio.txt", "a", encoding="utf-8") as file:
        file.writelines(all_items)


asyncio.run(main())
