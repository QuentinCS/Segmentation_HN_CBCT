# Script for comparing the results of inference on sCT and on CBCT
# plotting the result from inference segmentation from result.json file

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

def define_box_properties(plot_name, color_code, label):
    for k, v in plot_name.items():
        plt.setp(plot_name.get(k), color=color_code)
         
    # use plot function to draw a small line to name the legend.
    plt.plot([], c=color_code, label=label)
    plt.legend(fontsize=20)
 

start_time = time.time()

# Get results from json file for CT
with open("/export/home/qchaine/Stage/Stage_CREATIS/Jean_zay/Separated_organs/CT_sCT/Analyse/Full/result_sCT_full.json") as jsonFile:
    jsonObject_sCT = json.load(jsonFile)
    jsonFile.close()

Nb_images = jsonObject_sCT['Number of images']
list_images = jsonObject_sCT['List images']
list_organs = jsonObject_sCT['List Organs']
Nb_organs = len(list_organs)

# Get results from json file for sCT
with open("../Full/result.json") as jsonFile:
    jsonObject_CBCT = json.load(jsonFile)
    jsonFile.close()

Nb_images_CBCT = jsonObject_CBCT['Number of images']
list_images_CBCT = jsonObject_CBCT['List images']

# To use all OAR in result.json use the 3 lines below
list_oar = list_organs
list_oar.remove('Patient')
#list_oar.remove('Larynx-Trachee')
list_oar.remove('Nerf_Optique_D')
list_oar.remove('Nerf_Optique_G')
Nb_oar = len(list_oar)

# To use specific OAR use the 3 lines below
#Label = ['Parotide_D', 'Parotide_G', 'Tronc_Cerebral', 'Cavite_Buccale', 'Moelle', 'Oesophage', 'Thyroide', 'Mandibule', 'Larynx-Trachee', 'SubMandD', 'SubMandG', 'Oeil_D', 'Oeil_G']
Label = ['Parotid_R', 'Parotid_L', 'Brainstem', 'Oral Cavity', 'Spinal Cord', 'Esophagus', 'Thyroid', 'Mandible', 'Larynx-Trachea', 'SubMandR', 'SubMandL', 'Eye_R', 'Eye_L']
#list_oar = Label
#Nb_oar = len(Label)


print('Number of images :', Nb_images)
print('List of images :', list_images)
print('List of organs :', list_oar)

