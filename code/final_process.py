# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:53:09 2019

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
from textblob import TextBlob

#################### functions and preparations #########################################
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
stop_words = pd.read_table(r"C:\Users\nemow\Documents\628_module3\stat-628-module3-master\data\stop_words.txt")
stop_words = list(stop_words["words"])
#########################################################################################
################### 
data = review['text']
for i in range(len(data)):
    data[i] = word_process(data[i])
#    temp = data[i].replace('\n', ' ').split(' ')
#    comb = temp[0]
#    for j in range(len(temp)):
#        temp[j] = lem.lemmatize(temp[j], "v")
#        if j > 0:
#            comb = " ".join([comb,temp[j]])
#    data[i] = comb

########################################################################
word = list(map(lambda x: x.replace('no ', 'no').replace('never ', 'never').replace('not ', 'not').replace("n't ", ' not').replace('nt ', ' not').replace('discou','discount').replace("n' ", " not").replace("should ","should").replace("would ", "would").replace('\n', ' ').split(' '), list(data)))








############################## price ############################################
price_word = ["ticket","price","cost","deal"]
information1 = {}
score1 = []
for i in range(len(word)):
    temp = word[i]
    forward = []
    backward = []
    save = {}
    count = -1
    sumscore = 0
    for j in range(len(temp)):
        if temp[j] in price_word:
            count = count+1
            for k in range(j):
                if temp[j-k-1]!='':
                    forward.append(temp[j-k-1])
                else:
                    break
            for k in range(len(temp)-j-1):
                if temp[j+k+1]!='':
                    backward.append(temp[j+k+1])
                else:
                    break
            sentence = ""
            for m in range(len(forward)):
                sentence = " ".join([sentence, forward[len(forward)-1-m]])
            sentence = " ".join([sentence,temp[j]])
            for m in range(len(backward)):
                sentence = " ".join([sentence, backward[m]])
            blob = TextBlob(sentence)
            score = str(blob.sentiment.polarity)
            save[count] = [temp[j], sentence, score]
            sumscore = sumscore + blob.sentiment.polarity
    information1[i] = save
    if count == -1:
        score1.append(0)
    else:
        score1.append(sumscore/(count+1))

##################################################################################
############################## location ############################################
location_word = ["location","hotel","car","park","restaurant"]
information2 = {}
score2 = []
for i in range(len(word)):
    temp = word[i]
    forward = []
    backward = []
    save = {}
    count = -1
    sumscore = 0
    for j in range(len(temp)):
        if temp[j] in location_word:
            count = count+1
            for k in range(j):
                if temp[j-k-1]!='':
                    forward.append(temp[j-k-1])
                else:
                    break
            for k in range(len(temp)-j-1):
                if temp[j+k+1]!='':
                    backward.append(temp[j+k+1])
                else:
                    break
            sentence = ""
            for m in range(len(forward)):
                sentence = " ".join([sentence, forward[len(forward)-1-m]])
            sentence = " ".join([sentence,temp[j]])
            for m in range(len(backward)):
                sentence = " ".join([sentence, backward[m]])
            blob = TextBlob(sentence)
            score = str(blob.sentiment.polarity)
            save[count] = [temp[j], sentence, score]
            sumscore = sumscore + blob.sentiment.polarity
    information2[i] = save
    if count == -1:
        score2.append(0)
    else:
        score2.append(sumscore/(count+1))

##################################################################################
############################## facility ############################################
facility_word = ["facility","seat","place","chair","recliner","restroom","space","lobby","leather","screen","sound","3d","film","picture"]
information3 = {}
score3 = []
for i in range(len(word)):
    temp = word[i]
    forward = []
    backward = []
    save = {}
    count = -1
    sumscore = 0
    for j in range(len(temp)):
        if temp[j] in facility_word:
            count = count+1
            for k in range(j):
                if temp[j-k-1]!='':
                    forward.append(temp[j-k-1])
                else:
                    break
            for k in range(len(temp)-j-1):
                if temp[j+k+1]!='':
                    backward.append(temp[j+k+1])
                else:
                    break
            sentence = ""
            for m in range(len(forward)):
                sentence = " ".join([sentence, forward[len(forward)-1-m]])
            sentence = " ".join([sentence,temp[j]])
            for m in range(len(backward)):
                sentence = " ".join([sentence, backward[m]])
            blob = TextBlob(sentence)
            score = str(blob.sentiment.polarity)
            save[count] = [temp[j], sentence, score]
            sumscore = sumscore + blob.sentiment.polarity
    information3[i] = save
    if count == -1:
        score3.append(0)
    else:
        score3.append(sumscore/(count+1))

