# Test to run the reconstruction of the scbct 10 images per 10 images

import glob
import os
import sys
import shutil
import numpy as np

patients = sorted(glob.glob('simulations/*'))
#print(patients)

simu = 0
Nb_end = 0
Nb_start = 0

for patient in patients:

	files = (glob.glob(f'{patient}/*'))
	if os.path.exists(f'{patient}/reconstruct'):
		Nb_end += 1
	else:
		Nb_start += 1

for patient in patients:

	# go to patient simulation folder and run the simulations jobs
	main_path=os.getcwd()
	files = (glob.glob(f'{patient}/*'))
	os.chdir(patient)
	if os.path.exists(f'reconstruct'):
		os.chdir(main_path)
		continue

	shutil.copyfile('../../combine_primary_scatter.py', 'combine_primary_scatter.py')
	print(patient)

	# run the simulations
	reconstruct = f'python combine_primary_scatter.py'
	os.system(reconstruct)

	os.chdir(main_path)
	simu += 1

	if simu==10:
		break
	print('\n')

print(f'\n-----------------------------------------------')
print(f'{Nb_end} reconstruction finished\n')
print(f'{Nb_start} remaining reconstruction\n')
