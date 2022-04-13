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

# Function to count number of evaluation cases (both prediction and label present)
def count_eval (data):
	Eval = np.zeros(data.shape[1])
	print(data.shape[1])
	for i in range(0, data.shape[1]):
		for j in range(data.shape[0]):
			if data[j][i] != 0:
				Eval[i] += 1
	return Eval




start_time = time.time()

# Get results from json file 
with open("result.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

Nb_images = jsonObject['Number of images']
list_images = jsonObject['List images']
list_organs = jsonObject['List Organs']
Nb_organs = len(list_organs)

# To use all OAR in result.json use the 3 lines below
#list_oar = list_organs
#list_oar.remove('Patient')
#Nb_oar = len(list_oar)

# To use specific OAR use the 3 lines below
Label = ['Parotide_D', 'Parotide_G', 'Tronc_Cerebral', 'Cavite_Buccale', 'Moelle', 'Oesophage', 'Thyroide', 'Mandibule', 'Larynx-Trachee', 'SubMandD', 'SubMandG', 'Oeil_D', 'Oeil_G']
list_oar = Label
Nb_oar = len(Label)


print('Number of images :', Nb_images)
print('List of images :', list_images)
print('List of organs :', list_oar)

Images = []
Dice_raw = np.zeros((Nb_images, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_raw = np.zeros((Nb_images, Nb_oar)) # Lines : images, columns : OARs

for i in range(0, Nb_images):
	#print(json.dumps(jsonObject['Image%s'%(i)], indent=4, sort_keys=True))
	Images.append(jsonObject['Image%s'%(i)])

	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images[i]['Dice']:
			Dice_raw[i][oar] = float(Images[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_raw[i][oar] = float(Images[i]['Hausdorff']['%s'%(list_oar[oar])])
			

# Results with missing values removed 
Dice = []
Hausdorff = []
for i in range(Nb_oar):
	a = []
	b = []
	for j in range(Nb_images):
		if Dice_raw[j][i] != 0:
			a.append(Dice_raw[j][i])
		if Hausdorff_raw[j][i] != 0:
			b.append(Hausdorff_raw[j][i])
	Dice.append(a)
	Hausdorff.append(b)


evaluation_number = count_eval(Dice_raw)


# Stats on Data 
Stats = np.zeros((4, Nb_oar))
for i in range(Nb_oar):
	Stats[0][i] = meanModified(Dice_raw[:,i])
	Stats[1][i] = stdModified(Dice_raw[:,i])
	Stats[2][i] = meanModified(Hausdorff_raw[:,i])
	Stats[3][i] = stdModified(Hausdorff_raw[:,i])

print("\nDice :")
print("-----------------------------------------------")
print(Dice_raw)
print("Mean : \n", Stats[0])
print("Std : \n", Stats[1])
print("Stats : \n", evaluation_number)
print("-----------------------------------------------")
print("\nHausdorff :")
print("-------------------------------------------------------")
print(Hausdorff_raw)
print("Mean : \n", Stats[2])
print("Std : \n", Stats[3])
print("Stats : \n", evaluation_number)
print("-------------------------------------------------------")


# Boxplots for Dice and Hausdorff 
fig = plt.figure(figsize=(20,10))
#plt.subplot(1, 2, 1)
plt.boxplot(Dice, labels=list_oar, showmeans=True)
#plt.boxplot(Dice, labels=list_organs)
plt.title('Dice similarity coefficient')
plt.ylabel('DSC (-)')
plt.ylim(0, 1)
#plt.show()
fig.savefig("Dice.png")

#plt.figure()#figsize=(20,10))
fig1 = plt.figure(figsize=(20,15))
#plt.subplot(1, 2, 2)
plt.boxplot(Hausdorff, labels=list_oar, showmeans=True)
#plt.boxplot(Hausdorff, labels=list_organs)
plt.title('Hausdorff distance')
plt.ylabel('HD95 (mm)')
plt.ylim(0)
#plt.show()
fig1.savefig("HD.pdf")

save = open("Results.txt", "w")
save.write("Number of images : %s\n"%(Nb_images))
save.write("List of organs : %s\n"%(list_oar))
save.write("\nDice : \n")
for i in range(len(Dice_raw)):
	for j in range(len(Dice_raw[i])):
		save.write("%10.10s  "%(Dice_raw[i][j]))
	save.write("\n")
save.write("Mean : \n")
for i in range(len(Stats[0])):
	save.write("%10.10s  "%(Stats[0][i]))
save.write("\nStd : \n")
for i in range(len(Stats[1])):
	save.write("%10.10s  "%(Stats[1][i]))
save.write("\nStats : \n")
for i in range(len(evaluation_number)):
	save.write("%10.10s  "%(int(evaluation_number[i])))



save.write("\n \nHausdorff : \n")
for i in range(len(Hausdorff_raw)):
	for j in range(len(Hausdorff_raw[i])):
		save.write("%10.10s  "%(Hausdorff_raw[i][j]))
	save.write("\n")
save.write("Mean : \n")
for i in range(len(Stats[2])):
	save.write("%10.10s  "%(Stats[2][i]))
save.write("\nStd : \n")
for i in range(len(Stats[3])):
	save.write("%10.10s  "%(Stats[3][i]))
save.write("\nStats : \n")
for i in range(len(evaluation_number)):
	save.write("%10.10s  "%(int(evaluation_number[i])))
save.close()


duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
