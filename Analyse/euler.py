# Script to compute the Euler number, object number and hole number for the organs separately to check validity 
# Save outliers in text file  

import gatetools as gt
from skimage.measure import euler_number, label
import numpy as np
import matplotlib.pyplot as plt
import time
import oar
import sys
import itk
import gzip
import os
	
start_time = time.time()

images = []

# Travel through directory to get file list 
rootDir = 'Predictions'
for dirName, subdirList, fileList in os.walk(rootDir):
        images.append(fileList)
print(fileList, '\n')

outlier = 0
list_out = []

for i in range(len(fileList)):
	print(fileList[i])
	for key, value in oar.Label.items():
		if key != 'Background' and key != 'Patient':
			#print(key)		
			image_itk = itk.imread('Predictions/' + fileList[i])
			image_np = itk.array_view_from_image(image_itk)
			organ = image_np.copy()
			organ.fill(0)
			mask = image_np==oar.Label[key]	
			organ[mask] = 1

			euler = euler_number(organ, connectivity=1)
			objet = label(organ).max()
			trou = objet - euler 
			
			if euler != 0 and euler !=1 and key != 'Thyroide':
				outlier += 1
				list_out.append('%s : %s '%(fileList[i], key))
			if euler!=2 and key == 'Thyroide':
				outlier += 1
				list_out.append('%s : %s '%(fileList[i], key))
				 
			
			"""
			print('Euler number : %i'%(euler))
			print('Object number : %i'%(objet))
			print('Hole number : %i'%(trou))
			print('------------------------\n')
			"""
	#print('\n \n')

print('Outliers :', outlier)

save = open("Outliers.txt", "w")
for i in range(len(list_out)):
	save.write(list_out[i])
	save.write("\n")
save.close()


duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
