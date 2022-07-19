# Script to combine inferences for OARs when training separately for eah oar 
# Also multiple similar label and keep the biggest

import gatetools as gt
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import euler_number, label
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
import SimpleITK as sitk

# function to calculate the volume of labels

def volume_calculation(image_0, image, label):
	image_np = sitk.GetArrayFromImage(image)
	mask_oar = image_np.copy()
	mask_oar.fill(0)
	mask = image_np==label
	mask_oar[mask] = 1
	volume = np.sum(mask_oar != 0)*(0.1*image_0.GetSpacing()[0]*0.1*image_0.GetSpacing()[1]*0.1*image_0.GetSpacing()[2])
 
	return volume

start_time = time.time()

Pred = 'Predictions_combine'
if os.path.exists(Pred):
    sh.rmtree(Pred)
os.makedirs(Pred)

directory_name = []
list_images = []
# Travel through directory to get file list 
rootDir = '/export/home/qchaine/Stage/Stage_CREATIS/Database_Test_sCT/CT/CT/'
#rootDir = 'Labels/'
for dirName, subdirList, fileList in os.walk(rootDir):
		directory_name.append(dirName)
		list_images = fileList
list_images.sort()

for i in range(len(list_images)):
	list_images[i] = list_images[i][:-12]
	list_images[i] += '.nii.gz'

print(list_images)
#print(directory_name)
Nb_images = len(list_images)

cca = sitk.ConnectedComponentImageFilter()

for image in range(Nb_images):

############################# Spinal Cord #########################################

	prediction = 'SpinalCord/Predictions/'
	image_itk = sitk.ReadImage(prediction + list_images[image])
	#print(prediction + list_images[image])

	image_np = sitk.GetArrayFromImage(image_itk)
	image_comb = image_np.copy()	
	image_comb.fill(0)

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Spinal cord')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		spinal = image_np2==main_label

	else:
		spinal = image_np==2

	patient = image_np==1
	image_comb[patient] = 1
	image_comb[spinal] = 6

############################# Thyroid #########################################

	prediction = 'Thyroid/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 2:
		vol = 0
		print('Separate labels : thyroid')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		thyroid = image_np2==main_label
	else:
		thyroid = image_np==2

	image_comb[thyroid] = 8

############################# Larynx Trachea #########################################

	prediction = 'LarynxTrachea/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Larynx Trachea')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		larynxtrachea = image_np2==main_label
	else:
		larynxtrachea = image_np==2

	image_comb[larynxtrachea] = 10
	
############################# Parotid glands #########################################

	prediction = 'Parotids/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Parotid D')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		parotid_d = image_np2==main_label
	else:
		parotid_d  = image_np==2


	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==3
	image_np1[mask] = 3
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Parotid G')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		parotid_g = image_np2==main_label
	else:
		parotid_g  = image_np==3

	image_comb[parotid_d] = 2
	image_comb[parotid_g] = 3
	
############################# Brainstem #########################################

	prediction = 'Brainstem/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Brainstem')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		brainstem = image_np2==main_label
	else:
		brainstem = image_np==2

	image_comb[brainstem] = 4

############################# Esophagus #########################################
	
	prediction = 'Esophagus/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Esophagus')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		esophagus = image_np2==main_label
	else:
		esophagus = image_np==2

	image_comb[esophagus] = 7

############################# Submandibular glands #########################################
	
	prediction = 'Submandibular/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Submand D')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		submand_d = image_np2==main_label
	else:
		submand_d = image_np==2

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==3
	image_np1[mask] = 3
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Submand G')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		submand_g= image_np2==main_label
	else:
		submand_g = image_np==3

	image_comb[submand_d] = 11
	image_comb[submand_g] = 12
	
############################# Mandible #########################################

	prediction = 'Mandible/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)
	
	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Mandible')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		mandible = image_np2==main_label
	else:
		mandible = image_np==2

	image_comb[mandible] = 9

############################# Oral Cavity #########################################
	
	prediction = 'OralCavity/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Oral Cavity')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		oralcavity = image_np2==main_label
	else:
		oralcavity = image_np==2

	image_comb[oralcavity] = 5

############################# Eyes #########################################

	prediction = 'Eyes/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Eye R')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		eye_R = image_np2==main_label
	else:
		eye_R = image_np==2

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==3
	image_np1[mask] = 3
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Eye L')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		eye_L = image_np2==main_label
	else:
		eye_L = image_np==3

	image_comb[eye_R] = 13
	image_comb[eye_L] = 14

############################# Optic nerves #########################################
	
	prediction = 'OpticNerves/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==2
	image_np1[mask] = 2
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Optic nerve R')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		Optn_R = image_np2==main_label
	else:
		Optn_R = image_np==2

	image_np1 = image_np.copy()
	image_np1.fill(0)
	mask = image_np==3
	image_np1[mask] = 1
	image_2 = sitk.GetImageFromArray(image_np1)
	image_2 = cca.Execute(image_2)
	image_np2 = sitk.GetArrayFromImage(image_2)

	if np.max(image_np2) > 1:
		vol = 0
		print('Separate labels : Optic nerve L')
		for i in range(1, np.max(image_np2)):
			volume = volume_calculation(image_itk, image_2, i)
			if volume > vol:
				vol = volume	
				main_label = i
		Optn_L = image_np2==main_label
	else:
		Optn_L = image_np==3

	image_comb[Optn_R] = 15
	image_comb[Optn_L] = 16
	
	
	save = itk.image_from_array(image_comb)
	save.CopyInformation(image_itk) # Important to save the image with correct spacing, size!!
	itk.imwrite(save, Pred + '/' + list_images[image] + '.nii.gz')

	if (image)%5 == False:
		print(image)


duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
