from parse_package.multypurpose_parser import ScrapSession
from config import cookies, headers
import requests
from bs4 import BeautifulSoup
import cfscrape

proxy = {
    'protocol': 'https',
    'login': 'A8qRAN',
    'password': 'qx6CEk',
    'ip': '104.227.102.174',
    'port': '9400'
}


def get_info_from_site(url, session, photo_path):
    response = session.get(url=url, cookies=cookies, headers=headers, proxies=proxy)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h1').text
    photo_link = soup.find('img').get('src')
    try:
        text = soup.find('div', class_='articles_one k1_exy2xy1axay').text.strip()
        picture = session.get(url=photo_link, headers=headers, cookies=cookies)
        tags = soup.find_all('a', class_='article-tag')
        names_of_tags = ''
        date = soup.find('div', class_='img_div').text.strip('\n\n')[0].replace('\n', '')
        for tag in tags:
            names_of_tags += '|' + tag.get('href')
        out = open(f'{photo_path}/{title}.jpg', "wb")
        out.write(picture.content)
        out.close()

        data = {
            'title': title,
            'photo_path': f'{photo_path}/{title}.jpg',
            'text': text,
            'tags': names_of_tags,
            'date': date
        }
    except AttributeError:
        data = {}
    return data


def main():
    with open('links1.txt', 'r', encoding='UTF-8') as file:
        for link in file.readlines():
            session = cfscrape.create_scraper(requests.session())
            data = get_info_from_site(link, session, 'photos1')
            print(data)


if __name__ == '__main__':
    main()
