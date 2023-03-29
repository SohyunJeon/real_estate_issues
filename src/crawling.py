# %% Package Load

import time
import re
import requests
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime
from random import randint
import xml.etree.ElementTree as ET
import json
import pickle

import os
import re
from konlpy.tag import Twitter
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from PIL import Image
import numpy as np


# %% 동작구 기사 url 수집


def crawlling_article_urls(base_url, article_page):
    # base_url = 'https://land.naver.com/news/region.nhn?city_no=1100000000&dvsn_no=1159000000'
    add_url = 'https://land.naver.com'
    max_sec = 15
    # https://land.naver.com/news/newsRead.nhn?type=region&prsco_id=018&arti_id=0004896067

    class_regex = re.compile('NP=r:\d{1,2}i:+')
    article_url_list = []
    for page in range(1, article_page + 1):
        page_url = base_url + f'&page={page}'
        r = requests.get(page_url)

        html = r.text
        soup = bs(html)
        html_elem_list = soup.find_all('dt')
        for html_elem in html_elem_list:
            try:
                elem = html_elem.select('a')[0]['href']
                article_url_list.append(elem)
            except:
                pass

        rand_value = randint(1, max_sec)
        print('sleep time : ', rand_value)
        time.sleep(rand_value)

    article_url_list = [add_url + url for url in article_url_list]
    article_url_list = list(set(article_url_list))  # remove duplication

    return article_url_list


# %% 추출한 url에서  기사 수집

def crawlling_articles_with_url_list(article_url_list):
    max_sec = 15
    remove_pattern = '[a-zA-Z/><()=\"\'._:!-]'
    print(f'Total url count : {len(article_url_list)}')
    article_list = []
    for idx, url in enumerate(article_url_list):
        print(idx)
        r = requests.get(url)
        html = r.text
        soup = bs(html)
        raw_article = soup.find_all('div', attrs={'class': 'article_body size4',
                                                  'id': 'articleBody'})

        if len(raw_article) > 0:
            article_list.append(str(raw_article[0]))

            rand_value = randint(1, max_sec)
            print('sleep time : ', rand_value)
            time.sleep(rand_value)

    return article_list


# %% 크롤링
def crawlling(base_url, page):
    article_url_list = crawlling_article_urls(base_url, page)
    raw_articles = crawlling_articles_with_url_list(article_url_list)

    articles = list(map(lambda x: extract_pure_article(x), raw_articles))

    return articles


# %% 수집 기사 원본 전처리
def extract_pure_article(article):
    cleaner1 = re.compile('<.*?>')
    cleaned1 = re.sub(cleaner1, '', article)

    cleaner2 = re.compile('\\\t|\\\s|\\\n')
    cleaned2 = re.sub(cleaner2, '', cleaned1)

    cleaner3 = re.compile('[a-zA-Z가-힣]@[a-zA-Z]')
    cleaned3 = cleaner3.split(cleaned2)[0]

    return cleaned3




#%% Main
if __name__ == '__main__':
    ## remove stopwords
    data_base_dir = './data'
    stop_words_file= 'korean_stopwords.txt'

    with open(os.path.join(data_base_dir, stop_words_file), 'r', encoding='utf-8') as f:
        stopwords = f.readlines()
    stopwords = [x.replace('\n','') for x in stopwords]

    addtional = ['기자', '이데일리', '언론','언론사', '도시', '주택', '계획', '사업',
                 '일대', '지역', '추진','주민','시설', '구역', '가구','고','위','층',
                 '말']
    stopwords = stopwords + addtional

    ### 1. 동작구
    ## Crawlling
    url_Gu1 = 'https://land.naver.com/news/region.nhn?city_no=1100000000&dvsn_no=1159000000'
    Gu1_articles = crawlling(url_Gu1, 4)
    # save pickle
    with open(os.path.join(data_base_dir, 'dongjack_article.pkl'), 'wb') as pk:
        pickle.dump(Gu1_articles, pk)

    ### 2. 영등포구
    ## Crawlling
    url_Gu2 = 'https://land.naver.com/news/region.nhn?city_no=1100000000&dvsn_no=1156000000'
    Gu2_articles = crawlling(url_Gu2, 8)

    with open(os.path.join(data_base_dir, 'yeongdeungpo_article.pkl'), 'wb') as pk:
        pickle.dump(Gu2_articles, pk)