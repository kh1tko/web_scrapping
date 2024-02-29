from time import sleep

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'lxml')

movies = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-1364e729-0 caNpAE cli-parent')
data = []
for movie in movies:
    sleep(2)
    link = 'https://www.imdb.com/' + movie.find('a', class_='ipc-title-link-wrapper').get('href')
    name = movie.find('div', class_='sc-be6f1408-0 gVGktK cli-children').find('h3', class_='ipc-title__text').text.split('. ', 1)[1]
    year = movie.find('span', class_='sc-be6f1408-8 fcCUPU cli-title-metadata-item').text
    rate = movie.find('span',
                      class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating').text.split()
    print(name)
    data.append([link, name, year, rate[0]])

header = ['link,', 'name', 'year', 'rate']
df = pd.DataFrame(data, columns=header)
df.to_csv(r'data.cvs', sep=';', encoding='utf8')
