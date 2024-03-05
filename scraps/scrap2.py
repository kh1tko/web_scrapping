import asyncio
import aiohttp
from bs4 import BeautifulSoup
from time import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


async def fetch_url(session, url):
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def scrape_and_write_data(session, url):
    page_content = await fetch_url(session, url)
    soup = BeautifulSoup(page_content, 'html.parser')
    data = soup.find_all('div', class_='w-full rounded border')
    items = []
    for item in data:
        card_url = 'https://scrapingclub.com' + item.find('a').get('href')
        item_content = await fetch_url(session, card_url)
        item_soup = BeautifulSoup(item_content, 'html.parser')
        name = item_soup.find('h3', class_='card-title').text
        price = item_soup.find('h4', class_='my-4 card-price').text
        text = item_soup.find('p', class_='card-description').text
        url_img = 'https://scrapingclub.com' + item_soup.find('img', class_='card-img-top').get('src')
        items.append(f'{name}\n{price}\n{text}\n{url_img}\n\n')
    return items


async def main():
    start_time = time()
    urls = [f'https://scrapingclub.com/exercise/list_basic/?page={page}' for page in range(1, 6)]
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_and_write_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        all_items = [item for sublist in results for item in sublist]
    with open("scrap_club_2.txt", "w", encoding="utf-8") as file:
        file.writelines(all_items)
    print(f"Scraping completed in {time() - start_time} seconds")


asyncio.run(main())
