from bs4 import BeautifulSoup
import requests
import os
import re
from time import sleep
from SS_processor import process_text


def get_links(url):
    print('url: {} is starting!'.format(url))
    res = requests.get(url);sleep(2)
    soup = BeautifulSoup(res.text, 'lxml')
    
    titles = soup.select('h2.article-title')
    links = [title.find('a').get('href') for title in titles]
    
    next_link = soup.select_one('li.paging-next').find('a').get('href')
    
    return links, next_link

def get_article(links, save_dir):
    for link in links:
        lines = list()
        number = os.path.basename(link).split('.')[0]
        print(number);sleep(2)
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'lxml')
        # for i in soup.select("br"):
        #     i.replace_with("\n")
        texts = soup.select_one('div.article-body-inner')
        texts = texts.select('div.main_txt')
        for text in texts:
            lines.extend(text.get_text('.').split('.'))
        texts = process_text(lines)
        if texts is not None:
            save_texts(texts, number, save_dir)

def save_texts(texts, number, save_dir):
    existed_files = os.listdir(save_dir)
    save_path = os.path.join(save_dir, number + '.txt')
    if not save_path in existed_files:
        with open(save_path, 'w') as f:
            f.write('\n'.join(texts))

def call(save_dir):
    url = 'http://blog.livedoor.jp/kokon55/'
    while True:
        links, next_link = get_links(url)
        
        get_article(links, save_dir)
        if next_link is not None:
            url = next_link
        else:
            break


if __name__ == '__main__':
    save_dir = None
    call(save_dir)