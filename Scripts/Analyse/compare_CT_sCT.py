# Script for plotting the result for the inference on CT and sCT and comparison

import gatetools as gt
import numpy as np
import matplotlib.pyplot as plt
import difflib as di
from os import listdir
from os.path import isfile, join
import os
import shutil as sh
import re
import time
import sys
import itk
import gzip
import json
import SimpleITK as sitk
import scipy.stats as stats

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

def define_box_properties(plot_name, color_code, label):
    for k, v in plot_name.items():
        plt.setp(plot_name.get(k), color=color_code)
         
    # use plot function to draw a small line to name the legend.
    plt.plot([], c=color_code, label=label)
    plt.legend(fontsize=20)
 

start_time = time.time()

# Get results from json file for CT
with open("CT/result_CT.json") as jsonFile:
    jsonObject_CT = json.load(jsonFile)
    jsonFile.close()

Nb_images = jsonObject_CT['Number of images']
list_images = jsonObject_CT['List images']
list_organs = jsonObject_CT['List Organs']
Nb_organs = len(list_organs)

# Get results from json file for sCT
with open("sCT/result_sCT.json") as jsonFile:
    jsonObject_sCT = json.load(jsonFile)
    jsonFile.close()

Nb_images_sCT = jsonObject_sCT['Number of images']
list_images_sCT = jsonObject_sCT['List images']

# To use all OAR in result.json use the 3 lines below
list_oar = list_organs
list_oar.remove('Patient')
list_oar.remove('Larynx-Trachee')
list_oar.remove('Nerf_Optique_D')
list_oar.remove('Nerf_Optique_G')
Nb_oar = len(list_oar)

# To use specific OAR use the 3 lines below
#Label = ['Parotide_D', 'Parotide_G', 'Tronc_Cerebral', 'Cavite_Buccale', 'Moelle', 'Oesophage', 'Thyroide', 'Mandibule', 'Larynx-Trachee', 'SubMandD', 'SubMandG', 'Oeil_D', 'Oeil_G']
#list_oar = Label
#Nb_oar = len(Label)


print('Number of images :', Nb_images)
print('List of images :', list_images)
print('List of organs :', list_oar)

