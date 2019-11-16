# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 15:41:11 2019

@author: nemow
"""

import pandas as pd 
from functools import reduce
import string
# from spellchecker import SpellChecker
# spell = SpellChecker()
import nltk
nltk.download('wordnet')
porter = nltk.stem.PorterStemmer()
import numpy as np
import re
pd.options.mode.chained_assignment = None
from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()
#nltk.download('wordnet')
import math

punctuation = '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~'
review = pd.read_csv(r'C:\Users\nemow\Documents\628_module3\cinema_review.csv')
def append(x,y):
    return x+y
def clean(x):
    return list(filter(lambda x: False if x in stop_words or x == '' else True, x))
def word_process(sentence):
    del_estr = punctuation
    replace = " "*len(del_estr)
    tran_tab = str.maketrans(del_estr, replace)
    sentence = sentence.translate(tran_tab).lower()
    return sentence


#word_process tanslete sentences to words
stop_words = pd.read_table(r"C:\Users\nemow\Documents\628_module3\stat-628-module3-master\data\stop_words.txt")
stop_words = list(stop_words["words"])



data = review['text']
review_text = review['text']
for i in range(len(data)):
    data[i] = word_process(data[i])
    temp = data[i].replace('\n', ' ').split(' ')
    comb = temp[0]
    for j in range(len(temp)):
        temp[j] = lem.lemmatize(temp[j], "v")
        if j > 0:
            comb = " ".join([comb,temp[j]])
    data[i] = comb



word = list(map(lambda x: x.replace('no ', 'no').replace('locate','location').replace('recline','recliner').replace('bathroom','restroom').replace('movie','film').replace('never ', 'never').replace('not ', 'not').replace("n't ", ' not').replace('nt ', ' not').replace('discou','discount').replace("n' ", " not").replace("should ","should").replace("would ", "would").replace('\n', ' ').split(' '), list(data)))
word1 = list(map(lambda x: x.replace('\n', ' ').split(' '), list(data)))
word_clean = list(map(clean, word))
word_dict = {}
review_list = review
review_list["text"] = pd.Series(word_clean)
for i in list(review.index.values):
    data = review.loc[i]
    if type(data["text"]) == float:
        continue
    count = 1+data['compliments']
    time = (np.array('2019-01-01', dtype=np.datetime64)-np.array(review_list.loc[i]["date"].split(" ")[0], dtype=np.datetime64)).astype(dtype=np.float32)
    time_weight = 3-(time/365) if (3-(time/365))  > 0 else 0
    for w in review_list.loc[i]["text"]:
        if not w in word_dict:
            word_dict[w] = 0
        word_dict[w] += count*(0.8+time_weight)

def word_dict_fx(key):
    return word_dict[key]
hp_word = sorted(list(word_dict.keys()), key=word_dict_fx, reverse = True)
hp_word_count = pd.Series(word_dict)[hp_word]

#import csv
#w = csv.writer(open(r"C:\Users\nemow\Documents\628_module3\words.csv", "w",encoding='utf-8'))
#for key, val in hp_word_count.items():
#    w.writerow([key, val])

price_word = ["ticket","price","cost","deal"]
location_word = ["location","hotel","car","park","restaurant"]
facility_word = ["facility","seat","place","chair","recliner","restroom","space","lobby","leather","screen","sound","3d","film","picture"]
envir_word = ["wait","time","experience","people","line","style","security","smell","table"]
food_word = ["drink","beverage","bar","snack","eat","water","soda","menu","beer"]
service_word = ["service","serve","server","order","employee","staff"]
promo_word = ["family","vip","pass","discount"]

for i in range(len(word)):
    
    













forward = {}
backward = {}
non = []
count = -1
for i in range(len(word_clean)):
    temp = word1[i]
    for j in range(len(temp)):
        if temp[j] in nouns:
            count = count+1
            non.append(temp[j])
            forward[count]=[]
            backward[count]=[]
            for k in range(j):
                if temp[j-k-1]!='':
                    forward[count].append(temp[j-k-1])
                else:
                    break
            for k in range(len(temp)-j-1):
                if temp[j+k+1]!='':
                    backward[count].append(temp[j+k+1])
                else:
                    break

non[1]
backward[1]
forward[1]
word1[1]


sentence = []
for i in range(len(non)):
    temp = []
    temp = ""
    for j in range(len(forward[i])):
        temp = " ".join([temp, forward[i][len(forward[i])-1-j]])
    temp = " ".join([temp,non[i]])
    for j in range(len(backward[i])):
        temp = " ".join([temp, backward[i][j]])
    sentence.append(temp)

from textblob import TextBlob
score = []
for i in range(len(sentence)):
    temp = TextBlob(sentence[i])
    score.append(temp.sentiment.polarity)

dic = {'noun':non,
       'sentence':sentence,
       'score':score
       }

nouns_scoreboard = pd.DataFrame(dic)
nouns_scoreboard.to_csv(r'C:\Users\nemow\Documents\628_module3\scoreboard.csv')














