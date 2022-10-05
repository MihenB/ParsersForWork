from parse_package.multypurpose_parser import ScrapSession
from config import cookies, headers
link_root = 'https://kompromat1.pro'


def get_links():
    for num_of_page in range(10):
        session = ScrapSession()
        params = {
            'pg': str(num_of_page),
        }
        res = session.get('https://kompromat1.pro/articles', params=params, cookies=cookies, headers=headers
                          , proxies=False).soup
        cards = res.find_all('a', class_='articles_title')
        for card in cards:
            link = card.get('href')
            print(link_root + link)


def main():
    get_links()


if __name__ == '__main__':
    main()
