#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 09:14:20 2022

@author: quentin
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re

"""
def is_in(word, lists):
    for i in lists:
        if word == lists[i]:
            return True
    return False 
"""

Data = pd.read_excel('Biblio.xlsx', sheet_name="Segmentation DL_H&N")
Data['OARs'] = Data['OARs'].astype('string')
year = Data['Date'].values
train_set = Data['Train set'].values
test_set = Data['Test set'].values
loss = Data['Loss'].values
N_oar = Data['N_OARs'].values 
oar = Data['OARs'].values 




Oar = []


for i in range(0, len(oar)):
    a = re.split(',', oar[i])
    #if a[0] == ' ':
    #    a.pop(0)
    for j in range(len(a)):
        if a[j] != '0':
            Oar.append(a[j])



#print(Data)
print("Nombre d'articles :", len(Data))
print("Nombre moyen de patient pour le train set est %.f"%(np.mean(train_set)))
print("Nombre moyen de patient pour le test set est %.f"%(np.mean(test_set)))


plt.figure(figsize=(15,8))
plt.hist(year, bins=[i+min(year) for i in range(max(year)-min(year)+2)])
plt.xlabel('Year')
plt.ylabel('Articles (N)')
plt.show()

plt.figure(figsize=(15,8))
plt.hist(N_oar)#, bins=[i+min(year) for i in range(max(year)-min(year)+2)])
plt.title('Number of OARs per articles')
plt.xlabel('Nb_oars')
plt.ylabel('Articles (N)')
plt.show()

plt.figure(figsize=(50,25))
labels, counts = np.unique(Oar, return_counts=True)
ticks = range(len(counts))
plt.bar(ticks,counts, align='center')
plt.xticks(ticks, labels, rotation=90, fontsize=23)
#plt.title('Organs at risks frequency in articles', fontsize=50)
plt.ylabel('Articles (N)', fontsize=30)