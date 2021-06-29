from bs4 import BeautifulSoup
import requests
import csv

CSV = 'kivano.csv'
HOST = 'https://www.kivano.kg/'
URL = 'https://www.kivano.kg/planshety-i-bukridery'
HEADERS = { 
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, verify=False, params=params)
    return r 

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='item product_listbox oh')
    news_list = []    
    for item in items:
        try:
            news_list.append({
                'price': item.find('div', class_='listbox_price text-center'), 
                'title': item.find('div', class_='item product_listbox oh'), 
                'link': HOST + item.find('div', class_='listbox_title oh').find('a').get('href'),})
        except:
            pass
    return news_list




def news_save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Цена', 'Описание', 'Ссылка', ])
        for item in items:
            writer.writerow([item['price'], item['title'], item['link']])

def parce():
    PAGENATOR = input('Введите количество страниц:')
    PAGENATOR = int(PAGENATOR.strip())
    html = get_html(URL)
    if html.status_code == 200:
        news_list = []
        for page in range(1, PAGENATOR):
            print(f'Страница{page} готова')
            html = get_html(URL, params={'page':page})
            news_list.extend(get_content(html.text))
            news_save(news_list, CSV)
            print('Парсинг готов!')
        else:
            print('Error')

parce()