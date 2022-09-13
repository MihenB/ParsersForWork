from ParsersForWork.parse_package.multypurpose_parser import ScrapSession
from config import cookies, headers
from selenium.webdriver.common.action_chains import ActionChains
import time
import json


def write_to_json(data):
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    with open('result_data.json', 'w') as file:
        file.write(json_data)


def f(driver) -> None:
    actions = ActionChains(driver)
    element = driver.find_element('xpath', "/html/body/div[1]/header/div/div[2]/div[1]/button")
    actions.click(on_element=element)
    actions.perform()
    time.sleep(0.5)


def g(driver) -> None:
    actions = ActionChains(driver)
    element = driver.find_element('xpath', "/html/body/div[1]/main/div[2]/div/div[2]/div/div[2]/h1")
    actions.click(on_element=element)
    actions.perform()
    time.sleep(0.5)


def c(driver) -> None:
    actions = ActionChains(driver)
    element = driver.find_element('xpath', "/html/body/div[1]/main/div[2]/div/div[2]/div/div[1]/ul/li[1]/a")
    actions.click(on_element=element)
    actions.perform()
    time.sleep(0.5)


def get_subcategories(link):
    data = []
    session = ScrapSession()
    try:
        subcategories = session.render(link, secured=False, func=g).soup.find_all('a', class_='j-menu-item')
        for subcategory in subcategories:
            name_subcategory = subcategory.text.strip()
            link = subcategory.get('href')
            data.append({
                'name_subcategory': name_subcategory,
                'link': link
            })
    except AttributeError:
        try:
            subcategories = session.render(link, secured=False, func=c)\
                .soup.find_all('a')
            for subcategory in subcategories:
                name_subcategory = subcategory.text.strip()
                link = subcategory.get('href')
                data.append({
                    'name_subcategory': name_subcategory,
                    'link': link
                })
        except AttributeError:
            return data
    return data


def get_categories():
    i = 1
    data = []
    session = ScrapSession()
    categories = session.render('https://www.wildberries.ru/', secured=False, func=f)\
        .soup.find_all('li', class_="menu-burger__main-list-item j-men"
                                    "u-main-item menu-burger__main-list-item--subcategory")
    for category in categories:
        name_of_category = category.text.strip()
        link = category.find('a').get('href')
        subcategories = get_subcategories(link)
        data.append({
            'name_category': name_of_category,
            'link': link,
            'subcategories': subcategories
        })
        i += 1
        print(i)
    return data


def main():
    data = get_categories()
    print(data)
    write_to_json(data)


if __name__ == '__main__':
    main()