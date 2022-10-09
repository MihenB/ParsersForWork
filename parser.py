import requests
from bs4 import BeautifulSoup
from config.request_config import cookies, headers, url


def get_links():
    with open('links1.txt', 'a') as file:
        for num_of_page in range(100, 200):
            session = requests.Session()
            params = {
                'pg': str(num_of_page),
            }
            res = session.get(url=url,
                              params=params,
                              cookies=cookies,
                              headers=headers).text
            res = BeautifulSoup(res, 'lxml')
            cards = res.find_all('a', class_='articles_title')
            for card in cards:
                link = card.get('href')
                file.write(f'{url}{link}\n')
            print(f'Page {num_of_page}')


def main():
    get_links()


if __name__ == '__main__':
    main()
