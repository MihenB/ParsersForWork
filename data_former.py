from parse_package.multypurpose_parser import ScrapSession
from config import cookies, headers
link_root = 'https://kompromat1.pro'
import asyncio
import cfscrape
import aiohttp
from bs4 import BeautifulSoup
import time


# async def get(url):
#     data = []
#     async with aiohttp.ClientSession() as session:
#         session = cfscrape.create_scraper(session)
#         resp = session.get(url, cookies=cookies, headers=headers)
#         resp = BeautifulSoup(resp.text, 'lxml')
#         article = resp.find_all('a', class_='articles_title')
#
#     return data
#
#
# def get_links():
#     data = []
#     for num_of_page in range(1000, 14193):
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#         data += asyncio.run(get(num_of_page))
#         #print(len(data))
#         print(num_of_page + 1)
#     return data
#
#
# def main():
#     str_time = time.time()
#     data = get_links()
#     print(len(data))
#     write_to_txt(data)
#     end_time = time.time() - str_time
#     print(end_time)
#
#
# if __name__ == '__main__':
#     main()
