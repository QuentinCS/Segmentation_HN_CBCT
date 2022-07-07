# Test to run the simulation 10 images per 10 images

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
	if len(files) == 3:
		Nb_start += 1
	if len(files) != 3:
		Nb_end += 1

for patient in patients:

	# go to patient simulation folder and run the simulations jobs
	main_path=os.getcwd()
	files = (glob.glob(f'{patient}/*'))
	os.chdir(patient)
	if len(files) != 3:
		os.chdir(main_path)
		continue
	os.system('ls')
	print(patient)

	# run the simulations
	primary = 'gate_split_and_run.py -j 1 mac/primary-patient.mac'
	os.system(primary)
	scatter = f'gate_split_and_run.py -j 1 mac/scatter-patient.mac'
	os.system(scatter)

	os.chdir(main_path)
	simu += 1

	if simu==10:
		break
	print('\n\n')

print(f'\n-----------------------------------------------')
print(f'{Nb_end} simulations finished\n')
print(f'{Nb_start} remaining simulations\n')
