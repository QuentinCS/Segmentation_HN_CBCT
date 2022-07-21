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
	
	# Find indices where the condition is met
	image_np1 = itk.array_from_image(ar1)
	pixel_min1 = 0
	pixel_max1 = 0
	Sum = np.zeros(np.shape(image_np1)[0])
	#print('Size: ', np.shape(image_np1)[0])
	for i in range(0, np.shape(image_np1)[0]):
		Sum[i] = image_np1[i].sum()	
		if Sum[i] !=0 and Sum[i-1]==0:
			pixel_min1 = i
		if Sum[i] ==0 and Sum[i-1]!=0:
			pixel_max1 = i-1

	image_np2 = ar2.copy()
	pixel_min2 = 0
	pixel_max2 = 0
	Sum = np.zeros(np.shape(image_np2)[0])
	#print('Size: ', np.shape(image_np2)[0])
	for i in range(0, np.shape(image_np2)[0]):
		Sum[i] = image_np2[i].sum()	
		if Sum[i] !=0 and Sum[i-1]==0:
			pixel_min2 = i
		if Sum[i] ==0 and Sum[i-1]!=0:
			pixel_max2 = i-1

	if pixel_min1 == pixel_min2 and pixel_max1 == pixel_max2:

		im1 = np.asarray(image_np1).astype(bool)
		im2 = np.asarray(image_np2).astype(bool)
		if im1.shape != im2.shape:
			raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

		# Compute Dice coefficient
		intersection = np.logical_and(im1, im2)

		return 2. * intersection.sum() / (im1.sum() + im2.sum())

	else:
		print('Rescaling labels')
		if pixel_min1 > pixel_min2:
			pixel_min = pixel_min2
		else:	
			pixel_min = pixel_min1

		if pixel_max1 > pixel_max2:
			pixel_max = pixel_max2
		else:	
			pixel_max = pixel_max1

		for i in range(0, np.shape(image_np1)[0]):
			if i < pixel_min or i > pixel_max:
				for j in range(np.shape(image_np1)[1]):
					for k in range(np.shape(image_np1)[2]):
						image_np1[i][j][k] = 0
						image_np2[i][j][k] = 0

		im1 = np.asarray(image_np1).astype(bool)
		im2 = np.asarray(image_np2).astype(bool)
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
# Travel through directory to get file list of OARs for each images
roiDir = '/export/home/qchaine/Stage/Database_Test_sCT/sCT/Labels'
for dirName, subdirList, fileList in os.walk(roiDir):
    list_roi.append(fileList)
    directory_name.append(dirName)
directory_name.remove('/export/home/qchaine/Stage/Database_Test_sCT/sCT/Labels')

# Travel through directory to get file list of predictions
image_predict = []
predictDir = 'Predictions_combine'
for dirName, subdirList, fileList in os.walk(predictDir):
    list_predict = fileList
if 'plans.pkl' in list_predict:
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
#print(directory_name)

# Dictionary for store the data 
Data = {'Number of images': len(image), 'List images': image, 'List Organs': Organs}
print('Number of images :', len(image))

for i in range(len(image)):
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
		#roi_name = list_predict[i][:-7] + '/roi_' + key + '.mhd' # Test 
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
	
			if np.mean(image_pred_itk1) > 0:
				# Dice coefficient 
				Dice = dice(image_roi_itk, image_pred)
				Dict_dice[dt.Organs_dict[key]] = Dice
				#print('Dice : ', Dice)
			
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
with open("result_sCT.json", 'w') as outfile:
	json.dump(Data, outfile, indent=4)

duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)

