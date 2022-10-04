import time
import aiohttp
import asyncio
import cfscrape
import requests
from parse_package.multypurpose_parser import ScrapSession
from config import cookies, headers, url
from bs4 import BeautifulSoup


async def get_page(num_of_page):
    async with aiohttp.ClientSession() as session:
        session = cfscrape.create_scraper(session)
        # session = cfscrape.create_scraper(sess=requests.Session())
        response = session.get(url=url,
                               cookies=cookies,
                               headers=headers)
        data = []
        data.append(response)
        await asyncio.sleep(1)
        return data
    # data = []
    # session = ScrapSession()
    # response = session.get('https://kompromat1.pro/articles?pg=' + str(num_of_page), proxies=True, cookies=cookies
    #                        , headers=headers
    #                        , secured=True).soup
    # soup = response
    # links = soup.find_all('a', class_='articles_title')
    # for link in links:
    #     data.append(link.get('href'))
    # return data


async def get_data():
    session = ScrapSession()
    for i in range(785):
        # response = session.get('https://kompromat1.pro/articles/deputies?pg='+str(i), proxies=True, cookies=cookies
        #                        , headers=headers
        #                        , secured=True).soup
        # titles = response.find_all('a', class_='articles_title')
        # for title in titles:
        #     data.append(title.text.strip())
        print(await get_page(i))


async def main():
    await get_data()


if __name__ == '__main__':
    asyncio.run(main())
