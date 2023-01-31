
import requests as req
import fake_headers as fh
from bs4 import BeautifulSoup
import re


KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'терагерц', 'ChatGPT']
HOST = "https://habr.com/ru/all"
headers = fh.Headers(os="win", browser="opera").generate()


response = req.get(HOST, headers=headers)
soap = BeautifulSoup(response.text, "lxml")

articles_list = soap.find_all("article", class_="tm-articles-list__item")

print("Articles total:", len(articles_list))

result_list = []

for article in articles_list:
    article_body = article.find("div", class_="article-formatted-body")
    for keyword in KEYWORDS:
        if keyword.lower() in str(article_body.text).lower():
            publish_datetime = article.find("span", class_="tm-article-snippet__datetime-published").find("time")['datetime']
            article_title = article.find("a", class_="tm-article-snippet__title-link").find("span").text
            article_link = HOST + article.find("a", class_="tm-article-snippet__title-link")['href']
            result_list.append({'publish_datetime': publish_datetime, 'article_title' : article_title, "article_link": article_link})
            break
    # articles loop

for x in result_list:
    x['publish_datetime'] = re.sub(R"\..*", "", x['publish_datetime'])
    x['publish_datetime'] = re.sub(R"T", " ", x['publish_datetime'])
    print("Дата:", x['publish_datetime'], "Заголовок:", x['article_title'], 'Ссылка:', x['article_link'])
            

