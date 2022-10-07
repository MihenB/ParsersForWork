from parse_package.multypurpose_parser import ScrapSession
from config import cookies, headers


def get_info_from_site(url, session):
    soup = session.get(url=url, cookies=cookies, headers=headers, secured=True).soup
    title = soup.find('h1').text
    photo_link = soup.find('img').get('src')
    text = soup.find('div', class_='articles_one k1_exy2xy1axay').text.strip()
    # tags =
    data = {
        'title': title,
        'photo_link': photo_link,
        'text': text
    }
    return data


def main():
    session = ScrapSession()
    link = 'https://kompromat1.pro/articles/216592-repera_pashu_tehnika_gospitalizirovali_v_botkinskuju_boljnitsu'
    data = get_info_from_site(link, session)
    print(data)


if __name__ == '__main__':
    main()
