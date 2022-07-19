# Script to check the number of connected componnent (cc) for training database  

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
import json
import SimpleITK as sitk

start_time = time.time()

Dir = ['Brainstem_only/Task525_Brainstem', 'Esophagus_only/Task527_Esophagus', 'Eyes_only/Task532_Eyes', 'LarynxTrachea/Task523_LarynxTrachea', 'Mandible_only/Task529_Mandible', 'OralCavity_only/Task530_OralCavity', 'Parotids_only/Task530_OralCavity', 'SpinalCord_only/Task526_SpinalCord', 'SubMandibularGlands_only/Task528_SubMandibularGlands', 'Thyroide_only/Task522_Thyroide_only']

for i in range(len(Dir)):
	# Variables
	directory_name = []

	# Travel through directory to get file list 
	rootDir = Dir[1] + '/labelsTr/'
	for dirName, subdirList, fileList in os.walk(rootDir):
		directory_name.append(dirName)

	fileList.sort()

	cca = sitk.ConnectedComponentImageFilter()
	n_cc_eso = []
	n_cc_spi = []
	n_cc_par = []
	n_cc_bra = []
	n_cc_thy = []
	n_cc_lartra = []
	n_cc_ora = []
	n_cc_man = []
	n_cc_eye = []
	n_cc_sub = []

	for i in range(len(fileList)):
		#print(fileList[i])
		dict_volume = {}
		image_itk = itk.imread(rootDir + fileList[i])
		image_np = itk.array_from_image(image_itk)

		for key, value in dt.Label.items():
			if key != 'Background':
				#print(key)
				mask_oar = image_np.copy()
				mask_oar.fill(0)
				#mask = image_np==dt.Label[key]
				mask = image_np==2
				mask_oar[mask] = 1

				image = sitk.GetImageFromArray(mask_oar)
				image = cca.Execute(image)
				image_np2 = sitk.GetArrayFromImage(image)
				if key == 'Parotide_D' or key == 'Parotide_G':
					n_cc_par.append(np.max(image_np2))
				if key == 'Tronc_Cerebral':
					n_cc_bra.append(np.max(image_np2))
				if key == 'Cavite_Buccale':
					n_cc_ora.append(np.max(image_np2))
				if key == 'Moelle':
					n_cc_spi.append(np.max(image_np2))
				if key == 'Oesophage':
					n_cc_eso.append(np.max(image_np2))
				if key == 'Mandibule':
					n_cc_man.append(np.max(image_np2))
				if key == 'Thyroide':
					n_cc_thy.append(np.max(image_np2))
				if key == 'Larynx-Trachee':
					n_cc_lartra.append(np.max(image_np2))
				if key == 'SubMandD' or key == 'SubMandG':
					n_cc_sub.append(np.max(image_np2))
				if key == 'Oeil_D' or key == 'Oeil_G':
					n_cc_eye.append(np.max(image_np2))


	if i%5 == False:
		print(i)
	#print('\n\n')

print('Parotids :', n_cc_par)
print('Tronc_Cerebral :', n_cc_bra)
print('Moelle :', n_cc_spi)
print('Cavité Buccale :', n_cc_ora)
print('Oesophage :', n_cc_eso)
print('Mandibule :', n_cc_man)
print('Thyroide :', n_cc_thy)
print('Larynx Trachée :', n_cc_lartra)
print('SubMandibulars :', n_cc_sub)
print('Yeux :', n_cc_eye)


duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
