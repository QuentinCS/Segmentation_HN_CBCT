# Script for plotting the result from inference sementation from result.json file

import gatetools as gt
import numpy as np
import matplotlib.pyplot as plt
import difflib as di
from os import listdir
from os.path import isfile, join
import os
import shutil as sh
import oar as dt
import re
import time
import sys
import itk
import gzip
import json
import SimpleITK as sitk

# Modified mean and std to take in account empty organs
def meanModified (tab):
	Sum = 0
	n = 0
	for i in range(len(tab)):
		if tab[i] != 0:
			Sum += tab[i]
			n += 1		
	return Sum/(n+1e-10)

def stdModified (tab):
	Sum = 0
	n = 0
	mean = meanModified(tab)
	for i in range(len(tab)):
		if tab[i] != 0:
			Sum += pow((tab[i] - mean), 2)
			n += 1
	return np.sqrt(Sum/(n+1e-10))

start_time = time.time()

# Get results from json file 
with open("result.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

Nb_images = jsonObject['Number of images']
list_images = jsonObject['List images']
list_organs = jsonObject['List Organs']
Nb_organs = len(list_organs)

print('Number of images :', Nb_images)
print('List of images :', list_images)
print('List of organs :', list_organs)

Images = []
Dice_raw = np.zeros((Nb_images, Nb_organs)) # Lines : images, columns : OARs
Hausdorff_raw = np.zeros((Nb_images, Nb_organs)) # Lines : images, columns : OARs

for i in range(0, Nb_images):
	#print(json.dumps(jsonObject['Image%s'%(i)], indent=4, sort_keys=True))
	Images.append(jsonObject['Image%s'%(i)])

	for oar in range(0, len(list_organs)):
		if list_organs[oar] in Images[i]['Dice']:
			Dice_raw[i][oar] = float(Images[i]['Dice']['%s'%(list_organs[oar])])
			Hausdorff_raw[i][oar] = float(Images[i]['Hausdorff']['%s'%(list_organs[oar])])
			

# Results with missing values removed 
Dice = []
Hausdorff = []
for i in range(Nb_organs):
	a = []
	b = []
	for j in range(Nb_images):
		if Dice_raw[j][i] != 0:
			a.append(Dice_raw[j][i])
		if Hausdorff_raw[j][i] != 0:
			b.append(Hausdorff_raw[j][i])
	Dice.append(a)
	Hausdorff.append(b)


# Stats on Data 
Stats = np.zeros((4, Nb_organs))
for i in range(Nb_organs):
	Stats[0][i] = meanModified(Dice_raw[:,i])
	Stats[1][i] = stdModified(Dice_raw[:,i])
	Stats[2][i] = meanModified(Hausdorff_raw[:,i])
	Stats[3][i] = stdModified(Hausdorff_raw[:,i])

print("\nDice :")
print("-----------------------------------------------")
print(Dice_raw)
print("Mean : \n", Stats[0])
print("Std : \n", Stats[1])
print("-----------------------------------------------")
print("\nHausdorff :")
print("-------------------------------------------------------")
print(Hausdorff_raw)
print("Mean : \n", Stats[2])
print("Std : \n", Stats[3])
print("-------------------------------------------------------")


# Boxplots for Dice and Hausdorff 
fig = plt.figure(figsize=(20,10))
plt.subplot(1, 2, 1)
plt.boxplot(Dice, labels=list_organs)
plt.title('Dice similarity coefficient')
plt.ylabel('DSC (-)')
plt.ylim(0, 1)
#plt.show()

#plt.figure()#figsize=(20,10))
plt.subplot(1, 2, 2)
plt.boxplot(Hausdorff, labels=list_organs)
plt.title('Hausdorff distance')
plt.ylabel('HD95 (mm)')
plt.ylim(0)
plt.show()
fig.savefig("DSC_HD.pdf")


save = open("Results.txt", "w")
save.write("Number of images : %s\n"%(Nb_images))
save.write("List of organs : %s\n"%(list_organs))
save.write("\nDice : \n")
for i in range(len(Dice_raw)):
	for j in range(len(Dice_raw[i])):
		save.write("%10.10s  "%(Dice_raw[i][j]))
	save.write("\n")
save.write("\n \nHausdorff : \n")
for i in range(len(Hausdorff_raw)):
	for j in range(len(Hausdorff_raw[i])):
		save.write("%10.10s  "%(Hausdorff_raw[i][j]))
	save.write("\n")
save.close()



duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