Images_CT = []
Images_sCT = []
Dice_CT_raw = np.zeros((Nb_images, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_CT_raw = np.zeros((Nb_images, Nb_oar)) # Lines : images, columns : OARs
Dice_sCT_raw = np.zeros((Nb_images, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_sCT_raw = np.zeros((Nb_images, Nb_oar)) # Lines : images, columns : OARs

for i in range(0, Nb_images):
	#print(json.dumps(jsonObject['Image%s'%(i)], indent=4, sort_keys=True))
	Images_CT.append(jsonObject_CT['Image%s'%(i)])
	Images_sCT.append(jsonObject_sCT['Image%s'%(i)])

	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_CT[i]['Dice']:
			Dice_CT_raw[i][oar] = float(Images_CT[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_CT_raw[i][oar] = float(Images_CT[i]['Hausdorff']['%s'%(list_oar[oar])])
	
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_sCT[i]['Dice']:
			Dice_sCT_raw[i][oar] = float(Images_sCT[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_sCT_raw[i][oar] = float(Images_sCT[i]['Hausdorff']['%s'%(list_oar[oar])])
			
# Results with missing values removed 
list_2 = []
Dice = []
Dice_CT = []
Dice_sCT = []
Hausdorff_CT = []
Hausdorff_sCT = []
for i in range(Nb_oar):
	a_CT = []
	a_sCT = []
	b_CT = []
	b_sCT = []
	for j in range(Nb_images):
		if Dice_CT_raw[j][i] != 0:
			a_CT.append(Dice_CT_raw[j][i])
		if Dice_sCT_raw[j][i] != 0:
			a_sCT.append(Dice_sCT_raw[j][i])
		if Hausdorff_CT_raw[j][i] != 0:
			b_CT.append(Hausdorff_CT_raw[j][i])
		if Hausdorff_sCT_raw[j][i] != 0:
			b_sCT.append(Hausdorff_sCT_raw[j][i])
	Dice.append(a_CT)
	list_2.append(list_oar[i] + '_CT')
	list_2.append(list_oar[i] + '_sCT')
	Dice.append(a_sCT)
	Dice_CT.append(a_CT)
	Dice_sCT.append(a_sCT)
	Hausdorff_CT.append(b_CT)
	Hausdorff_sCT.append(b_sCT)



t_Dice = np.zeros(len(list_oar))
t_HD = np.zeros(len(list_oar))

# Statistical t-test fo similarity of the samples 
#save = open("Results_test.txt", "w")
for oar in range(0, len(list_oar)):
	#print(list_organs[oar], "Test : ", stats.ttest_ind(Dice_CT[oar], Dice_sCT[oar], equal_var=False))
	_, t_Dice[oar] = stats.ttest_ind(Dice_CT[oar], Dice_sCT[oar], equal_var=False)
	_, t_HD[oar] = stats.ttest_ind(Hausdorff_CT[oar], Hausdorff_sCT[oar], equal_var=False)


# Boxplots for Dice and Hausdorff 
plt.style.use('ggplot')
fig = plt.figure(figsize=(30,18))
ax = fig.add_subplot(111)
CT_Dice = plt.boxplot(Dice_CT, labels=list_oar, positions=np.array(np.arange(len(Dice_CT)))*2.0-0.35, widths = 0.4)
sCT_Dice = plt.boxplot(Dice_sCT,positions=np.array(np.arange(len(Dice_sCT)))*2.0+0.35, widths = 0.4)
[plt.text((2*i)-0.5, 0.95, 'p=%.2f'%(t_Dice[i]), fontsize=18, alpha=0.8, color='grey') for i in range(len(list_oar))]
[plt.axvline(2*x+1, color = 'grey', linestyle='-', alpha=0.4) for x in range(0, len(list_oar))]
plt.axhline(y = 0.8, color = 'grey', linestyle = '--', alpha=0.4)
# setting colors for each groups
define_box_properties(CT_Dice, '#D7191C', 'CT')
define_box_properties(sCT_Dice, '#2C7BB6', 'sCT')
plt.ylabel('DSC (-)', fontsize=20)
plt.ylim(0, 1)
plt.xticks(range(0, len(list_oar) * 2, 2), list_oar)
plt.legend(fontsize=25, loc='lower right')
fig.savefig("Dice_CT_sCT.png")
fig.savefig("Dice_CT_sCT.pdf")

fig = plt.figure(figsize=(30,18))
ax = fig.add_subplot(111)
CT_HD = plt.boxplot(Hausdorff_CT, labels=list_oar, positions=np.array(np.arange(len(Hausdorff_CT)))*2.0-0.35, widths = 0.4)
sCT_HD = plt.boxplot(Hausdorff_sCT,positions=np.array(np.arange(len(Hausdorff_sCT)))*2.0+0.35, widths = 0.4)
[plt.text((2*i)-0.5, 90, 'p=%.2f'%(t_HD[i]), fontsize=18, alpha=0.8, color='grey') for i in range(len(list_oar))]
[plt.axvline(2*x+1, color = 'grey', linestyle='--', alpha=0.5) for x in range(0, len(list_oar))]
# setting colors for each groups
define_box_properties(CT_HD, '#D7191C', 'CT')
define_box_properties(sCT_HD, '#2C7BB6', 'sCT')
plt.ylabel('Hausdorff (-)', fontsize=20)
#plt.ylim(0, 1)
plt.xticks(range(0, len(list_oar) * 2, 2), list_oar)
fig.savefig("Hausdorff_CT_sCT.png")
fig.savefig("Hausdorff_CT_sCT.pdf")

duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