##################################################################################
############################## environment ############################################
envir_word = ["wait","time","experience","people","line","style","security","smell","table"]
information4 = {}
score4 = []
for i in range(len(word)):
    temp = word[i]
    forward = []
    backward = []
    save = {}
    count = -1
    sumscore = 0
    for j in range(len(temp)):
        if temp[j] in envir_word:
            count = count+1
            for k in range(j):
                if temp[j-k-1]!='':
                    forward.append(temp[j-k-1])
                else:
                    break
            for k in range(len(temp)-j-1):
                if temp[j+k+1]!='':
                    backward.append(temp[j+k+1])
                else:
                    break
            sentence = ""
            for m in range(len(forward)):
                sentence = " ".join([sentence, forward[len(forward)-1-m]])
            sentence = " ".join([sentence,temp[j]])
            for m in range(len(backward)):
                sentence = " ".join([sentence, backward[m]])
            blob = TextBlob(sentence)
            score = str(blob.sentiment.polarity)
            save[count] = [temp[j], sentence, score]
            sumscore = sumscore + blob.sentiment.polarity
    information4[i] = save
    if count == -1:
        score4.append(0)
    else:
        score4.append(sumscore/(count+1))

##################################################################################
############################## food&drink ############################################
food_word = ["drink","beverage","bar","snack","eat","water","soda","menu","beer","popcorn"]
information5 = {}
score5 = []
for i in range(len(word)):
    temp = word[i]
    forward = []
    backward = []
    save = {}
    count = -1
    sumscore = 0
    for j in range(len(temp)):
        if temp[j] in food_word:
            count = count+1
            for k in range(j):
                if temp[j-k-1]!='':
                    forward.append(temp[j-k-1])
                else:
                    break
            for k in range(len(temp)-j-1):
                if temp[j+k+1]!='':
                    backward.append(temp[j+k+1])
                else:
                    break
            sentence = ""
            for m in range(len(forward)):
                sentence = " ".join([sentence, forward[len(forward)-1-m]])
            sentence = " ".join([sentence,temp[j]])
            for m in range(len(backward)):
                sentence = " ".join([sentence, backward[m]])
            blob = TextBlob(sentence)
            score = str(blob.sentiment.polarity)
            save[count] = [temp[j], sentence, score]
            sumscore = sumscore + blob.sentiment.polarity
    information5[i] = save
    if count == -1:
        score5.append(0)
    else:
        score5.append(sumscore/(count+1))

##################################################################################    
############################## service ############################################
service_word = ["service","serve","server","order","employee","staff"]
information6 = {}
score6 = []
for i in range(len(word)):
    temp = word[i]
    forward = []
    backward = []
    save = {}
    count = -1
    sumscore = 0
    for j in range(len(temp)):
        if temp[j] in service_word:
            count = count+1
            for k in range(j):
                if temp[j-k-1]!='':
                    forward.append(temp[j-k-1])
                else:
                    break
            for k in range(len(temp)-j-1):
                if temp[j+k+1]!='':
                    backward.append(temp[j+k+1])
                else:
                    break
            sentence = ""
            for m in range(len(forward)):
                sentence = " ".join([sentence, forward[len(forward)-1-m]])
            sentence = " ".join([sentence,temp[j]])
            for m in range(len(backward)):
                sentence = " ".join([sentence, backward[m]])
            blob = TextBlob(sentence)
            score = str(blob.sentiment.polarity)
            save[count] = [temp[j], sentence, score]
            sumscore = sumscore + blob.sentiment.polarity
    information6[i] = save
    if count == -1:
        score6.append(0)
    else:
        score6.append(sumscore/(count+1))

##################################################################################
############################## promotion ############################################
promo_word = ["family","vip","pass","discount"]
information7 = {}
score7 = []
for i in range(len(word)):
    temp = word[i]
    forward = []
    backward = []
    save = {}
    count = -1
    sumscore = 0
    for j in range(len(temp)):
        if temp[j] in promo_word:
            count = count+1
            for k in range(j):
                if temp[j-k-1]!='':
                    forward.append(temp[j-k-1])
                else:
                    break
            for k in range(len(temp)-j-1):
                if temp[j+k+1]!='':
                    backward.append(temp[j+k+1])
                else:
                    break
            sentence = ""
            for m in range(len(forward)):
                sentence = " ".join([sentence, forward[len(forward)-1-m]])
            sentence = " ".join([sentence,temp[j]])
            for m in range(len(backward)):
                sentence = " ".join([sentence, backward[m]])
            blob = TextBlob(sentence)
            score = str(blob.sentiment.polarity)
            save[count] = [temp[j], sentence, score]
            sumscore = sumscore + blob.sentiment.polarity
    information7[i] = save
    if count == -1:
        score7.append(0)
    else:
        score7.append(sumscore/(count+1))

