# Script to identify and copy in folder the patient's image present in the sCBCT training database 
# to compare the two method with exactly the same images in the training databases

import glob
import os
import sys
import shutil
import numpy as np
import time

start_time = time.time()

# Folder os simulation of sCBCT
simu_folder = '/export/home/qchaine/Stage/Gate_simulations/Simulation_1/simulations/'
patients = sorted(glob.glob(f'{simu_folder}*'))

print(f'Simulation folder :{simu_folder}')
print(f'Number of simulation images : {len(patients)}\n')

# Folder of training database for CT 
CT_folder = '/export/home/qchaine/Images/Database_HN/train_HN/'
CT = sorted(glob.glob(f'{CT_folder}/patient*/input/*'))

files = []

# Creation of folder for saving patient folders 
folder = 'CT_raw_database'
if os.path.exists(folder):
	shutil.rmtree(folder)
os.makedirs(folder)

for patient in patients:
	files.append(patient.replace(f'{simu_folder}', ''))

a = 0
i = 0

# Loop for copying folder of patient present in the sCBCT simulation for the training 
for CTs in CT:
	CTs = CTs.replace(f'{CT_folder}/patient*/input/', '')
	#print(CTs)

	for patient in files:
		if patient in CTs:
			shutil.copytree(f'{CTs}', f'{folder}/{patient}')
			#print('True')
			a += 1
	if i%5 == False:
		print(i)
	i += 1

print('Number of images in CT training database :' , a)

duree = time.time() - start_time
print('\nTotal running time : %5.3g s' % duree)
