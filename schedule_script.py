from bs4 import BeautifulSoup
import requests

TYPE_NEWS = ['technology_and_media', 'sport', 'economics', 'finances', 'politics']


def get_list_news(type_news):
    session = requests.Session()
    html_doc = session.get(url=f"https://www.rbc.ru/rubric/{type_news}/").content.decode('utf-8')
    soup = BeautifulSoup(html_doc, 'html.parser')
    links = soup.find_all('div', class_='material-card')
    news_list = []
    count = 0
    for i in links:
        link = i.get('data-metronome-href')
        if link:
            news_doc = session.get(url=link).content.decode('utf-8')
            soup2 = BeautifulSoup(news_doc, 'html.parser')
            count += 1
            title = soup2.head.title.text.upper()
            text = soup2.find('meta', {'itemprop': 'articleBody'})['content']
            news_list.extend((count, title, text))
    return news_list


a = input()
if a in TYPE_NEWS:
    for i in get_list_news(a):
        print(i)
