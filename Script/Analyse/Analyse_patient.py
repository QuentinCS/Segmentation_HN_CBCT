# Script for plotting the result from inference sementation from result.json file for the differents patients 

#import gatetools as gt
import numpy as np
import matplotlib.pyplot as plt
#import difflib as di
#from os import listdir
#from os.path import isfile, join
#import os
#import shutil as sh
#import re
import time
#import sys
#import itk
#import gzip
import json
#import SimpleITK as sitk
import scipy.stats as stats

#Functions 
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
#list_oar.remove('Larynx-Trachee')
list_oar.remove('Nerf_Optique_D')
list_oar.remove('Nerf_Optique_G')
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

############################ HA22 ###############################

with open("HA22/result.json") as jsonFile:
    jsonObject_HA22 = json.load(jsonFile)
    jsonFile.close()

Nb_images_HA22 = jsonObject_HA22['Number of images']
list_images_HA22 = jsonObject_HA22['List images']

Images_HA22 = []
Dice_HA22_raw = np.zeros((Nb_images_HA22, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_HA22_raw = np.zeros((Nb_images_HA22, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_HA22):
	Images_HA22.append(jsonObject_HA22['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_HA22[i]['Dice']:
			Dice_HA22_raw[i][oar] = float(Images_HA22[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_HA22_raw[i][oar] = float(Images_HA22[i]['Hausdorff']['%s'%(list_oar[oar])])

############################ LD ###############################

with open("LD/result.json") as jsonFile:
    jsonObject_LD = json.load(jsonFile)
    jsonFile.close()

Nb_images_LD = jsonObject_LD['Number of images']
list_images_LD = jsonObject_LD['List images']

Images_LD = []
Dice_LD_raw = np.zeros((Nb_images_LD, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_LD_raw = np.zeros((Nb_images_LD, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_LD):
	Images_LD.append(jsonObject_LD['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_LD[i]['Dice']:
			Dice_LD_raw[i][oar] = float(Images_LD[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_LD_raw[i][oar] = float(Images_LD[i]['Hausdorff']['%s'%(list_oar[oar])])

############################ LY ###############################

with open("LY/result.json") as jsonFile:
    jsonObject_LY = json.load(jsonFile)
    jsonFile.close()

Nb_images_LY = jsonObject_LY['Number of images']
list_images_LY = jsonObject_LY['List images']

Images_LY = []
Dice_LY_raw = np.zeros((Nb_images_LY, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_LY_raw = np.zeros((Nb_images_LY, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_LY):
	Images_LY.append(jsonObject_LY['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_LY[i]['Dice']:
			Dice_LY_raw[i][oar] = float(Images_LY[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_LY_raw[i][oar] = float(Images_LY[i]['Hausdorff']['%s'%(list_oar[oar])])

############################ MA113 ###############################

with open("MA113/result.json") as jsonFile:
    jsonObject_MA113 = json.load(jsonFile)
    jsonFile.close()

Nb_images_MA113 = jsonObject_MA113['Number of images']
list_images_MA113 = jsonObject_MA113['List images']

Images_MA113 = []
Dice_MA113_raw = np.zeros((Nb_images_MA113, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_MA113_raw = np.zeros((Nb_images_MA113, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_MA113):
	Images_MA113.append(jsonObject_MA113['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_MA113[i]['Dice']:
			Dice_MA113_raw[i][oar] = float(Images_MA113[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_MA113_raw[i][oar] = float(Images_MA113[i]['Hausdorff']['%s'%(list_oar[oar])])

############################ PL52 ###############################

with open("PL52/result.json") as jsonFile:
    jsonObject_PL52 = json.load(jsonFile)
    jsonFile.close()

Nb_images_PL52 = jsonObject_PL52['Number of images']
list_images_PL52 = jsonObject_PL52['List images']

Images_PL52 = []
Dice_PL52_raw = np.zeros((Nb_images_PL52, Nb_oar)) # Lines : images, columns : OARs
Hausdorff_PL52_raw = np.zeros((Nb_images_PL52, Nb_oar)) # Lines : images, columns : OARs
for i in range(0, Nb_images_PL52):
	Images_PL52.append(jsonObject_PL52['Image%s'%(i)])
	for oar in range(0, len(list_oar)):
		if list_oar[oar] in Images_PL52[i]['Dice']:
			Dice_PL52_raw[i][oar] = float(Images_PL52[i]['Dice']['%s'%(list_oar[oar])])
			Hausdorff_PL52_raw[i][oar] = float(Images_PL52[i]['Hausdorff']['%s'%(list_oar[oar])])



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
Dice_HA22 = []
Dice_LD = []
Dice_LY = []
Dice_MA113 = []
Dice_PL52 = []

Hausdorff_BA302= []
Hausdorff_BB92 = []
Hausdorff_CP72 = []
Hausdorff_FP72 = []
Hausdorff_GE32 = []
Hausdorff_GL42 = []
Hausdorff_GP4 = []
Hausdorff_GS4 = []
Hausdorff_HA22 = []
Hausdorff_LD = []
Hausdorff_LY = []
Hausdorff_MA113 = []
Hausdorff_PL52 = []

for i in range(Nb_oar):

	a_BA302 = []
	a_BB92 = []
	a_CP72 = []
	a_FP72 = []
	a_GE32 = []
	a_GL42 = []
	a_GP4 = []
	a_GS4 = []
	a_HA22 = []
	a_LD = []
	a_LY = []
	a_MA113 = []
	a_PL52 = []

	b_BA302 = []
	b_BB92 = []
	b_CP72 = []
	b_FP72 = []
	b_GE32 = []
	b_GL42 = []
	b_GP4 = []
	b_GS4 = []
	b_HA22 = []
	b_LD = []
	b_LY = []
	b_MA113 = []
	b_PL52 = []

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
	for j in range(Nb_images_HA22):
		if Dice_HA22_raw[j][i] != 0:
			a_HA22.append(Dice_HA22_raw[j][i])
		if Hausdorff_HA22_raw[j][i] != 0:
			b_HA22.append(Hausdorff_HA22_raw[j][i])
	for j in range(Nb_images_LD):
		if Dice_LD_raw[j][i] != 0:
			a_LD.append(Dice_LD_raw[j][i])
		if Hausdorff_LD_raw[j][i] != 0:
			b_LD.append(Hausdorff_LD_raw[j][i])
	for j in range(Nb_images_LY):
		if Dice_LY_raw[j][i] != 0:
			a_LY.append(Dice_LY_raw[j][i])
		if Hausdorff_LY_raw[j][i] != 0:
			b_LY.append(Hausdorff_LY_raw[j][i])
	for j in range(Nb_images_MA113):
		if Dice_MA113_raw[j][i] != 0:
			a_MA113.append(Dice_MA113_raw[j][i])
		if Hausdorff_MA113_raw[j][i] != 0:
			b_MA113.append(Hausdorff_MA113_raw[j][i])
	for j in range(Nb_images_PL52):
		if Dice_PL52_raw[j][i] != 0:
			a_PL52.append(Dice_PL52_raw[j][i])
		if Hausdorff_PL52_raw[j][i] != 0:
			b_PL52.append(Hausdorff_PL52_raw[j][i])
	
	Dice.append(a_BA302)
	Dice.append(a_BB92)
	Dice.append(a_CP72)
	Dice.append(a_FP72)
	Dice.append(a_GE32)
	Dice.append(a_GL42)
	Dice.append(a_GP4)
	Dice.append(a_GS4)
	Dice.append(a_HA22)
	Dice.append(a_LD)
	Dice.append(a_LY)
	Dice.append(a_MA113)
	Dice.append(a_PL52)

	Dice_BA302.append(a_BA302)
	Dice_BB92.append(a_BB92)
	Dice_CP72.append(a_CP72)
	Dice_FP72.append(a_FP72)
	Dice_GE32.append(a_GE32)
	Dice_GL42.append(a_GL42)
	Dice_GP4.append(a_GP4)
	Dice_GS4.append(a_GS4)
	Dice_HA22.append(a_HA22)
	Dice_LD.append(a_LD)
	Dice_LY.append(a_LY)
	Dice_MA113.append(a_MA113)
	Dice_PL52.append(a_PL52)

	Hausdorff_BA302.append(b_BA302)
	Hausdorff_BB92.append(b_BB92)
	Hausdorff_CP72.append(b_CP72)
	Hausdorff_FP72.append(b_FP72)
	Hausdorff_GE32.append(b_GE32)
	Hausdorff_GL42.append(b_GL42)
	Hausdorff_GP4.append(b_GP4)
	Hausdorff_GS4.append(b_GS4)
	Hausdorff_HA22.append(b_HA22)
	Hausdorff_LD.append(b_LD)
	Hausdorff_LY.append(b_LY)
	Hausdorff_MA113.append(b_MA113)
	Hausdorff_PL52.append(b_PL52)


plt.style.use('ggplot')
# Boxplots for Dice and Hausdorff 
fig, (ax1, ax2) = plt.subplots(2, figsize=(30,15))
BA302_Dice = ax1.boxplot(Dice_BA302[0:int(len(Dice_BA302)/2)], labels=list_oar[0:int(len(list_oar)/2)], positions=np.array(np.arange(len(Dice_BA302[0:int(len(Dice_BA302)/2)])))*2.0-0.9, widths = 0.1)
BB92_Dice = ax1.boxplot(Dice_BB92[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_BB92[0:int(len(Dice_BA302)/2)])))*2.0-0.75, widths = 0.1)
CP72_Dice = ax1.boxplot(Dice_CP72[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_CP72[0:int(len(Dice_BA302)/2)])))*2.0-0.60, widths = 0.1)
FP72_Dice = ax1.boxplot(Dice_FP72[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_FP72[0:int(len(Dice_BA302)/2)])))*2.0-0.45, widths = 0.1)
GE32_Dice = ax1.boxplot(Dice_GE32[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_GE32[0:int(len(Dice_BA302)/2)])))*2.0-0.30, widths = 0.1)
GL42_Dice = ax1.boxplot(Dice_GL42[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_GL42[0:int(len(Dice_BA302)/2)])))*2.0-0.15, widths = 0.1)
GP4_Dice = ax1.boxplot(Dice_GP4[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_GP4[0:int(len(Dice_BA302)/2)])))*2.0+0.0, widths = 0.1)
GS4_Dice = ax1.boxplot(Dice_GS4[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_GS4[0:int(len(Dice_BA302)/2)])))*2.0+0.15, widths = 0.1)
HA22_Dice = ax1.boxplot(Dice_HA22[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_HA22[0:int(len(Dice_BA302)/2)])))*2.0+0.30, widths = 0.1)
LD_Dice = ax1.boxplot(Dice_LD[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_LD[0:int(len(Dice_BA302)/2)])))*2.0+0.45, widths = 0.1)
LY_Dice = ax1.boxplot(Dice_LY[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_LY[0:int(len(Dice_BA302)/2)])))*2.0+0.60, widths = 0.1)
MA113_Dice = ax1.boxplot(Dice_MA113[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_MA113[0:int(len(Dice_BA302)/2)])))*2.0+0.75, widths = 0.1)
PL52_Dice = ax1.boxplot(Dice_PL52[0:int(len(Dice_BA302)/2)],positions=np.array(np.arange(len(Dice_PL52[0:int(len(Dice_BA302)/2)])))*2.0+0.9, widths = 0.1)
[ax1.axvline(2*x+1, color = 'grey', linestyle='-', alpha=0.4) for x in range(0, len(list_oar[0:int(len(Dice_BA302)/2)]))]
#ax1.axhline(y = 0.8, color = 'grey', linestyle = '--', alpha=0.4)
define_box_properties(BA302_Dice, 'red', 'BA302')
define_box_properties(BB92_Dice, 'blue', 'BB92')
define_box_properties(CP72_Dice, 'green', 'CP72')
define_box_properties(FP72_Dice, 'yellow', 'FP72')
define_box_properties(GE32_Dice, 'brown', 'GE32')
define_box_properties(GL42_Dice, 'purple', 'GL42')
define_box_properties(GP4_Dice, 'orange', 'GP4')
define_box_properties(GS4_Dice, 'navy', 'GS4')
define_box_properties(HA22_Dice, 'lime', 'HA22')
define_box_properties(LD_Dice, 'aqua', 'LD')
define_box_properties(LY_Dice, 'crimson', 'LY')
define_box_properties(MA113_Dice, 'chartreuse', 'MA113')
define_box_properties(PL52_Dice, 'royalblue', 'PL52')
ax1.set_ylabel('DSC (-)', fontsize=20)
ax1.set_ylim(0, 1)
ax1.set_xticks(range(0, len(list_oar[0:int(len(list_oar)/2)]) * 2, 2), list_oar[0:int(len(list_oar)/2)], fontsize=15)
BA302_Dice = ax2.boxplot(Dice_BA302[int(len(Dice_BA302)/2):len(Dice_BA302)], labels=list_oar[int(len(list_oar)/2):len(list_oar)], positions=np.array(np.arange(len(Dice_BA302[int(len(Dice_BA302)/2):len(Dice_BA302)])))*2.0-0.9, widths = 0.1)
BB92_Dice = ax2.boxplot(Dice_BB92[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_BB92[int(len(Dice_BA302)/2):len(list_oar)])))*2.0-0.75, widths = 0.1)
CP72_Dice = ax2.boxplot(Dice_CP72[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_CP72[int(len(Dice_BA302)/2):len(list_oar)])))*2.0-0.60, widths = 0.1)
FP72_Dice = ax2.boxplot(Dice_FP72[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_FP72[int(len(Dice_BA302)/2):len(list_oar)])))*2.0-0.45, widths = 0.1)
GE32_Dice = ax2.boxplot(Dice_GE32[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_GE32[int(len(Dice_BA302)/2):len(list_oar)])))*2.0-0.30, widths = 0.1)
GL42_Dice = ax2.boxplot(Dice_GL42[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_GL42[int(len(Dice_BA302)/2):len(list_oar)])))*2.0-0.15, widths = 0.1)
GP4_Dice = ax2.boxplot(Dice_GP4[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_GP4[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.00, widths = 0.1)
GS4_Dice = ax2.boxplot(Dice_GS4[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_GS4[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.15, widths = 0.1)
HA22_Dice = ax2.boxplot(Dice_HA22[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_HA22[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.30, widths = 0.1)
LD_Dice = ax2.boxplot(Dice_LD[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_LD[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.45, widths = 0.1)
LY_Dice = ax2.boxplot(Dice_LY[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_LY[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.60, widths = 0.1)
MA113_Dice = ax2.boxplot(Dice_MA113[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_MA113[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.75, widths = 0.1)
PL52_Dice = ax2.boxplot(Dice_PL52[int(len(Dice_BA302)/2):len(Dice_BA302)],positions=np.array(np.arange(len(Dice_PL52[int(len(Dice_BA302)/2):len(list_oar)])))*2.0+0.9, widths = 0.1)
[ax2.axvline(2*x+1, color = 'grey', linestyle='-', alpha=0.4) for x in range(0, len(list_oar[int(len(Dice_BA302)/2):len(list_oar)-1]))]
#ax2.axhline(y = 0.8, color = 'grey', linestyle = '--', alpha=0.4)
define_box_properties(BA302_Dice, 'red', 'BA302')
define_box_properties(BB92_Dice, 'blue', 'BB92')
define_box_properties(CP72_Dice, 'green', 'CP72')
define_box_properties(FP72_Dice, 'yellow', 'FP72')
define_box_properties(GE32_Dice, 'brown', 'GE32')
define_box_properties(GL42_Dice, 'purple', 'GL42')
define_box_properties(GP4_Dice, 'orange', 'GP4')
define_box_properties(GS4_Dice, 'navy', 'GS4')
define_box_properties(HA22_Dice, 'lime', 'HA22')
define_box_properties(LD_Dice, 'aqua', 'LD')
define_box_properties(LY_Dice, 'crimson', 'LY')
define_box_properties(MA113_Dice, 'chartreuse', 'MA113')
define_box_properties(PL52_Dice, 'royalblue', 'PL52')
ax2.set_ylabel('DSC (-)', fontsize=20)
ax2.set_ylim(0, 1)
ax2.set_xticks(range(0, len(list_oar[int(len(list_oar)/2):len(list_oar)]) * 2, 2), list_oar[int(len(list_oar)/2):len(list_oar)], fontsize=15)
lines, labels = fig.axes[-1].get_legend_handles_labels()
ax2.legend(lines[0:int(len(lines)/2)], labels[0:int(len(labels)/2)], loc = 'lower right', frameon=False, fontsize=12)
fig.savefig("Dice_patient.png")
fig.savefig("Dice_patient.pdf")


fig, (ax1, ax2) = plt.subplots(2, figsize=(30,15))
BA302_HD = ax1.boxplot(Hausdorff_BA302[0:int(len(Hausdorff_BA302)/2)], labels=list_oar[0:int(len(list_oar)/2)], positions=np.array(np.arange(len(Hausdorff_BA302[0:int(len(Hausdorff_BA302)/2)])))*2.0-0.9, widths = 0.1)
BB92_HD = ax1.boxplot(Hausdorff_BB92[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_BB92[0:int(len(Hausdorff_BA302)/2)])))*2.0-0.75, widths = 0.1)
CP72_HD = ax1.boxplot(Hausdorff_CP72[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_CP72[0:int(len(Hausdorff_BA302)/2)])))*2.0-0.60, widths = 0.1)
FP72_HD = ax1.boxplot(Hausdorff_FP72[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_FP72[0:int(len(Hausdorff_BA302)/2)])))*2.0-0.45, widths = 0.1)
GE32_HD = ax1.boxplot(Hausdorff_GE32[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_GE32[0:int(len(Hausdorff_BA302)/2)])))*2.0-0.30, widths = 0.1)
GL42_HD = ax1.boxplot(Hausdorff_GL42[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_GL42[0:int(len(Hausdorff_BA302)/2)])))*2.0-0.15, widths = 0.1)
GP4_HD = ax1.boxplot(Hausdorff_GP4[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_GP4[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.00, widths = 0.1)
GS4_HD = ax1.boxplot(Hausdorff_GS4[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_GS4[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.15, widths = 0.1)
HA22_HD = ax1.boxplot(Hausdorff_HA22[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_HA22[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.30, widths = 0.1)
LD_HD = ax1.boxplot(Hausdorff_LD[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_LD[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.45, widths = 0.1)
LY_HD = ax1.boxplot(Hausdorff_LY[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_LY[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.60, widths = 0.1)
MA113_HD = ax1.boxplot(Hausdorff_MA113[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_MA113[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.75, widths = 0.1)
PL52_HD = ax1.boxplot(Hausdorff_PL52[0:int(len(Hausdorff_BA302)/2)],positions=np.array(np.arange(len(Hausdorff_PL52[0:int(len(Hausdorff_BA302)/2)])))*2.0+0.9, widths = 0.1)
[ax1.axvline(2*x+1, color = 'grey', linestyle='--', alpha=0.5) for x in range(0, len(list_oar[0:int(len(Hausdorff_BA302)/2)]))]
define_box_properties(BA302_HD, 'red', 'BA302')
define_box_properties(BB92_HD, 'blue', 'BB92')
define_box_properties(CP72_HD, 'green', 'CP72')
define_box_properties(FP72_HD, 'yellow', 'FP72')
define_box_properties(GE32_HD, 'brown', 'GE32')
define_box_properties(GL42_HD, 'purple', 'GL42')
define_box_properties(GP4_HD, 'orange', 'GP4')
define_box_properties(GS4_HD, 'navy', 'GS4')
define_box_properties(HA22_HD, 'lime', 'HA22')
define_box_properties(LD_HD, 'aqua', 'LD')
define_box_properties(LY_HD, 'crimson', 'LY')
define_box_properties(MA113_HD, 'chartreuse', 'MA113')
define_box_properties(PL52_HD, 'royalblue', 'PL52')
ax1.set_ylim(0, 100)
ax1.set_ylabel('Hausdorff (-)', fontsize=20)
ax1.set_xticks(range(0, len(list_oar[0:int(len(list_oar)/2)]) * 2, 2), list_oar[0:int(len(list_oar)/2)], fontsize=15)
BA302_HD = ax2.boxplot(Hausdorff_BA302[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)], labels=list_oar[int(len(list_oar)/2):len(list_oar)], positions=np.array(np.arange(len(Hausdorff_BA302[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0-0.9, widths = 0.1)
BB92_HD = ax2.boxplot(Hausdorff_BB92[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_BB92[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0-0.75, widths = 0.1)
CP72_HD = ax2.boxplot(Hausdorff_CP72[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_CP72[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0-0.60, widths = 0.1)
FP72_HD = ax2.boxplot(Hausdorff_FP72[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_FP72[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0-0.45, widths = 0.1)
GE32_HD = ax2.boxplot(Hausdorff_GE32[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_GE32[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0-0.30, widths = 0.1)
GL42_HD = ax2.boxplot(Hausdorff_GL42[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_GL42[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0-0.15, widths = 0.1)
GP4_HD = ax2.boxplot(Hausdorff_GP4[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_GP4[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.00, widths = 0.1)
GS4_HD = ax2.boxplot(Hausdorff_GS4[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_GS4[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.15, widths = 0.1)
HA22_HD = ax2.boxplot(Hausdorff_HA22[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_HA22[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.30, widths = 0.1)
LD_HD = ax2.boxplot(Hausdorff_LD[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_LD[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.45, widths = 0.1)
LY_HD = ax2.boxplot(Hausdorff_LY[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_LY[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.60, widths = 0.1)
MA113_HD = ax2.boxplot(Hausdorff_MA113[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_MA113[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.75, widths = 0.1)
PL52_HD = ax2.boxplot(Hausdorff_PL52[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)],positions=np.array(np.arange(len(Hausdorff_PL52[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)])))*2.0+0.9, widths = 0.1)
[ax2.axvline(2*x+1, color = 'grey', linestyle='-', alpha=0.5) for x in range(0, len(list_oar[int(len(Hausdorff_BA302)/2):len(Hausdorff_BA302)-1]))]
define_box_properties(BA302_HD, 'red', 'BA302')
define_box_properties(BB92_HD, 'blue', 'BB92')
define_box_properties(CP72_HD, 'green', 'CP72')
define_box_properties(FP72_HD, 'yellow', 'FP72')
define_box_properties(GE32_HD, 'brown', 'GE32')
define_box_properties(GL42_HD, 'purple', 'GL42')
define_box_properties(GP4_HD, 'orange', 'GP4')
define_box_properties(GS4_HD, 'navy', 'GS4')
define_box_properties(HA22_HD, 'lime', 'HA22')
define_box_properties(LD_HD, 'aqua', 'LD')
define_box_properties(LY_HD, 'crimson', 'LY')
define_box_properties(MA113_HD, 'chartreuse', 'MA113')
define_box_properties(PL52_HD, 'royalblue', 'PL52')
ax2.set_ylim(0, 100)
ax2.set_ylabel('Hausdorff (-)', fontsize=20)
ax2.set_xticks(range(0, len(list_oar[int(len(list_oar)/2):len(list_oar)]) * 2, 2), list_oar[int(len(list_oar)/2):len(list_oar)], fontsize=15)
lines, labels = fig.axes[-1].get_legend_handles_labels()
ax2.legend(lines[0:int(len(lines)/2)], labels[0:int(len(labels)/2)], loc = 'upper right', frameon=False, fontsize=12)
fig.savefig("Hausdorff_patient.png")
fig.savefig("Hausdorff_patient.pdf")


duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
