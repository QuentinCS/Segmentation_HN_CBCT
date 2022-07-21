# Script to compute volumes of organs at risks for test set and compare to labels.
# Images in folders prediction and labels

import gatetools as gt
import numpy as np
import matplotlib.pyplot as plt
import difflib as di
from os import listdir
from os.path import isfile, join
import os
import shutil as sh
import oar as dt
import re
import time
import sys
import itk
import gzip
import json
#from scipy import stats 
import scipy.stats as stats

def volume_calculation(directory, list_images):
	dict_result = {'Number of image ': len(fileList)}
	
	for i in range(len(list_images)):
		dict_volume = {}
		image_itk = itk.imread(directory + list_images[i])
		image_np = itk.array_from_image(image_itk)
		for key, value in dt.Label.items():
			if key != 'Background':
				mask_oar = image_np.copy()
				mask_oar.fill(0)
				mask = image_np==dt.Label[key]
				mask_oar[mask] = 1
				#print(dt.Label[key])
				volume = np.sum(mask_oar != 0)*(0.1*image_itk.GetSpacing()[0]*0.1*image_itk.GetSpacing()[1]*0.1*image_itk.GetSpacing()[2])
				dict_volume[key] = volume
				#print("OAR :", key,  ", Surface :", dict_volume[key], " cm^3")

		dict_result['Image_%s'%(i)] = dict_volume
		if i%5 == False:
			print(i)
	return dict_result



start_time = time.time()

predictions = 'Predictions_combine/'
labels = '/export/home/qchaine/Stage/Database_Test_sCT/Labels/'

list_organs = []
for key, value in dt.Label.items():
	if key != 'Background':
		list_organs.append(key)

# Variables
directory = 0
directory_name = []

# Travel through directory to get file list for the prediction
for dirName, subdirList, fileList in os.walk(predictions):
    directory += 1
    directory_name.append(dirName)

fileList.sort()
if 'plans.pkl' in fileList:
	fileList.remove('plans.pkl')

images = []
for i in range(len(fileList)):
	images.append(fileList[i][:-7])

Volume_pred = volume_calculation(predictions, images)

# Dict to save the results 
Volume_label = {'Number of image ': len(fileList)}

for i in range(len(images)):
	dict_volume = {}
	OAR = []
	for key, value in dt.Organs_dict.items():
		roi_name = labels + images[i] + '/roi_' + key + '.mhd'
		if os.path.isfile(roi_name):
			image_itk = itk.imread(roi_name)
			image_np = itk.array_from_image(image_itk)
			#print(roi_name)
			volume = np.sum(image_np != 0)*(0.1*image_itk.GetSpacing()[0]*0.1*image_itk.GetSpacing()[1]*0.1*image_itk.GetSpacing()[2])
			#print("OAR : ", dt.Organs_dict[key], ", volume : " , volume)
			dict_volume[dt.Organs_dict[key]] = volume
			OAR.append(dt.Organs_dict[key])
		if os.path.isfile(roi_name) == False and dt.Organs_dict[key] not in OAR:
			dict_volume[dt.Organs_dict[key]] = 0
	Volume_label['Image_%s'%(i)] = dict_volume
	if i%5 == False:
		print(i)

# Save result to json 
with open("volume_prediction.json", 'w') as outfile:
	json.dump(Volume_pred, outfile, indent=4)
with open("volume_label.json", 'w') as outfile:
	json.dump(Volume_label, outfile, indent=4)


Vol_pred_raw = np.zeros((len(images), len(list_organs)))
Vol_label_raw = np.zeros((len(images), len(list_organs)))
Vol_pred = []
Vol_label = []

for i in range(len(fileList)):
	for oar in range(0, len(list_organs)):
		Vol_pred_raw[i][oar] = float(Volume_pred['Image_%s'%(i)]['%s'%(list_organs[oar])])
		Vol_label_raw[i][oar] = float(Volume_label['Image_%s'%(i)]['%s'%(list_organs[oar])])

for oar in range(0, len(list_organs)):
	a = []
	b = []
	for i in range(len(fileList)):
		# To compare only if two labels are present
		if Vol_pred_raw[i][oar] != 0 and Vol_label_raw[i][oar] !=0: 
			a.append(Vol_pred_raw[i][oar])					
			b.append(Vol_label_raw[i][oar])					
	Vol_pred.append(a)
	Vol_label.append(b)

