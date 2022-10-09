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


def get_number_of_month(month):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
             'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    if month in months:
        number_of_month = months.index(month) + 1
        if number_of_month < 10:
            return f'{0}{number_of_month}'
        else:
            return f'{number_of_month}'


def format_tags(tags):
    f_tags = ''
    tags = tags.split('|')
    for i in range(1, len(tags)):
        name_tag = tags[i].split('/')[3]
        f_tags += f'|{name_tag}'
    return f_tags


def format_text(text):
    text = text.split('\n\n\n\n\n\n\n\n')[1]
    return text


def get_info_from_site(url, session, photo_path, count):
    response = session.get(url=url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h1').text
    photo_link = soup.find('img').get('src')
    text = format_text(soup.find('div', class_='articles_one').text.strip())
    picture = session.get(url=photo_link, headers=headers, cookies=cookies)
    tags = soup.find_all('a', class_='article-tag')
    names_of_tags = ''
    date = soup.find('div', class_='img_div').text.replace('\n', '').split('г.')[0].split(' ')
    date = f'{date[1]}.{get_number_of_month(date[2])}.{date[3]}'
    for tag in tags:
        names_of_tags += '|' + tag.get('href')
    names_of_tags = format_tags(names_of_tags)
    with open(f'{photo_path}/{count}.jpg', "wb") as file:
        file.write(picture.content)
    data = {
        'title': title,
        'photo_path': f'{photo_path}/{count}.jpg',
        'text': text,
        'tags': names_of_tags,
        'date': date
    }
    return data


def main():
    with open('links1.txt', 'r', encoding='UTF-8') as file:
        count = 0
        for link in file.readlines():
            session = cfscrape.create_scraper(requests.session())
            data = get_info_from_site(link, session, 'photos1', count)
            count += 1
            print(data)
            #print(data.get('text'))


if __name__ == '__main__':
    main()
