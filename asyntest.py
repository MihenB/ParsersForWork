# from parse_package.multypurpose_parser import ScrapSession
from config.request_config import cookies, headers
import asyncio
from bs4 import BeautifulSoup
import time
from aiocfscrape import CloudflareScraper

link_root = 'https://kompromat1.pro'


def write_to_txt(data):
    with open('links.txt', 'w') as file:
        for link in data:
            file.writelines(link + '\n')


async def get(num, session: CloudflareScraper, file):
    # session = cfscrape.create_scraper(sess=session)
    params = {
        'pg': str(num),
    }
    # session = cfscrape.create_scraper(session)
    resp = await session.get('https://kompromat1.pro/articles', params=params, cookies=cookies, headers=headers)
    # resp = await session.get('https://google.com', headers=headers)
    resp = BeautifulSoup(await resp.text(), 'lxml')
    cards = resp.find_all('a', class_='articles_title')
    print(num)
    for card in cards:
        link = card.get('href')
        file.write(f'{link_root}{link}\n')
    # await asyncio.sleep(0)


async def get_links():
    # data = []
    async with CloudflareScraper() as session:
        with open('links.txt', 'a', encoding='utf-8') as file:
            tasks = [asyncio.create_task(get(num_of_page, session, file))
                     for num_of_page in range(1000, 14193)]
    # for num_of_page in range(1000, 14193):
    #     # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #     data += asyncio.run(get(num_of_page))
    #     # print(len(data))
    #     print(num_of_page + 1)
    # return data
            await asyncio.gather(*tasks)


async def main():
    str_time = time.time()
    await get_links()
    # print(len(data))
    # write_to_txt(data)
    end_time = time.time() - str_time
    print(f'Execution time: {end_time}')


if __name__ == '__main__':
    asyncio.run(main())
