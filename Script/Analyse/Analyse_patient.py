# Script for plotting the result from inference sementation from result.json file

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

############################ BA302 ###############################

with open("BA302/result.json") as jsonFile:
    jsonObject_BA302 = json.load(jsonFile)
    jsonFile.close()

Nb_images_BA302 = jsonObject_BA302['Number of images']
list_images_BA302 = jsonObject_BA302['List images']
list_organs_BA302 = jsonObject_BA302['List Organs']
Nb_organs = len(list_organs_BA302)

# To use all OAR in result.json use the 3 lines below
list_oar = list_organs_BA302
list_oar.remove('Patient')
list_oar.remove('Larynx-Trachee')
Nb_oar = len(list_oar)

Images_BA302 = []
Dice_BA302_raw = np.zeros((Nb_images_BA302, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_BA302_raw = np.zeros((Nb_images_BA302, Nb_oar)) # Lines : images, columns : OARs

for i in range(0, Nb_images_BA302):
	Images_BA302.append(jsonObject_BA302['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_BA302[i]['Dice']:
			Dice_BA302_raw[i][oar] = float(Images_BA302[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_BA302_raw[i][oar] = float(Images_BA302[i]['Hausdorff']['%s'%(list_oar[oar])])

############################ BB92 ###############################

with open("BB92/result.json") as jsonFile:
    jsonObject_BB92 = json.load(jsonFile)
    jsonFile.close()

Nb_images_BB92 = jsonObject_BB92['Number of images']
list_images_BB92 = jsonObject_BB92['List images']

Images_BB92 = []
Dice_BB92_raw = np.zeros((Nb_images_BB92, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_BB92_raw = np.zeros((Nb_images_BB92, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_BB92):
	Images_BB92.append(jsonObject_BB92['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_BB92[i]['Dice']:
			Dice_BB92_raw[i][oar] = float(Images_BB92[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_BB92_raw[i][oar] = float(Images_BB92[i]['Hausdorff']['%s'%(list_oar[oar])])


############################ CP72 ###############################

with open("CP72/result.json") as jsonFile:
    jsonObject_CP72 = json.load(jsonFile)
    jsonFile.close()

Nb_images_CP72 = jsonObject_CP72['Number of images']
list_images_CP72 = jsonObject_CP72['List images']

Images_CP72 = []
Dice_CP72_raw = np.zeros((Nb_images_CP72, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_CP72_raw = np.zeros((Nb_images_CP72, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_CP72):
	Images_CP72.append(jsonObject_CP72['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_CP72[i]['Dice']:
			Dice_CP72_raw[i][oar] = float(Images_CP72[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_CP72_raw[i][oar] = float(Images_CP72[i]['Hausdorff']['%s'%(list_oar[oar])])


############################ FP72 ###############################

with open("FP72/result.json") as jsonFile:
    jsonObject_FP72 = json.load(jsonFile)
    jsonFile.close()

Nb_images_FP72 = jsonObject_FP72['Number of images']
list_images_FP72 = jsonObject_FP72['List images']

Images_FP72 = []
Dice_FP72_raw = np.zeros((Nb_images_FP72, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_FP72_raw = np.zeros((Nb_images_FP72, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_FP72):
	Images_FP72.append(jsonObject_FP72['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_FP72[i]['Dice']:
			Dice_FP72_raw[i][oar] = float(Images_FP72[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_FP72_raw[i][oar] = float(Images_FP72[i]['Hausdorff']['%s'%(list_oar[oar])])


############################ GE32 ###############################

with open("GE32/result.json") as jsonFile:
    jsonObject_GE32 = json.load(jsonFile)
    jsonFile.close()

Nb_images_GE32 = jsonObject_GE32['Number of images']
list_images_GE32 = jsonObject_GE32['List images']

Images_GE32 = []
Dice_GE32_raw = np.zeros((Nb_images_GE32, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_GE32_raw = np.zeros((Nb_images_GE32, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_GE32):
	Images_GE32.append(jsonObject_GE32['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_GE32[i]['Dice']:
			Dice_GE32_raw[i][oar] = float(Images_GE32[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_GE32_raw[i][oar] = float(Images_GE32[i]['Hausdorff']['%s'%(list_oar[oar])])

############################ GL42 ###############################

with open("GL42/result.json") as jsonFile:
    jsonObject_GL42 = json.load(jsonFile)
    jsonFile.close()

Nb_images_GL42 = jsonObject_GL42['Number of images']
list_images_GL42 = jsonObject_GL42['List images']

Images_GL42 = []
Dice_GL42_raw = np.zeros((Nb_images_GL42, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_GL42_raw = np.zeros((Nb_images_GL42, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_GL42):
	Images_GL42.append(jsonObject_GL42['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_GL42[i]['Dice']:
			Dice_GL42_raw[i][oar] = float(Images_GL42[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_GL42_raw[i][oar] = float(Images_GL42[i]['Hausdorff']['%s'%(list_oar[oar])])

############################ GP4 ###############################

with open("GP4/result.json") as jsonFile:
    jsonObject_GP4 = json.load(jsonFile)
    jsonFile.close()

Nb_images_GP4 = jsonObject_GP4['Number of images']
list_images_GP4 = jsonObject_GP4['List images']

Images_GP4 = []
Dice_GP4_raw = np.zeros((Nb_images_GP4, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_GP4_raw = np.zeros((Nb_images_GP4, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_GP4):
	Images_GP4.append(jsonObject_GP4['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_GP4[i]['Dice']:
			Dice_GP4_raw[i][oar] = float(Images_GP4[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_GP4_raw[i][oar] = float(Images_GP4[i]['Hausdorff']['%s'%(list_oar[oar])])

############################ GS4 ###############################

with open("GS4/result.json") as jsonFile:
    jsonObject_GS4 = json.load(jsonFile)
    jsonFile.close()

Nb_images_GS4 = jsonObject_GS4['Number of images']
list_images_GS4 = jsonObject_GS4['List images']

Images_GS4 = []
Dice_GS4_raw = np.zeros((Nb_images_GS4, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_GS4_raw = np.zeros((Nb_images_GS4, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_GS4):
	Images_GS4.append(jsonObject_GS4['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_GS4[i]['Dice']:
			Dice_GS4_raw[i][oar] = float(Images_GS4[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_GS4_raw[i][oar] = float(Images_GS4[i]['Hausdorff']['%s'%(list_oar[oar])])



print('List of organs :', list_oar)

# Combination of result for all patients 		
# Results with missing values removed 
Dice = []
Dice_BA302 = []
Dice_BB92 = []
Dice_CP72 = []
Dice_FP72 = []
Dice_GE32 = []
Dice_GL42 = []
Dice_GP4 = []
Dice_GS4 = []

Hausdorff_BA302= []
Hausdorff_BB92 = []
Hausdorff_CP72 = []
Hausdorff_FP72 = []
Hausdorff_GE32 = []
Hausdorff_GL42 = []
Hausdorff_GP4 = []
Hausdorff_GS4 = []

for i in range(Nb_oar):

	a_BA302 = []
	a_BB92 = []
	a_CP72 = []
	a_FP72 = []
	a_GE32 = []
	a_GL42 = []
	a_GP4 = []
	a_GS4 = []

	b_BA302 = []
	b_BB92 = []
	b_CP72 = []
	b_FP72 = []
	b_GE32 = []
	b_GL42 = []
	b_GP4 = []
	b_GS4 = []

	for j in range(Nb_images_BA302):
		if Dice_BA302_raw[j][i] != 0:
			a_BA302.append(Dice_BA302_raw[j][i])
		if Hausdorff_BA302_raw[j][i] != 0:
			b_BA302.append(Hausdorff_BA302_raw[j][i])
	for j in range(Nb_images_BB92):
		if Dice_BB92_raw[j][i] != 0:
			a_BB92.append(Dice_BB92_raw[j][i])
		if Hausdorff_BB92_raw[j][i] != 0:
			b_BB92.append(Hausdorff_BB92_raw[j][i])
	for j in range(Nb_images_CP72):
		if Dice_CP72_raw[j][i] != 0:
			a_CP72.append(Dice_CP72_raw[j][i])
		if Hausdorff_CP72_raw[j][i] != 0:
			b_CP72.append(Hausdorff_CP72_raw[j][i])
	for j in range(Nb_images_FP72):
		if Dice_FP72_raw[j][i] != 0:
			a_FP72.append(Dice_FP72_raw[j][i])
		if Hausdorff_FP72_raw[j][i] != 0:
			b_FP72.append(Hausdorff_FP72_raw[j][i])
	for j in range(Nb_images_GE32):
		if Dice_GE32_raw[j][i] != 0:
			a_GE32.append(Dice_GE32_raw[j][i])
		if Hausdorff_GE32_raw[j][i] != 0:
			b_GE32.append(Hausdorff_GE32_raw[j][i])
	for j in range(Nb_images_GL42):
		if Dice_GL42_raw[j][i] != 0:
			a_GL42.append(Dice_GL42_raw[j][i])
		if Hausdorff_GL42_raw[j][i] != 0:
			b_GL42.append(Hausdorff_GL42_raw[j][i])
	for j in range(Nb_images_GP4):
		if Dice_GP4_raw[j][i] != 0:
			a_GP4.append(Dice_GP4_raw[j][i])
		if Hausdorff_GP4_raw[j][i] != 0:
			b_GP4.append(Hausdorff_GP4_raw[j][i])
	for j in range(Nb_images_GS4):
		if Dice_GS4_raw[j][i] != 0:
			a_GS4.append(Dice_GS4_raw[j][i])
		if Hausdorff_GS4_raw[j][i] != 0:
			b_GS4.append(Hausdorff_GS4_raw[j][i])
	
	Dice.append(a_BA302)
	Dice.append(a_BB92)
	Dice.append(a_CP72)
	Dice.append(a_FP72)
	Dice.append(a_GE32)
	Dice.append(a_GL42)
	Dice.append(a_GP4)
	Dice.append(a_GS4)
	Dice_BA302.append(a_BA302)
	Dice_BB92.append(a_BB92)
	Dice_CP72.append(a_CP72)
	Dice_FP72.append(a_FP72)
	Dice_GE32.append(a_GE32)
	Dice_GL42.append(a_GL42)
	Dice_GP4.append(a_GP4)
	Dice_GS4.append(a_GS4)
	Hausdorff_BA302.append(b_BA302)
	Hausdorff_BB92.append(b_BB92)
	Hausdorff_CP72.append(b_CP72)
	Hausdorff_FP72.append(b_FP72)
	Hausdorff_GE32.append(b_GE32)
	Hausdorff_GL42.append(b_GL42)
	Hausdorff_GP4.append(b_GP4)
	Hausdorff_GS4.append(b_GS4)


# Boxplots for Dice and Hausdorff 
fig, (ax1, ax2) = plt.subplots(2, figsize=(30,15))
BA302_Dice = ax1.boxplot(Dice_BA302[0:int(len(Dice_BA302)/2)], labels=list_oar[0:int(len(list_oar)/2)], positions=np.array(np.arange(len(Dice_BA302[0:int(len(Dice_BA302)/2)])))*2.0-0.9, widths = 0.2)
BB92_Dice = ax1.boxplot(Dice_BB92[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_BB92[0:int(len(Dice_BA302)/2)])))*2.0-0.6, widths = 0.2)
CP72_Dice = ax1.boxplot(Dice_CP72[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_CP72[0:int(len(Dice_BA302)/2)])))*2.0-0.3, widths = 0.2)
FP72_Dice = ax1.boxplot(Dice_FP72[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_FP72[0:int(len(Dice_BA302)/2)])))*2.0+0.0, widths = 0.2)
GE32_Dice = ax1.boxplot(Dice_GE32[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_GE32[0:int(len(Dice_BA302)/2)])))*2.0+0.3, widths = 0.2)
GL42_Dice = ax1.boxplot(Dice_GL42[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_GL42[0:int(len(Dice_BA302)/2)])))*2.0+0.6, widths = 0.2)
GP4_Dice = ax1.boxplot(Dice_GP4[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_GP4[0:int(len(Dice_BA302)/2)])))*2.0+0.75, widths = 0.2)
GS4_Dice = ax1.boxplot(Dice_GS4[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_GS4[0:int(len(Dice_BA302)/2)])))*2.0+0.9, widths = 0.2)
[ax1.axvline(2*x+1, color = 'grey', linestyle='-', alpha=0.4) for x in range(0, len(list_oar[0:int(len(Dice_BA302)/2)]))]
ax1.axhline(y = 0.8, color = 'grey', linestyle = '--', alpha=0.4)
# setting colors for each groups
define_box_properties(BA302_Dice, 'red', 'BA302')
define_box_properties(BB92_Dice, 'blue', 'BB92')
define_box_properties(CP72_Dice, 'green', 'CP72')
define_box_properties(FP72_Dice, 'yellow', 'FP72')
define_box_properties(GE32_Dice, 'brown', 'GE32')
define_box_properties(GL42_Dice, 'purple', 'GL42')
define_box_properties(GP4_Dice, 'orange', 'GP4')
define_box_properties(Gs4_Dice, 'navy', 'GS4')
ax1.set_ylabel('DSC (-)', fontsize=20)
ax1.set_ylim(0, 1)
ax1.set_xticks(range(0, len(list_oar[0:int(len(list_oar)/2)]) * 2, 2), list_oar[0:int(len(list_oar)/2)])
BA302_Dice = ax2.boxplot(Dice_BA302[int(len(Dice_BA302)/2):len(Dice_BA302)], labels=list_oar[7:len(list_oar)], positions=np.array(np.arange(len(Dice_BA302[int(len(Dice_BA302)/2):len(Dice_BA302)])))*2.0-0.9, widths = 0.2)
BB92_Dice = ax2.boxplot(Dice_BB92[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_BB92[int(len(Dice_BA302)/2):len(list_oar)])))*2.0-0.6, widths = 0.2)
CP72_Dice = ax2.boxplot(Dice_CP72[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_CP72[int(len(Dice_BA302)/2):len(list_oar)])))*2.0-0.3, widths = 0.2)
FP72_Dice = ax2.boxplot(Dice_FP72[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_FP72[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.0, widths = 0.2)
GE32_Dice = ax2.boxplot(Dice_GE32[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_GE32[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.3, widths = 0.2)
GL42_Dice = ax2.boxplot(Dice_GL42[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_GL42[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.6, widths = 0.2)
GP4_Dice = ax2.boxplot(Dice_GP4[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_GP4[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.75, widths = 0.2)
GS4_Dice = ax2.boxplot(Dice_GS4[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_GS4[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.9, widths = 0.2)
[ax2.axvline(2*x+1, color = 'grey', linestyle='-', alpha=0.4) for x in range(0, len(list_oar[int(len(Dice_BA302)/2):len(list_oar)]))]
ax2.axhline(y = 0.8, color = 'grey', linestyle = '--', alpha=0.4)
# setting colors for each groups
define_box_properties(BA302_Dice, 'red', 'BA302')
define_box_properties(BB92_Dice, 'blue', 'BB92')
define_box_properties(CP72_Dice, 'green', 'CP72')
define_box_properties(FP72_Dice, 'yellow', 'FP72')
define_box_properties(GE32_Dice, 'brown', 'GE32')
define_box_properties(GL42_Dice, 'purple', 'GL42')
define_box_properties(GP4_Dice, 'orange', 'GP4')
define_box_properties(Gs4_Dice, 'navy', 'GS4')
ax2.set_ylabel('DSC (-)', fontsize=20)
ax2.set_ylim(0, 1)
ax2.set_xticks(range(0, len(list_oar[int(len(list_oar)/2):len(list_oar)]) * 2, 2), list_oar[int(len(list_oar)/2):len(list_oar)])
lines, labels = fig.axes[-1].get_legend_handles_labels()
ax2.legend(lines[0:int(len(lines)/2)], labels[0:int(len(labels)/2)], loc = 'lower left')
fig.savefig("Dice_patient.png")
fig.savefig("Dice_patient.pdf")


fig, (ax1, ax2) = plt.subplots(2, figsize=(30,15))
BA302_HD = ax1.boxplot(Hausdorff_BA302[0:int(len(Hausdorff_BA302)/2)], labels=list_oar[0:int(len(list_oar)/2)], positions=np.array(np.arange(len(Hausdorff_BA302[0:int(len(Hausdorff_BA302)/2)])))*2.0-0.9, widths = 0.2)
BB92_HD = ax1.boxplot(Hausdorff_BB92[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_BB92[0:int(len(Hausdorff_BA302)/2)])))*2.0-0.6, widths = 0.2)
CP72_HD = ax1.boxplot(Hausdorff_CP72[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_CP72[0:int(len(Hausdorff_BA302)/2)])))*2.0-0.3, widths = 0.2)
FP72_HD = ax1.boxplot(Hausdorff_FP72[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_FP72[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.0, widths = 0.2)
GE32_HD = ax1.boxplot(Hausdorff_GE32[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_GE32[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.3, widths = 0.2)
GL42_HD = ax1.boxplot(Hausdorff_GL42[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_GL42[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.6, widths = 0.2)
GP4_HD = ax1.boxplot(Hausdorff_GP4[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_GP4[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.75, widths = 0.2)
GS4_HD = ax1.boxplot(Hausdorff_GS4[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_GS4[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.9, widths = 0.2)
[ax1.axvline(2*x+1, color = 'grey', linestyle='--', alpha=0.5) for x in range(0, len(list_oar[0:int(len(Hausdorff_BA302)/2)]))]
# setting colors for each groups
define_box_properties(BA302_HD, 'red', 'BA302')
define_box_properties(BB92_HD, 'blue', 'BB92')
define_box_properties(CP72_HD, 'green', 'CP72')
define_box_properties(FP72_HD, 'yellow', 'FP72')
define_box_properties(GE32_HD, 'brown', 'GE32')
define_box_properties(GL42_HD, 'purple', 'GL42')
define_box_properties(GP4_HD, 'orange', 'GP4')
define_box_properties(GS4_HD, 'navy', 'GS4')
ax1.set_ylabel('Hausdorff (-)', fontsize=20)
#ax1.ylim(0, 1)
ax1.set_xticks(range(0, len(list_oar[0:int(len(list_oar)/2)]) * 2, 2), list_oar[0:int(len(list_oar)/2)])
BA302_HD = ax2.boxplot(Hausdorff_BA302[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)], labels=list_oar[int(len(list_oar)/2):len(list_oar)], positions=np.array(np.arange(len(Hausdorff_BA302[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0-0.9, widths = 0.2)
BB92_HD = ax2.boxplot(Hausdorff_BB92[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_BB92[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0-0.6, widths = 0.2)
CP72_HD = ax2.boxplot(Hausdorff_CP72[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_CP72[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0-0.3, widths = 0.2)
FP72_HD = ax2.boxplot(Hausdorff_FP72[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_FP72[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.0, widths = 0.2)
GE32_HD = ax2.boxplot(Hausdorff_GE32[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_GE32[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.3, widths = 0.2)
GL42_HD = ax2.boxplot(Hausdorff_GL42[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_GL42[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.6, widths = 0.2)
GP4_HD = ax2.boxplot(Hausdorff_GP4[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_GP4[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.75, widths = 0.2)
GS4_HD = ax2.boxplot(Hausdorff_GS4[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_GS4[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.9, widths = 0.2)
[ax2.axvline(2*x+1, color = 'grey', linestyle='--', alpha=0.5) for x in range(0, len(list_oar[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)]))]
define_box_properties(BA302_HD, 'red', 'BA302')
define_box_properties(BB92_HD, 'blue', 'BB92')
define_box_properties(CP72_HD, 'green', 'CP72')
define_box_properties(FP72_HD, 'yellow', 'FP72')
define_box_properties(GE32_HD, 'brown', 'GE32')
define_box_properties(GL42_HD, 'purple', 'GL42')
define_box_properties(GP4_HD, 'orange', 'GP4')
define_box_properties(GS4_HD, 'navy', 'GS4')
ax2.set_ylabel('Hausdorff (-)', fontsize=20)
ax2.set_xticks(range(0, len(list_oar[int(len(list_oar)/2):len(list_oar)]) * 2, 2), list_oar[int(len(list_oar)/2):len(list_oar)])
lines, labels = fig.axes[-1].get_legend_handles_labels()
ax2.legend(lines[0:int(len(lines)/2)], labels[0:int(len(labels)/2)], loc = 'lower left')
fig.savefig("Hausdorff_patient.png")
fig.savefig("Hausdorff_patient.pdf")



duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
