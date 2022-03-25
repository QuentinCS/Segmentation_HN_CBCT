# Script to get the results of the inference on test set and calculate Dice and Hausdorff 
# run with : python get_results.py

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

# Calcul of Dice coefficient 
def dice(ar1, ar2):
    im1 = np.asarray(ar1).astype(bool)
    im2 = np.asarray(ar2).astype(bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    # Compute Dice coefficient
    intersection = np.logical_and(im1, im2)

    return 2. * intersection.sum() / (im1.sum() + im2.sum())

# Function to get the key in the dictionnary using the value
def get_key(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None

start_time = time.time()


list_roi = []
directory_name = []
# Travel through directory to get file list 
roiDir = 'Labels2'
for dirName, subdirList, fileList in os.walk(roiDir):
    list_roi.append(fileList)
    directory_name.append(dirName)
directory_name.remove('Labels2')

image_predict = []
predictDir = 'Predictions2'
for dirName, subdirList, fileList in os.walk(predictDir):
    list_predict = fileList
list_predict.remove('plans.pkl')

image = []
for i in range(len(list_predict)):
    image.append(list_predict[i].replace('.nii.gz', ''))

Organs = []
for key, value in dt.Organs_dict.items():
	if value not in Organs:
		Organs.append(value)

directory_name.sort()
image.sort()
list_predict.sort()

print('Organs :', Organs)

# Dictionary for store the data 
Data = {'Number of images': len(image), 'List images': image, 'List Organs': Organs}
print('Number of images :', len(image))

for i in range(len(directory_name)):
	OAR = []
	print("Image :", list_predict[i])
	predict_name = predictDir + '/' + list_predict[i]
	image_predict = itk.imread(predict_name)

	dict_image = {"Name": list_predict[i]}
	Data['Image%s'%(i)] = dict_image
	Dict_dice = {}
	Dict_hausdorff = {}
	for key, value in dt.Organs_dict.items():
		roi_name = directory_name[i] + '/roi_' + key + '.mhd'
		print(roi_name)
		if os.path.isfile(roi_name):
			image_roi_itk = itk.imread(roi_name)
			image_pred1 = itk.array_from_image(image_predict)
			image_pred = image_pred1.copy()
			image_pred.fill(0)
			mask = image_pred1==dt.Label[dt.Organs_dict[key]]
			image_pred[mask] = 1
			image_pred_itk1 = itk.image_from_array(image_pred)
			image_pred_itk = gt.applyTransformation(input=image_pred_itk1, like=image_roi_itk) # Reset to the correct origin 			
			itk.imwrite(image_pred_itk,  "Test.nii" )			

			if np.mean(image_pred_itk1) > 0:
				# Dice coefficient 
				Dice = dice(image_roi_itk, image_pred)
				Dict_dice[dt.Organs_dict[key]] = Dice
			
				# Hausdorff
				Hausdorff = gt.computeHausdorff(image_roi_itk, image_pred_itk, 0.95)
				Dict_hausdorff[dt.Organs_dict[key]] = Hausdorff
			
				if dt.Organs_dict[key] not in OAR and os.path.isfile(roi_name):
					OAR.append(dt.Organs_dict[key])
	
	# Put data in Dictionaries	
	Data['Image%s'%(i)]['Organs'] = OAR
	Data['Image%s'%(i)]['Dice'] = Dict_dice
	Data['Image%s'%(i)]['Hausdorff'] = Dict_hausdorff


# Save result to json 
with open("result.json", 'w') as outfile:
	json.dump(Data, outfile, indent=4)

duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)


######################################
#############  TEST  #################
######################################

"""
	if os.path.isfile(directory_name[i] + '/' + 'roi_ParotidR.mhd'):
			image_2 = itk.imread(directory_name[i] + '/' + 'roi_ParotidR.mhd')
			Dice = dice(image2, image_2)
			#print("Dice Parotid right : ", Dice)
			dice_parotidr.append(Dice)	
			Dict_dice['ParotidR'] = Dice
		if os.path.isfile(directory_name[i] + '/' + 'roi_ParotidL.mhd'): 
			image_3 = itk.imread(directory_name[i] + '/' + 'roi_ParotidL.mhd')
			Dice = dice(image3, image_3)
			#print("Dice Parotid left : ", Dice)
			dice_parotidl.append(Dice)	
			Dict_dice['ParotidL'] = Dice
		if os.path.isfile(directory_name[i] + '/' + 'roi_Larynx.mhd'):
			image_4 = itk.imread(directory_name[i] + '/' + 'roi_Larynx.mhd')
			Dice = dice(image4, image_4)
			#print("Dice Larynx: ", Dice)
			dice_larynx.append(Dice)
			Dict_dice['Larynx'] = Dice
		if os.path.isfile(directory_name[i] + '/' + 'roi_Brainstem.mhd'):
			image_5 = itk.imread(directory_name[i] + '/' + 'roi_Brainstem.mhd')
			Dice = dice(image5, image_5)
			#print("Dice Brainstem: ", Dice)
			dice_brainstem.append(Dice)
			Dict_dice['Brainstem'] = Dice
"""






"""
	for key, value in dt.Organs_dict.items():
		roi_name = directory_name[i] + '/roi_' + value + '.mhd'
		print(roi_name)
		if os.path.isfile(roi_name):
			image_roi_itk = itk.imread(roi_name)
			image_pred1 = itk.array_from_image(image_predict)
			#image_pred = np.where(image_pred1==dt.Label[key], dt.Label[key], 0)
			image_pred = image_pred1.copy()
			image_pred.fill(0)
			mask = image_pred1==dt.Label[key]
			image_pred[mask] = dt.Label[key]
			image_pred_itk = itk.image_from_array(image_pred)
			
			# Dice coefficient 
			Dice = dice(image_roi_itk, image_pred)
			Dict_dice[get_key(dt.Organs_dict, value)] = Dice
			
			# Hausdorff
			Hausdorff = gt.computeHausdorff(image_roi_itk, image_pred_itk, 0.95)
			Dict_hausdorff[get_key(dt.Organs_dict, value)] = Hausdorff
			
			if get_key(dt.Organs_dict, value) not in OAR and os.path.isfile(roi_name):
				OAR.append(get_key(dt.Organs_dict, value))
	

"""







