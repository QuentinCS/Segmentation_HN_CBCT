# Test to run the reconstruction of the scbct 10 images per 10 images

import glob
import os
import sys
import shutil
import numpy as np

patients = sorted(glob.glob('simulations/*'))
#print(patients)

simu = 0

for patient in patients:

	# go to patient simulation folder and run the simulations jobs
	main_path=os.getcwd()
	files = (glob.glob(f'{patient}/*'))
	os.chdir(patient)
	print(patient)

	# run the simulations
	reconstruct = f'python combine_primary_scatter.py'
	os.system(reconstruct)

	os.chdir(main_path)
	simu += 1

	if simu==10:
		break
	print('\n')
