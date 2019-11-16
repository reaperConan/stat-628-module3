#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
from functools import reduce
import string
# from spellchecker import SpellChecker
# spell = SpellChecker()
import nltk
porter = nltk.stem.PorterStemmer()
import numpy as np
import re
pd.options.mode.chained_assignment = None
from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()
#nltk.download('wordnet')
import math


# In[2]:


user = pd.read_csv("data/c_user.csv")
tip = pd.read_csv("data/c_tip.csv")
rev = pd.read_csv("data/c_review.csv")
business = pd.read_csv("data/cinema.csv")


# In[3]:


def append(x,y):
    return x+y
def clean(x):
    return list(filter(lambda x: False if x in stop_words or x == '' else True, x))
def word_process(s):
    s = s.translate(str.maketrans('', '', string.punctuation)).lower()
    return lem.lemmatize(s, "v") 


# In[4]:


stop_words = pd.read_table("data/stop_words.txt")
stop_words = list(stop_words["words"])


# In[5]:

for star in range(6):
    if star != 0 :
        review = rev[rev["stars"] == star]
    else:
        review = rev
        
    word_init = list(map(lambda x: x.replace('no ', 'no').replace('not ', 'not').replace("n't ", ' not').replace('nt ', ' not').replace("n' ", " not").replace("should ","should").replace("would ", "would").replace('\n', ' ').split(' '), list(review["text"])))
    
    
    # In[7]:
    
    
    # sample = list(np.random.choice(len(word_init), size=100, replace=False))
    # word = list(map(lambda x: list(map(word_process, x)), list(pd.Series(word_init)[sample])))
    word = list(map(lambda x: list(map(word_process, x)), word_init))
    
    
    # In[8]:
    
    
    word_clean = list(map(clean, word))
    
    
    # In[9]:
    
    
    word_dict = {}
    review_list = review
    review_list["text"] = pd.Series(word_clean)
    for i in list(review.index.values):
        data = review.loc[i]
        if type(data["text"]) == float:
            continue
        count = 1+data["useful"]+data["funny"]+data["cool"]
        time = (np.array('2019-01-01', dtype=np.datetime64)-np.array(review_list.loc[i]["date"].split(" ")[0], dtype=np.datetime64)).astype(dtype=np.float32)
        time_weight = 3-(time/365) if (3-(time/365))  > 0 else 0
        for w in review_list.loc[i]["text"]:
            if not w in word_dict:
                word_dict[w] = 0
            word_dict[w] += count*(0.8+time_weight)
    word_dict
    
    
    # In[10]:
    
    
    # count_filter = pd.Series(word_dict) >= sorted(list(word_dict.values()))[-50]
    # count_filter = count_filter.reset_index()[0]
    # pd.Series(list(word_dict.keys()))[count_filter]
    def word_dict_fx(key):
        return word_dict[key]
    
    
    # In[11]:
    
    
    hp_word = sorted(list(word_dict.keys()), key=word_dict_fx, reverse = True)
    hp_word_count = pd.Series(word_dict)[hp_word]
    
    
    # In[12]:
    
    
    import csv
    w = csv.writer(open("word_count/output" + str(star) + ".csv", "w"))
    for key, val in hp_word_count.items():
        w.writerow([key, val])
    
