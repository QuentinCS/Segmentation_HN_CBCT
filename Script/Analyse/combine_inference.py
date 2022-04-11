# Script to combine inferences for OARs when training separately for eah oar 

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

start_time = time.time()

Pred = 'Predictions_combine'
if os.path.exists(Pred):
    sh.rmtree(Pred)
os.makedirs(Pred)

directory_name = []
list_images = []
# Travel through directory to get file list 
rootDir = '/export/home/qchaine/Stage/Stage_CREATIS/Database_Test_sCT/Labels/'
for dirName, subdirList, fileList in os.walk(rootDir):
	if len(fileList) > 6:
		directory_name.append(dirName)
		list_images.append(dirName.replace(rootDir, ''))
list_images.sort()

print(list_images)
#print(directory_name)
Nb_images = len(list_images)

for image in range(Nb_images):
	prediction = '/export/home/qchaine/nnUnet/nnUNet/nnUNet_trained_models/nnUNet/3d_fullres/Task526_SpinalCord/nnUNetTrainerV2_noMirroring__nnUNetPlansv2.1/fold_0/Analyse/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)
	image_comb = image_np.copy()	
	image_comb.fill(0)
	patient = image_np==1
	spinal = image_np==2
	image_comb[patient] = 1
	image_comb[spinal] = 6

	prediction = '/export/home/qchaine/nnUnet/nnUNet/nnUNet_trained_models/nnUNet/3d_fullres/Task522_Thyroide_only/nnUNetTrainerV2_noMirroring__nnUNetPlansv2.1/fold_0/Analyse/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)
	thyroid = image_np==2
	image_comb[thyroid] = 8
	
	prediction = '/export/home/qchaine/nnUnet/nnUNet/nnUNet_trained_models/nnUNet/3d_fullres/Task523_LarynxTrachea/nnUNetTrainerV2_noMirroring__nnUNetPlansv2.1/fold_0/Analyse/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)
	larynxtrachea = image_np==2
	image_comb[larynxtrachea] = 10
	
	prediction = '/export/home/qchaine/nnUnet/nnUNet/nnUNet_trained_models/nnUNet/3d_fullres/Task524_Parotids/nnUNetTrainerV2_noMirroring__nnUNetPlansv2.1/fold_0/Analyse/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)
	parotid_d = image_np==2
	parotid_g = image_np==3
	image_comb[parotid_d] = 2
	image_comb[parotid_g] = 3
	
	prediction = '/export/home/qchaine/nnUnet/nnUNet/nnUNet_trained_models/nnUNet/3d_fullres/Task525_Brainstem/nnUNetTrainerV2_noMirroring__nnUNetPlansv2.1/fold_0/Analyse/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)
	brainstem = image_np==2
	image_comb[brainstem] = 4
	
	prediction = '/export/home/qchaine/nnUnet/nnUNet/nnUNet_trained_models/nnUNet/3d_fullres/Task527_Esophagus/nnUNetTrainerV2_noMirroring__nnUNetPlansv2.1/fold_0/Analyse/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)
	esophagus = image_np==2
	image_comb[larynxtrachea] = 7
	
	prediction = '/export/home/qchaine/nnUnet/nnUNet/nnUNet_trained_models/nnUNet/3d_fullres/Task528_SubMandibularGlands/nnUNetTrainerV2_noMirroring__nnUNetPlansv2.1/fold_0/Analyse/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)
	submand_d = image_np==2
	submand_g = image_np==3
	image_comb[submand_d] = 11
	image_comb[submand_g] = 12
	
	prediction = '/export/home/qchaine/nnUnet/nnUNet/nnUNet_trained_models/nnUNet/3d_fullres/Task529_Mandible/nnUNetTrainerV2_noMirroring__nnUNetPlansv2.1/fold_0/Analyse/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)
	mandible = image_np==2
	image_comb[mandible] = 9
	
	prediction = '/export/home/qchaine/nnUnet/nnUNet/nnUNet_trained_models/nnUNet/3d_fullres/Task530_OralCavity/nnUNetTrainerV2_noMirroring__nnUNetPlansv2.1/fold_0/Analyse/Predictions/'
	image_itk = itk.imread(prediction + list_images[image])
	image_np = itk.array_view_from_image(image_itk)
	oralcavity = image_np==2
	image_comb[oralcavity] = 5
	
	save = itk.image_from_array(image_comb)
	save.CopyInformation(image_itk) # Important to save the image with correct spacing, size!!
	itk.imwrite(save, Pred + '/' + list_images[image] + '.nii.gz')

	if (image)%5 == False:
		print(image)


duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
