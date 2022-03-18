# Script to set the database in the format required by nnUNet: https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_conversion.md
# Need one argument : the Task name, a second argument (no matter what) will draw the oar frequency 
# Run in folder with the patient folders and create a folder with argv[1] name (the task name) for save images and labels 
# Functionnal

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
import create_json

start_time = time.time()

if len(sys.argv) <= 1:
    print("Error: Argument missing. Need one argument to name task \n")
    exit()

# Variables
directory = 0
list1 =[]
list_name =[]
directory_name = []
nb_image = 0
n_missing = 0
nb_oar = np.zeros(len(dt.Label)-1)

# By default don't print oar frequency 
plot_oar = False
if len(sys.argv) > 2:
    plot_oar = True

# Spacing for resampling
spacing = 4.0
newspacing = itk.Vector[itk.D, 3]()
newspacing.Fill(spacing)

# Name task and create the differents folders needed vy nnUNet 
Task_name = sys.argv[1]
image_train_dir = Task_name + "/imagesTr/"
label_train_dir = Task_name + "/labelsTr/"

if os.path.exists(Task_name):
    sh.rmtree(Task_name)
os.makedirs(Task_name)
os.makedirs(image_train_dir)
os.makedirs(label_train_dir)

# Travel through directory to get file list 
rootDir = '.'
for dirName, subdirList, fileList in os.walk(rootDir):
    directory += 1
    if len(fileList) > 6:
        list1.append(fileList)
        directory_name.append(dirName)

# The only solution that I found for separate the two lists ...
# There is certainly a better way to do it 
for dirName, subdirList, fileList in os.walk(rootDir):
    directory += 1
    if len(fileList) > 6:
        list_name.append(fileList)

# Remove the number character to identify the OAR from dictionary 
for i in range(len(list_name)):
    for j in range(len(list_name[i])):
        for a in range(len(dt.list_remove)):
            list_name[i][j] = list_name[i][j].replace(dt.list_remove[a], '')

# Loop to looking on the different files (CT.nii, OARs, ...) and save it in a new folder  
print("Number of images : ", len(list1), "\n")
for i in range(len(list1)):

    # Get CT file and save it in the folder imagesTr/
    if os.path.isfile(directory_name[i] + '/CT.nii') == True:
        # Resampling of image 
        image_itk = itk.imread(directory_name[i]+"/CT.nii")
        image_ref = gt.applyTransformation(input=image_itk, newspacing=newspacing, force_resample=True, adaptive=True, interpolation_mode='linear', pad=-1024.0)
    else:
        print("Error: missing CT.nii file")
        break

    # Get patient file, necessary for the following 
    patient = False
    for j in range(0, len(list1[i])):
        # Get background to sum
        file_name = directory_name[i] + "/" + list1[i][j]
        if list_name[i][j] in dt.OAR['Patient']:    
            imageBck = itk.imread(file_name)
            imageBck_np = gt.applyTransformation(input=imageBck, like=image_ref, force_resample=True, interpolation_mode='NN')
            mask_oar = itk.array_view_from_image(imageBck_np)
            patient = True
            nb_oar[0] += 1
            #print("patient")
    
    # If no patient label doesn't add image 
    if patient == False:
        #print("Missing file Patient.nii.")
        n_missing += 1
        continue

    OAR = []
    # Loop for getting the OARs and sum them over the patient 
    for j in range(0, len(list1[i])):
        for key, value in dt.OAR.items():
            file_name = directory_name[i] + "/" + list1[i][j]
            if list_name[i][j] in (value) and list_name[i][j] not in dt.OAR['Patient'] and key not in OAR:
                image = itk.imread(file_name)
                image_rescale = gt.applyTransformation(input=image, like=image_ref, force_resample=True, interpolation_mode='NN')
                image_np = itk.array_view_from_image(image_rescale)
                image_np *= dt.Label[key]
                mask_oar += image_np
                OAR.append(key) # To avoid multi label for same OAR
                nb_oar[dt.Label[key]-1] += 1 

    # Save CT file 
    itk.imwrite(image_ref, image_train_dir + "CTHN_%.3i_0000.nii"%(i))
    # gzip image if begin image is not .gz
    with open(image_train_dir + "CTHN_%.3i_0000.nii"%(i), 'rb') as src, gzip.open(image_train_dir + "CTHN_%.3i_0000.nii.gz"%(i), 'wb') as dst:
        dst.writelines(src)
    os.remove(image_train_dir + "CTHN_%.3i_0000.nii"%(i))


    # Save the OARs summed in folder labelTr/ 
    oar_name = "CTHN_%.3i"%(i) + ".nii"
    save = itk.image_from_array(mask_oar)
    save.CopyInformation(image_ref) # Important to save the image with correct spacing, size!!
    itk.imwrite(save, label_train_dir + "/" + oar_name)

    # gzip image if begin image is not .gz
    with open(label_train_dir + "/" + oar_name, 'rb') as src, gzip.open(label_train_dir + "/" + oar_name + '.gz', 'wb') as dst:
        dst.writelines(src)
    os.remove(label_train_dir + "/" + oar_name)

    if i%5 == False:
            print(i)


print("\nPatient label missing: %i, images removed"%(n_missing))

# Create json file
create_json.generate_dataset_json(output_file=Task_name + '/dataset.json', imagesTr_dir=image_train_dir, imagesTs_dir=None, modalities=create_json.modalities,
                          labels=create_json.dict_oar, dataset_name=Task_name, license="hands off!", dataset_description="Head and neck CT",
                          dataset_reference="", dataset_release='0.0')


# Draw bar plot of OAR frequency 
fig = plt.figure(figsize=(20,10))
plt.bar(dt.OAR.keys(), nb_oar)
plt.title("Organs-at-risks label frequency in images")
plt.ylabel("Nb of labels (-)")
fig.savefig("oar_frequency.pdf")

if plot_oar == True:
    plt.show()

duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
