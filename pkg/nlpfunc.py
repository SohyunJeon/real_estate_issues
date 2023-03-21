# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:31:17 2021

@author: sherr
"""

#%% Package import


from konlpy.tag import Twitter
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pprint as pp
import nltk



# %%  형태소 분석 및 명사 추출
def analyze_morph_extract_noun(text_list, stopwords):
    twitter = Twitter()

    morphs = []
    for text in text_list:
        morphs.append(twitter.pos(text))

    noun_adj_adv_list = []
    for sentense in morphs:
        for word, tag in sentense:
            if (tag in ['Noun']) and not (word in stopwords):
                noun_adj_adv_list.append(word)

    count = Counter(noun_adj_adv_list)
    word_dict = dict(count.most_common())

    return word_dict, noun_adj_adv_list



# %% 워드 클라우드 생성
def make_wordcloud(word_dict, mask, cloud_set):
    wordcloud = WordCloud(
        font_path=cloud_set['font_path'],
        background_color=cloud_set['background_color'],
        colormap=cloud_set['colormap'],
        width=cloud_set['width'],
        height=cloud_set['height'],
        mask=cloud_set['mask']
    )

    wordcloud_words = wordcloud.generate_from_frequencies(word_dict)

    array = wordcloud.to_array()

    plt.figure(figsize=(100, 80))
    plt.imshow(array, interpolation='bilinear')
    plt.axis('off')
    # plt.title('Word Cloud of Real Estate Articles')
    plt.show()


def check_count_pos(model_name, pos):
    text = nltk.Text(pos, name='NMSC')
    print('모델명: {}'.format(model_name))
    print("토큰의 개수 : {}".format(len(text.tokens)))
    print("unique 토큰의 개수 : {}".format(len(set(text.tokens))))
    print("상위 50개 빈도의 단어 : ")
    pp.pprint(text.vocab().most_common(50))

    print("Plot Chart")

    plt.figure(figsize=(20, 10))
    plt.rcParams.update({'font.size': 20})
    text.plot(50)