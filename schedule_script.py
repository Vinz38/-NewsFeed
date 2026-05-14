from random import shuffle
from bs4 import BeautifulSoup
import requests

TYPE_NEWS = ['technology_and_media', 'sport', 'economics', 'finances', 'politics']


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
    return news_list


def get_news(href, par):
    news_doc = requests.get(url=href, timeout=(5, 10)).content.decode('utf-8')
    soup = BeautifulSoup(news_doc, 'html.parser')
    if par == "title":
        title = soup.head.title.text.upper()
        return title
    elif par == "text":
        text = soup.find('meta', {'itemprop': 'articleBody'})['content']
        return text


def get_links(user_id):
    gl_list = []
    for i in requests.get('http://127.0.0.1:5000/api/user/category/{}'.format(user_id)).json()['category']:
        news_resp = requests.get('http://127.0.0.1:5000/api/news/{}'.format(i)).json()
        for x in news_resp['news']:
            if len(gl_list) < 15:
                gl_list.append(x['link_news'])
            else:
                break
    shuffle(gl_list)
    return gl_list


def get_text_and_links(user_id):
    itog = []
    for link in get_links(user_id):
        itog.append((get_news(link, "title"), link))
    return itog

def main():
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


if __name__ == "__main__":
    main()
