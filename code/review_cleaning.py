# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:22:51 2019

@author: nemow
"""

import os
import json
from sklearn.externals import joblib
import numpy as np

########## read in the review json file ####################################################
review_user = []
review_stars = []
review_date = []
review_text = []
review_comp = []
review_business = []
with open(r"C:\Users\nemow\Documents\628_module3\review.json",'rb') as f:
    lens = f.readlines()
    for index,line in enumerate(lens):
        review = json.loads(line)
        if str(review['business_id']) in final_id: #select those cinema's reviews
            if str(review['user_id']) not in baduser: #delete those spam users' reviews
                review_user.append(review['user_id'])
                review_stars.append(review['stars'])
                review_date.append(review['date'])
                review_text.append(review['text'])
                review_comp.append(review['useful']+review['funny']+review['cool'])
                review_business.append(review['business_id'])
############################################################################################
########## read in the tip json file #######################################################
tip_user = []
tip_date = []
tip_text = []
tip_comp = []
tip_business = []
with open(r"C:\Users\nemow\Documents\628_module3\tip.json",'rb') as f:
    lens = f.readlines()
    for index,line in enumerate(lens):
        tip = json.loads(line)
        if str(tip['business_id']) in final_id: #select those cinema's reviews
            if str(tip['user_id']) not in baduser: #delete those spam users' reviews
                tip_user.append(tip['user_id'])
                tip_date.append(tip['date'])
                tip_text.append(tip['text'])
                tip_comp.append(tip['compliment_count'])
                tip_business.append(tip['business_id'])
############################################################################################
################ write the selected reviews and tips in csv files ##########################
dic1 = {'user_id':review_user,
        'stars':review_stars,
        'date':review_date,
        'text':review_text,
        'compliments':review_comp,
        'business_id':review_business}

dic2 = {'user_id':tip_user,
        'date':tip_date,
        'text':tip_text,
        'compliments':tip_comp,
        'business_id':tip_business}

import pandas as pd
cin_review = pd.DataFrame(dic1)
cin_tip = pd.DataFrame(dic2)

cin_review.to_csv(r'C:\Users\nemow\Documents\628_module3\cinema_review.csv')
cin_tip.to_csv(r'C:\Users\nemow\Documents\628_module3\cinema_tip.csv')
                
                
