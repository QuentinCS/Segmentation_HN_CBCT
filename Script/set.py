# Script to put the database in the right format and select OAR and save CT and organs images in a folder Data_setXXX
# Save in file Data_set_file the folder with images for patient
# Need dictionnary file dict_oar.py
# Warning : Delete all previous file (Data_set_file) and folders (Data_set_XXX) !!!!

import gatetools as gt
import numpy as np 
import difflib as di
from os import listdir
from os.path import isfile, join
import os
import shutil as sh
import dict_oar as dt 
import re
import time

# Function to get the key in the dictionnary using the value
def get_key(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None

start_time = time.time()

directory = 0
list1 =[]
list_name =[]
directory_name = []

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

# Remove the number character to better identify the OAR
for i in range(len(list_name)):
    for j in range(len(list_name[i])):
        #print(list1[i][j], "\n")
        for a in range(len(dt.list_remove)):
            list_name[i][j] = list_name[i][j].replace(dt.list_remove[a], '')
            #print(list1[i][j])
        
# Data file with list of folder, supress if already exists
if os.path.exists('Data_set_file'):
    os.remove('Data_set_file')


# Loop to looking on the different files (CT.nii, OARs, ...) and save it in a new folder  
print("Number of images : ", len(list1))
nb_image = 0
for i in range(len(list1)):
    
    name = 'Data_set_%.3i'%(nb_image)
    if os.path.exists(name):
        sh.rmtree(name)
    os.makedirs(name)
    if os.path.isfile(directory_name[i] + '/CT.nii') == True:
        #print("CT.nii Found !")
        sh.copyfile(directory_name[i] + '/CT.nii', name + '/CT.nii')
        #print('Copy: ok !')
    else:
        print("Error: missing CT.nii file")
        break
    
    for j in range(len(list1[i])):
        for value in dt.OAR.values():
            if list_name[i][j] in value:
                #print(list1[i][j], " : found")
                #print("OAR :", get_OAR(dt.OAR, value))
                sh.copyfile(directory_name[i] + "/" + list1[i][j], name + "/" + get_key(dt.OAR, value) + ".nii") # Copy OAR image in the right folder with the right name 
    
    if os.path.isfile(name + '/Patient.nii') == True:
        with open('Data_set_file', 'a') as f:
            f.write(name + '\n')
        with open(name + "/dir" , 'a') as f:
            f.write(directory_name[i]  + '\n')
        nb_image += 1
    else:
        print("Missing file Patient.nii.")
        #sh.rmtree(name)

print("All files correctly copied")

duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
