import requests
test_list = [
    '|34553|345354|35|34364',
    '|345',
    '|3465|3453'
]
test_list_titles = [
    'first',
    'second',
    'bob'
]


def format_list_to_dict(list_of_links, list_of_titles):
    result_dict = {}
    for i in range(len(list_of_links)):
        one_page_links = []
        for link in list_of_links[i].split('|')[1::]:
            one_page_links.append(link)
        result_dict[list_of_titles[i]] = one_page_links
    return result_dict


def main():
    print(format_list_to_dict(test_list, test_list_titles))


if __name__ == '__main__':
    main()



