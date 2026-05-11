from bs4 import BeautifulSoup
import requests

TYPE_NEWS = ['technology_and_media', 'sport', 'economics', 'finances', 'politics', 'films']


def get_list_link_news(type_news):
    news_list = []
    session = requests.Session()
    html_doc = session.get(url=f"https://www.rbc.ru/rubric/{type_news}/").content.decode('utf-8')
    soup = BeautifulSoup(html_doc, 'html.parser')
    links = soup.find_all('div', class_='material-card')
    if type_news == "films":
        pass
    for i in links:
        link = i.get('data-metronome-href')
        if link:
            news_list.append(link)
            """
            news_doc = session.get(url=link).content.decode('utf-8')
            soup2 = BeautifulSoup(news_doc, 'html.parser')
            title = soup2.head.title.text.upper()
            text = soup2.find('meta', {'itemprop': 'articleBody'})['content']
            news_list.extend((count, title, text))
            """
    return news_list


if __name__ == "__main__":
    for a in TYPE_NEWS:
        for i in get_list_link_news(a):
            resp = requests.post('http://127.0.0.1:5000/api/news/{}'.format(a), json={
                "categories": a,
                "link_news": i,
            })
            if resp.status_code != 200:
                print(f"Ошибка {resp.status_code}: {resp.text}")
            else:
                print(f"Добавлено: {i}")
