# Script to combine the Larynx and the trachea within the same image for the Labels

import gatetools as gt
import numpy as np
import matplotlib.pyplot as plt
import difflib as di
from os import listdir
from os.path import isfile, join
import os
import shutil as sh
import time
import itk

start_time = time.time()


list_roi = []
directory_name = []
# Travel through directory to get file list of OARs for each images
roiDir = '.'
for dirName, subdirList, fileList in os.walk(roiDir):
    list_roi.append(fileList)
    directory_name.append(dirName)


print(directory_name)
#print(list_roi)

for i in range(len(directory_name)):
	print("Image :", list_roi[i])
	
	if os.path.isfile(directory_name[i] + '/roi_Trachea.mhd'): 
		if os.path.isfile(directory_name[i] + '/roi_Larynx.mhd'):
			image_itk_larynx = itk.imread(directory_name[i] + '/roi_Larynx.mhd')
			image_np_larynx = itk.array_from_image(image_itk_larynx)
			image_itk_trachea = itk.imread(directory_name[i] + '/roi_Trachea.mhd')
			image_np_trachea = itk.array_from_image(image_itk_trachea)
			image_comb = image_np_larynx.copy()
			image_comb.fill(0)
			larynx = image_np_larynx>0
			trachea = image_np_trachea>0
			image_comb[larynx] = 1 
			image_comb[trachea] = 1	
			image_comb_itk1 = itk.image_from_array(image_comb)
			image_comb_itk = gt.applyTransformation(input=image_comb_itk1, like=image_itk_larynx) # Reset to the correct origin 			
			itk.imwrite(image_comb_itk, directory_name[i] + '/roi_Larynx-Trachea.mhd')
		else:
			if os.path.isfile(directory_name[i] + '/roi_Larynx1.mhd'):
				image_itk_larynx = itk.imread(directory_name[i] + '/roi_Larynx1.mhd')
				image_np_larynx = itk.array_from_image(image_itk_larynx)
				image_itk_trachea = itk.imread(directory_name[i] + '/roi_Trachea.mhd')
				image_np_trachea = itk.array_from_image(image_itk_trachea)
				image_comb = image_np_larynx.copy()
				image_comb.fill(0)
				larynx = image_np_larynx>0
				trachea = image_np_trachea>0
				image_comb[larynx] = 1 
				image_comb[trachea] = 1	
				image_comb_itk1 = itk.image_from_array(image_comb)
				image_comb_itk = gt.applyTransformation(input=image_comb_itk1, like=image_itk_larynx) # Reset to the correct origin 			
				itk.imwrite(image_comb_itk, directory_name[i] + '/roi_Larynx-Trachea.nii')
			else:
				image_itk_Trachea = itk.imread(directory_name[i] + '/roi_Trachea.mhd')
				itk.imwrite(image_itk_Trachea, directory_name[i] + '/roi_Larynx-Trachea.mhd')

	else:
		if os.path.isfile(directory_name[i] + '/roi_Larynx.mhd'):
			image_itk_larynx = itk.imread(directory_name[i] + '/roi_Larynx.mhd')
			itk.imwrite(image_itk_larynx,  directory_name[i] + '/roi_Larynx-Trachea.mhd')
		if os.path.isfile(directory_name[i] + '/roi_Larynx1.mhd'):
			image_itk_larynx = itk.imread(directory_name[i] + '/roi_Larynx1.mhd')
			itk.imwrite(image_itk_larynx, directory_name[i] + '/roi_Larynx-Trachea.mhd')


duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)