Images_sCT = []
Images_CBCT = []
Dice_sCT_raw = np.zeros((Nb_images, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_sCT_raw = np.zeros((Nb_images, Nb_oar)) # Lines : images, columns : OARs
Dice_CBCT_raw = np.zeros((Nb_images, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_CBCT_raw = np.zeros((Nb_images, Nb_oar)) # Lines : images, columns : OARs

for i in range(0, Nb_images):
	#print(json.dumps(jsonObject['Image%s'%(i)], indent=4, sort_keys=True))
	Images_sCT.append(jsonObject_sCT['Image%s'%(i)])
	Images_CBCT.append(jsonObject_CBCT['Image%s'%(i)])

	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_sCT[i]['Dice']:
			Dice_sCT_raw[i][oar] = float(Images_sCT[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_sCT_raw[i][oar] = float(Images_sCT[i]['Hausdorff']['%s'%(list_oar[oar])])
	
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_CBCT[i]['Dice']:
			Dice_CBCT_raw[i][oar] = float(Images_CBCT[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_CBCT_raw[i][oar] = float(Images_CBCT[i]['Hausdorff']['%s'%(list_oar[oar])])
			
# Results with missing values removed 
list_2 = []
Dice = []
Dice_sCT = []
Dice_CBCT = []
Hausdorff_sCT = []
Hausdorff_CBCT = []
for i in range(Nb_oar):
	a_sCT = []
	a_CBCT = []
	b_sCT = []
	b_CBCT = []
	for j in range(Nb_images):
		if Dice_sCT_raw[j][i] != 0:
			a_sCT.append(Dice_sCT_raw[j][i])
		if Dice_CBCT_raw[j][i] != 0:
			a_CBCT.append(Dice_CBCT_raw[j][i])
		
		if Hausdorff_sCT_raw[j][i] != 0:
			b_sCT.append(Hausdorff_sCT_raw[j][i])
		if Hausdorff_CBCT_raw[j][i] != 0:
			b_CBCT.append(Hausdorff_CBCT_raw[j][i])
		
	Dice.append(a_sCT)
	list_2.append(list_oar[i] + '_sCT')
	list_2.append(list_oar[i] + '_CBCT')
	Dice.append(a_sCT)
	Dice_sCT.append(a_sCT)
	Dice_CBCT.append(a_CBCT)
	Hausdorff_sCT.append(b_sCT)
	Hausdorff_CBCT.append(b_CBCT)


# Calculation of relative error between the sCT prediction and CBCT prediction

Dice_RE = np.zeros(len(Dice_sCT))
HD_RE = np.zeros(len(Hausdorff_sCT))

print('\nRelative error (Dice):')
for i in range(len(Dice_sCT)):
	Dice_RE[i] = (np.mean(Dice_sCT[i])-np.mean(Dice_CBCT[i]))/np.mean(Dice_sCT[i])
	HD_RE[i] = (np.mean(Hausdorff_sCT[i])-np.mean(Hausdorff_CBCT[i]))/np.mean(Hausdorff_sCT[i])
	print(f'{list_oar[i]} : -{100*Dice_RE[i]:.2f} %')

print(f'\nMean Relative errror, Dice: {100*np.mean(Dice_RE):.2f} %')
print(f'Mean Relative errror, Hausdorff: {100*np.mean(HD_RE):.2f} %')

# Boxplots for Dice and Hausdorff 
#plt.style.use('ggplot')
fig = plt.figure(figsize=(30,18))
ax = fig.add_subplot(111)
sCT_Dice = plt.boxplot(Dice_sCT, labels=list_oar, positions=np.array(np.arange(len(Dice_sCT)))*2.0-0.35, widths = 0.4)
CBCT_Dice = plt.boxplot(Dice_CBCT,positions=np.array(np.arange(len(Dice_CBCT)))*2.0+0.35, widths = 0.4)
[plt.text((2*i)-0.8, 0.95, f'RE=-{100*Dice_RE[i]:.1f} %', fontsize=16, alpha=0.8, color='grey') for i in range(len(list_oar))]
[plt.axvline(2*x+1, color = 'grey', linestyle='-', alpha=0.4) for x in range(0, len(list_oar))]
plt.axhline(y = 0.8, color = 'grey', linestyle = '--', alpha=0.4)
# setting colors for each groups
define_box_properties(sCT_Dice, '#D7191C', 'sCT')
define_box_properties(CBCT_Dice, '#2C7BB6', 'CBCT')
plt.ylabel('Dice (-)', fontsize=25)
plt.ylim(0, 1)
plt.yticks(fontsize=20)
plt.xticks(range(0, len(list_oar) * 2, 2), Label, fontsize=20, rotation=30)
plt.legend(fontsize=25, loc='lower right')
fig.savefig("Dice_sCT_CBCT.png", dpi=500)
fig.savefig("Dice_sCT_CBCT.pdf")


fig = plt.figure(figsize=(30,18))
ax = fig.add_subplot(111)
CT_HD = plt.boxplot(Hausdorff_sCT, labels=list_oar, positions=np.array(np.arange(len(Hausdorff_sCT)))*2.0-0.35, widths = 0.4)
sCT_HD = plt.boxplot(Hausdorff_CBCT,positions=np.array(np.arange(len(Hausdorff_CBCT)))*2.0+0.35, widths = 0.4)
[plt.text((2*i)-0.8, 120, f'RE={100*HD_RE[i]:.1f} %', fontsize=16, alpha=0.8, color='grey') for i in range(len(list_oar))]
[plt.axvline(2*x+1, color = 'grey', linestyle='--', alpha=0.5) for x in range(0, len(list_oar))]
# setting colors for each groups
define_box_properties(CT_HD, '#D7191C', 'CT')
define_box_properties(sCT_HD, '#2C7BB6', 'sCT')
plt.ylabel('Hausdorff (-)', fontsize=20)
plt.yticks(fontsize=20)
#plt.ylim(0, 1)
plt.xticks(range(0, len(list_oar) * 2, 2), Label, fontsize=20, rotation=30)
fig.savefig("Hausdorff_CBCT_sCT.png", dpi=500)
fig.savefig("Hausdorff_CBCT_sCT.pdf")


duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
