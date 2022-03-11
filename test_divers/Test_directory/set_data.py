# Script for resampling, naming images and set label file with gatetools and compress to .nii.gz,
# Apply on folder Data_set_XXX with CT file and OARs files (Patient, Parotide R, Parotide L, Larynx, Tronc cerebral)
# Labels will have the same size, spacing as the CT scan used as ref

import gatetools as gt 
import time
import sys
import itk
import gzip
import os
import shutil as sh
import dict_oar as dt

# Function to get the key in the dictionnary using the value
def get_OAR(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None

start_time = time.time()

# Spacing for resampling
spacing = 8.0
newspacing = itk.Vector[itk.D, 3]()
newspacing.Fill(spacing)

if len(sys.argv) <= 1:
    print("Error: Argument missing. Need one argument to name task \n")
    exit()

# Name task and create the differents folders 
Task_name = sys.argv[1]
image_test_dir = Task_name + "/imagesTr"
label_test_dir = Task_name + "/labelsTr"

if os.path.exists(Task_name):
    sh.rmtree(Task_name)
os.makedirs(Task_name)
os.makedirs(image_test_dir)
os.makedirs(label_test_dir)

Folder = []
with open("Data_set_file", "r") as file1:
    ligne = file1.readline()
    while ligne != "":
        Folder.append(ligne)
        ligne = file1.readline()

folder = []
for i in Folder:
    folder.append(i.strip())

print("Number of files : ", len(folder)) 
for i in range(0, len(folder)):
    print(i)
    new_name = "CTHN_" + folder[i][9] + folder[i][10] + folder[i][11] + "_0000.nii" 
    
    # Resampling of image 
    image_itk = itk.imread(folder[i]+"/CT.nii") 
    image_ref = gt.applyTransformation(input=image_itk, newspacing=newspacing, force_resample=True, adaptive=True, interpolation_mode='linear', pad=-1024.0)
    itk.imwrite(image_ref, image_test_dir + "/" + new_name)

    # gzip image if begin image is not .gz
    with open( image_test_dir + "/" + new_name, 'rb') as src, gzip.open(image_test_dir + "/" + new_name + '.gz', 'wb') as dst:
        dst.writelines(src)
    os.remove(image_test_dir + "/" + new_name)

    # Get background to sum
    imageBck = itk.imread(folder[i]+"/0_Patient")
    imageBck_np = gt.applyTransformation(input=imageBck, like=image_ref, force_resample=True, interpolation_mode='NN')
    mask_oar = itk.array_view_from_image(imageBck_np)
   
    file_list = []
    # Travel through directory to get file list 
    for dirName, subdirList, fileList in os.walk(folder[i]):
        print(fileList)
        #file_list.append(fileList)
        #list_name.append(fileList)
    
    for j in range(0, len(fileList)):
        for value in dt.Name.values():
            if fileList[j] in value:
                image = itk.imread(folder[i] + "/" + str(fileList[j]))
                image_rescale = gt.applyTransformation(input=image, like=image_ref, force_resample=True, interpolation_mode='NN')
                image_np = itk.array_view_from_image(image_rescale)
                organ = value
                print(organ)
    image_np *= get_OAR(dt.Label[organ]) 
    #mask_oar += get_OAR(dt.Label[organ])*image_np
    # A corriger ici un truc bizzare ...

    """

    #Get the OARs, scale up, resize and sum
    image1 = itk.imread(folder[i]+"/1_Parotide_D")
    image2 = itk.imread(folder[i]+"/2_Parotide_G")
    image3 = itk.imread(folder[i]+"/3_Larynx")
    image4 = itk.imread(folder[i]+"/4_Tronc_Cerebral")

    # Resize to CT size and newspacing
    image_1S = gt.applyTransformation(input=image1, like=image_ref, force_resample=True, interpolation_mode='NN')
    image_2S = gt.applyTransformation(input=image2, like=image_ref, force_resample=True, interpolation_mode='NN')
    image_3S = gt.applyTransformation(input=image3, like=image_ref, force_resample=True, interpolation_mode='NN')
    image_4S = gt.applyTransformation(input=image4, like=image_ref, force_resample=True, interpolation_mode='NN')
    
    image1_np = itk.array_view_from_image(image_1S)
    image2_np = itk.array_view_from_image(image_2S)
    image3_np = itk.array_view_from_image(image_3S)
    image4_np = itk.array_view_from_image(image_4S)

    # Scale up to label
    image1_np *= 1
    image2_np *= 2
    image3_np *= 3
    image4_np *= 4

    # Adding labels  
    Mask_oar = mask_oar + image1_np  + image2_np  + image3_np + image4_np

    # Save result
    oar_name = "CTHN_" + folder[i][9] + folder[i][10] + folder[i][11] + ".nii" 
    save = itk.image_from_array(Mask_oar)
    save.CopyInformation(image_ref) # Important to save the image with correct spacing, size!!
    itk.imwrite(save, label_test_dir + "/" + oar_name)

    # gzip image if begin image is not .gz
    with open(label_test_dir + "/" + oar_name, 'rb') as src, gzip.open(label_test_dir + "/" + oar_name + '.gz', 'wb') as dst:
            dst.writelines(src)
    os.remove(label_test_dir + "/" + oar_name)
    """
duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
