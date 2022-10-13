import json


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
    try:
        text = text.split('\n\n\n\n\n\n\n\n')[1]
    except IndexError:
        text = text
    return text


def write_to_json(data):
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    with open('result_data.json', 'a') as file:
        file.write(json_data)


def get_info_from_site(soup, primary_key):
    title = soup.find('h1').text
    text = format_text(soup.find('div', class_='articles_one').text.strip())
    tags = soup.find_all('a', class_='article-tag')
    names_of_tags = ''
    date = soup.find('div', class_='img_div').text.replace('\n', '').split('г.')[0].split(' ')
    date = f'{date[1]}.{get_number_of_month(date[2])}.{date[3]}'
    photos_links_soup = soup.find_all('img')
    photos_links = ''
    for photo_link in photos_links_soup:
        if 'logo?' not in photo_link.get('src') and 'https' in photo_link.get('src'):
            link_src = photo_link.get('src')
            photos_links += f'|{link_src}'
    for tag in tags:
        names_of_tags += '|' + tag.get('href')
    names_of_tags = format_tags(names_of_tags)
    data = {
        'title': title,
        'photos_links': photos_links,
        'text': text,
        'tags': names_of_tags,
        'date': date,
        'primary_key': primary_key
    }
    return data


def main():
    pass


if __name__ == '__main__':
    main()
