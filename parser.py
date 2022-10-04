import time

from parse_package.multypurpose_parser import ScrapSession
from config import cookies, headers


def get_data():
    data = []
    session = ScrapSession()
    for i in range(785):
        response = session.get('https://kompromat1.pro/articles/deputies?pg='+str(i), proxies=True, cookies=cookies
                               , headers=headers
                               , secured=True).soup
        titles = response.find_all('a', class_='articles_title')
        for title in titles:
            data.append(title.text.strip())
    return data


def main():
    data = get_data()
    print(len(data))


if __name__ == '__main__':
    main()
