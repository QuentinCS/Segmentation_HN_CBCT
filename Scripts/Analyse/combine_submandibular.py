# Script to combine the submandibular glands within the same image for the Labels

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
	
	if os.path.isfile(directory_name[i] + '/roi_GlndSubmandL.mhd'): 
		if os.path.isfile(directory_name[i] + '/roi_GlndSubmandR.mhd'):
			image_itk_subR = itk.imread(directory_name[i] + '/roi_GlndSubmandR.mhd')
			image_np_subR = itk.array_from_image(image_itk_subR)
			image_itk_subL = itk.imread(directory_name[i] + '/roi_GlndSubmandL.mhd')
			image_np_subL = itk.array_from_image(image_itk_subL)
			image_comb = image_np_subR.copy()
			image_comb.fill(0)
			subR = image_np_subR>0
			subL = image_np_subL>0
			image_comb[subR] = 1 
			image_comb[subL] = 1	
			image_comb_itk1 = itk.image_from_array(image_comb)
			image_comb_itk = gt.applyTransformation(input=image_comb_itk1, like=image_itk_subR) # Reset to the correct origin 			
			itk.imwrite(image_comb_itk, directory_name[i] + '/roi_SubMandGlands.mhd')
		else:
			image_itk_sub = itk.imread(directory_name[i] + '/roi_GlndSubmandL.mhd')
			itk.imwrite(image_itk_sub,  directory_name[i] + '/roi_SubMandGlands.mhd')

	else:
		if os.path.isfile(directory_name[i] + '/roi_GlndSubmandR.mhd'):
			image_itk_sub = itk.imread(directory_name[i] + '/roi_GlndSubmandR.mhd')
			itk.imwrite(image_itk_sub,  directory_name[i] + '/roi_SubMandGlands.mhd')


duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)

