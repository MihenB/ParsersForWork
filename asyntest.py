from parse_package.multypurpose_parser import ScrapSession
from config import cookies, headers
link_root = 'https://kompromat1.pro'
import asyncio
import cfscrape
import aiohttp
from bs4 import BeautifulSoup
import time

def write_to_txt(data):
    with open('links.txt', 'w') as file:
        for link in data:
            file.writelines(link +'\n')


async def get(num):
    data = []
    async with aiohttp.ClientSession() as session:
        params = {
            'pg': str(num),
        }
        session = cfscrape.create_scraper(session)
        resp = session.get('https://kompromat1.pro/articles', params=params, cookies=cookies, headers=headers)
        resp = BeautifulSoup(resp.text, 'lxml')
        cards = resp.find_all('a', class_='articles_title')
        for card in cards:
            link = card.get('href')
            data.append(link_root + link)
        #await asyncio.sleep(0)
    return data


def get_links():
    data = []
    for num_of_page in range(1000, 14193):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        data += asyncio.run(get(num_of_page))
        #print(len(data))
        print(num_of_page + 1)
    return data


def main():
    str_time = time.time()
    data = get_links()
    print(len(data))
    write_to_txt(data)
    end_time = time.time() - str_time
    print(end_time)


if __name__ == '__main__':
    main()