Ecart_vol = []
for oar in range(0, len(list_organs)):
	a = np.zeros(len(Vol_pred[oar]))		
	for i in range(len(Vol_pred[oar])):
		a[i] = (Vol_pred[oar][i] - Vol_label[oar][i])/Vol_label[oar][i]
	Ecart_vol.append(a)

# Statistical t-test fo similarity of the samples 
save = open("Results_test.txt", "w")
for oar in range(0, len(list_organs)):
	print(list_organs[oar], "Test : ", stats.ttest_ind(Vol_pred[oar], Vol_label[oar], equal_var=False))
	save.write("%s Test : %s\n"%(list_organs[oar], stats.ttest_ind(Vol_pred[oar], Vol_label[oar], equal_var=False)))
save.close()


# Plot histogramms for each OAR
fig=plt.figure(figsize=(20, 15))
for oar in range(1, len(list_organs)+1):
	plt.subplot(2, int(len(list_organs)/2), oar)
	plt.suptitle('Volume of Organs at risks in labels')
	plt.hist(Vol_pred[oar-1], label='Predictions \nN = %i \nMean = %.2f \nStd = %.2f\n-------------'%(len(Vol_pred[oar-1]), np.mean(Vol_pred[oar-1]), np.std(Vol_pred[oar-1])), color='red')
	plt.hist(Vol_label[oar-1], label='Labels \nN = %i \nMean = %.2f \nStd = %.2f'%(len(Vol_label[oar-1]), np.mean(Vol_label[oar-1]), np.std(Vol_label[oar-1])), color='navy', alpha=0.5)
	plt.title(list_organs[oar-1])
	plt.xlabel('V ($cm^3$)', fontsize=8)
	if oar == 1 or oar == (int(len(list_organs)/2)+1):
		plt.ylabel('dN/dV', fontsize=10)
	plt.legend()
plt.show()
fig.savefig('Volume_comparison_oar.pdf')


# Plot histogramms for each OAR
fig=plt.figure(figsize=(20, 15))
for oar in range(1, len(list_organs)+1):
	plt.subplot(2, int(len(list_organs)/2), oar)
	plt.suptitle('Relative gap in Volume of Organs at risks in test set from labels')
	plt.hist(Ecart_vol[oar-1], label='N = %i \nMean = %.2f \nStd = %.2f'%(len(Ecart_vol[oar-1]), np.mean(Ecart_vol[oar-1]), np.std(Ecart_vol[oar-1])))
	plt.title(list_organs[oar-1])
	plt.xlabel('V ($cm^3$)', fontsize=8)
	if oar == 1 or oar == (int(len(list_organs)/2)+1):
		plt.ylabel('dN/dV', fontsize=10)
	plt.legend()
plt.show()
fig.savefig('Gap_Volume_oar.pdf')


# Plot histogramms for each OAR
fig=plt.figure(figsize=(20, 15))
for oar in range(1, len(list_organs)+1):
	plt.subplot(2, int(len(list_organs)/2), oar)
	plt.suptitle('Volume of Organs at risks in predictions')
	plt.hist(Vol_pred[oar-1], label='N = %i \nMean = %.2f \nStd = %.2f'%(len(Vol_pred[oar-1]), np.mean(Vol_pred[oar-1]), np.std(Vol_pred[oar-1])))
	plt.title(list_organs[oar-1])
	plt.xlabel('V ($cm^3$)', fontsize=8)
	if oar == 1 or oar == (int(len(list_organs)/2)+1):
		plt.ylabel('dN/dV', fontsize=10)
	plt.legend()
plt.show()
fig.savefig('Volume_oar_prediction.pdf')


# Plot histogramms for each OAR
fig=plt.figure(figsize=(20, 15))
for oar in range(1, len(list_organs)+1):
	plt.subplot(2, int(len(list_organs)/2), oar)
	plt.suptitle('Volume of Organs at risks in labels')
	plt.hist(Vol_label[oar-1], label='N = %i \nMean = %.2f \nStd = %.2f'%(len(Vol_label[oar-1]), np.mean(Vol_label[oar-1]), np.std(Vol_label[oar-1])))
	plt.title(list_organs[oar-1])
	plt.xlabel('V ($cm^3$)', fontsize=8)
	if oar == 1 or oar == (int(len(list_organs)/2)+1):
		plt.ylabel('dN/dV', fontsize=10)
	plt.legend()
plt.show()
fig.savefig('Volume_oar_labels.pdf')


duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
