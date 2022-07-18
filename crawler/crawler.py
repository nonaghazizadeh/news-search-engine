import json
import os

import requests
from bs4 import BeautifulSoup
import lxml

DIR_NAME = 'news'
os.makedirs(DIR_NAME, exist_ok=True)

BASE_URL = "https://www.hamshahrionline.ir"
POSTFIX_URL = "/page/archive.xhtml?wide=0&ms=0&"
SUBJECTS_DICT = {6: 'سیاسی', 11: 'جهان', 10: 'اقتصاد', 5: 'جامعه', 7: 'شهر', 21: 'زندگی', 580: 'محله',
               718: 'فناوری اطلاعات', 20: 'دانش', 26: 'فرهنگ و هنر', 9: 'ورزش'}

data = {}

TOTAL_PAGES = 50
idx = 0
for k, v in SUBJECTS_DICT.items():
    for page_num in range(1, TOTAL_PAGES + 1):
        all_news_links = []

        url = f"{BASE_URL}{POSTFIX_URL}pi={page_num}&tp={k}"
        f = requests.get(url)
        soup = BeautifulSoup(f.content, 'lxml')
        all_news = soup.find('div', {'id': 'mainbody'}).findAll('div', {'class': 'desc'})

        for news in all_news:
            all_news_links.append(news.findAll('h3'))

        for news_link in all_news_links:
            title = news_link[0].find('a').text
            link = news_link[0].find('a')['href']

            per_url = BASE_URL + link
            per_f = requests.get(per_url)
            per_soup = BeautifulSoup(per_f.content, 'lxml')

            try:
                texts = per_soup.find('div', {"itemprop": "articleBody"}).findAll('p')
            except Exception as e:
                continue

            content = ""
            for text in texts:
                content += text.text
            if content != "":
                data[idx] = {'title': title, 'subject': v, 'content': content}
                idx += 1

        print(f"crawling page {page_num} of subject {v} done.")

with open(f"{DIR_NAME}/news.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)

