# Script to compute volumes of organs at risks from training dataset 
# Images in folder 'labelsTr'

import gatetools as gt
import numpy as np
import matplotlib.pyplot as plt
import difflib as di
from os import listdir
from os.path import isfile, join
import os
import shutil as sh
import dict_oar as dt
import re
import time
import sys
import itk
import gzip
import json

start_time = time.time()

# Variables
directory = 0
list1 =[]
list_name =[]
directory_name = []
nb_image = 0
n_missing = 0
nb_oar = np.zeros(len(dt.Label)-1)
n_oar = len(dt.Label)

# Travel through directory to get file list 
rootDir = 'labelsTr/'
for dirName, subdirList, fileList in os.walk(rootDir):
    directory += 1
    directory_name.append(dirName)

fileList.sort()
#print(fileList)

# Dict to save the results 
Volume = {'Number of image ': len(fileList)}

for i in range(len(fileList)):
	dict_volume = {}
	image_itk = itk.imread(rootDir + fileList[i])
	image_np = itk.array_from_image(image_itk)
	for key, value in dt.Label.items():
		if key != 'Background':
			mask_oar = image_np.copy()
			mask_oar.fill(0)
			mask = image_np==dt.Label[key]
			mask_oar[mask] = 1
			#print(dt.Label[key])
			volume = np.sum(mask_oar != 0)*(0.1*image_itk.GetSpacing()[0]*0.1*image_itk.GetSpacing()[1]*0.1*image_itk.GetSpacing()[2])
			dict_volume[key] = volume
			#print("OAR :", key,  ", Surface :", dict_volume[key], " cm^3")

	Volume['Image_%s'%(i)] = dict_volume
	if i%5 == False:
		print(i)

# Save result to json 
with open("result.json", 'w') as outfile:
	json.dump(Volume, outfile, indent=4)

list_organs = []
for key, value in dt.Label.items():
	if key != 'Background':
		list_organs.append(key)

Vol_raw = np.zeros((len(fileList), len(list_organs)))
Vol = []
for i in range(len(fileList)):
	for oar in range(0, len(list_organs)):
		Vol_raw[i][oar] = float(Volume['Image_%s'%(i)]['%s'%(list_organs[oar])])
		

for oar in range(0, len(list_organs)):
	a = []
	for i in range(len(fileList)):
		if Vol_raw[i][oar] != 0: 
			a.append(Vol_raw[i][oar])					
	Vol.append(a)

# Plot histogramms for each OAR
fig=plt.figure(figsize=(20, 15))
for oar in range(1, n_oar):
	plt.subplot(2, 6, oar)
	plt.suptitle('Volume of Organs at risks in train set')
	plt.hist(Vol[oar-1], label='N = %i \nMean = %.2f \nStd = %.2f'%(len(Vol[oar-1]), np.mean(Vol[oar-1]), np.std(Vol[oar-1])))
	plt.title(list_organs[oar-1])
	plt.xlabel('V ($cm^3$)', fontsize=8)
	if oar == 1 or oar == 7:
		plt.ylabel('dN/dV', fontsize=10)
	plt.legend()
plt.show()
fig.savefig('Volume_oar.pdf')

duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