##################################################################################
price = []
location = []
facility = []
environment = []
food = []
service = []
promotion = []

for i in range(len(movie_index)):
    find = final_id[i]
    temp1 = 0
    temp2 = 0
    temp3 = 0
    temp4 = 0
    temp5 = 0
    temp6 = 0
    temp7 = 0
    for j in range(len(data)):
        if review['business_id'][j] == find:
            temp1 += score1[j]
            temp2 += score2[j]
            temp3 += score3[j]
            temp4 += score4[j]
            temp5 += score5[j]
            temp6 += score6[j]
            temp7 += score7[j]
    price.append(temp1)
    location.append(temp2)
    facility.append(temp3)
    environment.append(temp4)
    food.append(temp5)
    service.append(temp6)
    promotion.append(temp7)




review['business_id'][0]
average = [np.median(price), np.median(location), np.median(facility), np.median(environment), np.median(food), np.median(service), np.median(promotion)]
seven = ["price","location","facility","environment","food","service","promotion"]
good_ad = ["Your customers are pleased with the price.", "The location of your cinema is great.", "The facilities make your customers comfortable.", "Your cinema has create a pleasant environment for the customers.", "Food and drinks here provides customers a great experience.", "The service is gratifying.", "Customers like your promotion activities very much."]
bad_ad = ["Your customers are complaining about the price.", "Your cinema may not be in the best area.","You should improve the facilities.", "It's helpful if your can create a better environment.", "Better food and drinks can make your cinema more competitive.", "The customers are expecting better service.", "More promotion plans may attract more customers."]

def order(x):
    y = sorted(x)
    z = []
    for i in range(len(y)):
        for j in range(len(x)):
            if y[i] == x[j] and y[i] != 0:
                z.append(j)
    return(z)






advice = []
for i in range(len(final_id)):
    read_id = final_id[i]
    temp_score = [price[i],location[i],facility[i],environment[i],food[i],service[i],promotion[i]]
    temp_advice = ""
    if temp_score == [0,0,0,0,0,0,0]:
        advice.append("There are too few reviews to analyse. Maybe your cinema needs more advertisements.")
        continue
    else:
        above = ""
        below = ""
        for j in range(len(average)):
            if temp_score[j]>average[j] and temp_score[j] != 0:
                above = ",".join([above,seven[j]])
            if temp_score[j]<average[j] and temp_score[j] != 0:
                below = ",".join([below,seven[j]])
        if above != "":
            temp_advice = " ".join([temp_advice,"The rating of",above[1:],"of your cinema is higher than median."])
        if below != "":
            temp_advice = " ".join([temp_advice,"The rating of",below[1:],"of your cinema is lower than median."])
        
        fin_score = order(temp_score)
        if len(fin_score)>0:
            temp_advice = " ".join([temp_advice,bad_ad[fin_score[0]]])
            if len(fin_score)>1:
                temp_advice = " ".join([temp_advice,bad_ad[fin_score[1]]])
                if len(fin_score)>2 and len(fin_score)<4:
                    if temp_score[fin_score[2]]>average[fin_score[2]]:
                        temp_advice = " ".join([temp_advice,good_ad[fin_score[2]]])
                else:
                    if temp_score[fin_score[-1]]>average[fin_score[-1]]:
                        temp_advice = " ".join([temp_advice,good_ad[fin_score[-1]]])
                    if temp_score[fin_score[-2]]>average[fin_score[-2]]:
                        temp_advice = " ".join([temp_advice,good_ad[fin_score[-2]]])

    advice.append(temp_advice)

final = {"id":final_id,
         "name":final_name,
         "state":final_state,
         "city":final_city,
         "price":price,
         "location":location,
         "facility":facility,
         "environment":environment,
         "food&drink":food,
         "service":service,
         "promotion":promotion,
         "advice":advice
        }
final_csv = pd.DataFrame(final)
final_csv.to_csv(r'C:\Users\nemow\Documents\628_module3\final_score.csv')



















