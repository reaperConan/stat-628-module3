# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:58:18 2019

@author: nemow
"""

import os
import json
from sklearn.externals import joblib
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

#zorm function
def znorm(x):
    x = (x-np.mean(x))/np.std(x)
    return x
################ read in the user json file ################################################
comp_user = []
comp_review = []
friends = []
fans = []
review_count = []
star = []
user_id = []
with open(r"C:\Users\nemow\Documents\628_module3\user.json",'rb') as f:
    lens = f.readlines()
    for index,line in enumerate(lens):
        user = json.loads(line)
        user_id.append(user['user_id'])
        comp_user.append(user['compliment_cool'] + user['compliment_cute'] + user['compliment_funny'] + user['compliment_hot'] + user['compliment_list'] + user['compliment_more'] + user['compliment_note'] + user['compliment_photos'] + user['compliment_plain'] + user['compliment_profile'] + user['compliment_writer'])
        comp_review.append(user['cool'] + user['funny'] + user['useful'])
        friends.append(user['friends'])
        fans.append(user['fans'])
        review_count.append(user['review_count'])
        star.append(user['average_stars'])
############################################################################################
################ count the friends instead of only ids #####################################
for i in range(len(friends)):
    temp = friends[i].split(",")
    count = len(temp)
    if temp == ['None']:
        count = 0
    friends[i] = count
############################################################################################
################ attributes processing: get 4 attributes:compliments, followers, stars, reviews #######
comp_user = np.array(comp_user)
comp_review = np.array(comp_review)
friends = np.array(friends)
fans = np.array(fans)
review_count = np.array(review_count)
star = np.array(star)
followers = friends+fans #combine friends and fans to be followers
compliment = comp_review + comp_user
print('number of users who only had one review',len(review_count[review_count == 1]))
z_compliment = znorm(comp_review + comp_user)
z_followers = znorm(friends+fans)
z_review_count = znorm(review_count)
z_star = np.abs(znorm(star))
##################################################################################################
########### this comment part is the experiment process to find out the best n_clusters ##########
#data = np.transpose([z_star,z_compliment,z_followers,z_review_count])
#color = ["red","blue","gold","green","blue","purple","pink"]
#for i in range(2,8):
#    estimator = KMeans(n_clusters = i)
#    estimator.fit(data)
#    pred = estimator.predict(data)
#    for j in range(0,i):
#        print(j,":",len(pred[pred == j]))
#    plt.rcParams['savefig.dpi'] = 200
#    plt.rcParams['figure.dpi'] = 200
#    for k in range(0,i):
#        plt.scatter(review_count[pred == k],star[pred == k],c = color[k],s = 0.1,alpha = 0.5,marker = ".")
#    plt.axhline(y = np.mean(star),c = 'black')
#    plt.xlim((0,3000))
#    plt.savefig("review-star"+str(i-1)+".png")
#    plt.show()
#    for k in range(0,i):
#        plt.scatter(followers[pred == k],star[pred == k],c = color[k],s = 0.1,alpha = 0.5,marker = ".")
#    plt.axhline(y = np.mean(star),c = 'black')
#    plt.xlim((0,5000))
#    plt.savefig("followers-star"+str(i-1)+".png")
#    plt.show()
#    for k in range(0,i):
#        plt.scatter(compliment[pred == k],star[pred == k],c = color[k],s = 0.1,alpha = 0.5,marker = ".")
#    plt.axhline(y = np.mean(star),c = 'black')
#    plt.xlim((0,100000))
#    plt.savefig("compliment-star"+str(i-1)+".png")
#    plt.show()
#    for k in range(0,i):
#        plt.scatter(review_count[pred == k],compliment[pred == k],c = color[k],s = 0.1,alpha = 0.5,marker = ".")
#    plt.xlim((0,3000))
#    plt.ylim((0,20000))
#    plt.savefig("review-compliment"+str(i-1)+".png")
#    plt.show()
#    for k in range(0,i):
#        plt.scatter(review_count[pred == k],followers[pred == k],c = color[k],s = 0.1,alpha = 0.5,marker = ".")
#    plt.xlim((0,3000))
#    plt.savefig("review-followers"+str(i-1)+".png")
#    plt.show()
#    for k in range(0,i):
#        plt.scatter(compliment[pred == k],followers[pred == k],c = color[k],s = 0.1,alpha = 0.5,marker = ".")
#    plt.xlim((0,100000))
#    plt.ylim((0,8000))
#    plt.savefig("compliment-followers"+str(i-1)+".png")
#    plt.show()
#    if i == 2:
#        break
#####################################################################################################
###################### kmeans with n_cluster=5 ##########################################################
data = np.transpose([z_star,z_compliment,z_followers,z_review_count])
estimator = KMeans(n_clusters = 5)
estimator.fit(data)
pred = estimator.predict(data)
#draw the plots to find out the cluster we want
plt.scatter(compliment[pred == 0],star[pred == 0],c = "red",s = 0.01,alpha = 0.2)
plt.scatter(compliment[pred == 1],star[pred == 1],c = "blue",s=0.01,alpha = 0.2)
plt.scatter(compliment[pred == 2],star[pred == 2],c = "purple",s=0.01,alpha = 0.2)
plt.scatter(compliment[pred == 3],star[pred == 3],c = "black",s=0.01,alpha = 0.2)
plt.scatter(compliment[pred == 4],star[pred == 4],c = "green",s=0.01,alpha = 0.2)
plt.show()

user_id = np.array(user_id)
baduser = user_id[pred == 3]















