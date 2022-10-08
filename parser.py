from parse_package.multypurpose_parser import ScrapSession
from config import cookies, headers
link_root = 'https://kompromat1.pro'


def get_links():
    with open('links1.txt', 'a') as file:
        for num_of_page in range(100, 200):
            session = ScrapSession()
            params = {
                'pg': str(num_of_page),
            }
            res = session.get('https://kompromat1.pro/articles', params=params, cookies=cookies, headers=headers
                              , proxies=True, secured=True).soup
            cards = res.find_all('a', class_='articles_title')
            for card in cards:
                link = card.get('href')
                file.write(f'{link_root}{link}\n')
            print(f'Page {num_of_page}')


def main():
    get_links()


if __name__ == '__main__':
    main()