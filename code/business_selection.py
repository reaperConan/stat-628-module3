# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 00:45:56 2019

@author: nemow
"""

import os
import json
from sklearn.externals import joblib
import numpy as np

bu_categories = []
bu_id = []
bu_name = []
movie_index = []
attributes = []

with open(r"C:\Users\nemow\Documents\628_module3\business.json",'rb') as f:
    lens = f.readlines()
    for index,line in enumerate(lens):
        business = json.loads(line)
        bu_categories.append(business['categories'])
        bu_id.append(business['business_id'])
        bu_name.append(business['name'])
        if "cinema" in str(business['categories']).lower():
            movie_index.append(index) 

final_id = np.array(bu_id)[movie_index]




            
#bu_categories = np.array(bu_categories)
#save_categories = []
#for i in movie_index:
#    temp = bu_categories[i].split(",")
#    for j in range(len(temp)):
#        save_categories.append(temp[j])
#
#
#save_categories = list(set(save_categories))
#for i in range(len(save_categories)):
#    if "cinema" in str(save_categories[i]).lower() or "theater" in str(save_categories[i]).lower():
#        print(save_categories[i])
