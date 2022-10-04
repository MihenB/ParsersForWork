import time
import aiohttp
import asyncio
import cfscrape
from parse_package.multypurpose_parser import ScrapSession
from config import cookies, headers, url
from bs4 import BeautifulSoup


def get_page(num_of_page):
    data = []
    session = ScrapSession()
    response = session.get('https://kompromat1.pro/articles?pg=' + str(num_of_page), proxies=True, cookies=cookies
                           , headers=headers
                           , secured=True).soup
    soup = response
    links = soup.find_all('a', class_='articles_title')
    for link in links:
        data.append(link.get('href'))
    return data


def get_data():
    for i in range(785):
        # response = session.get('https://kompromat1.pro/articles/deputies?pg='+str(i), proxies=True, cookies=cookies
        #                        , headers=headers
        #                        , secured=True).soup
        # titles = response.find_all('a', class_='articles_title')
        # for title in titles:
        #     data.append(title.text.strip())
        print(get_page(i))


def main():
    get_data()


if __name__ == '__main__':
    main()
