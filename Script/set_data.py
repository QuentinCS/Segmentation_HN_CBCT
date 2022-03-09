# Script for resampling, naming images and set label file with gatetools and compress to .nii.gz,
# Apply on folder Data_set_XXX with CT file and OARs files (Patient, Parotide R, Parotide L, Larynx, Tronc cerebral)
# Labels will have the same size, spacing as the CT scan used as ref

import gatetools as gt 
import time
import sys
import itk
import gzip
import os

start_time = time.time()

# Spacing for resampling
spacing = 8.0
newspacing = itk.Vector[itk.D, 3]()
newspacing.Fill(spacing)

Folder = []
with open("list", "r") as file1:
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
    #image_resize = gt.applyTransformation(input=image_itk, like=image_ref , force_resample=True, adaptive=True)
    #image_ref = gt.applyTransformation(input=image_itk, newspacing=newspacing, force_resample=True, adaptive=True, interpolation_mode='linear')
    image_ref = gt.applyTransformation(input=image_itk, newspacing=newspacing, force_resample=True, adaptive=True, interpolation_mode='linear', pad=-1024.0)
    itk.imwrite(image_ref, "../imagesTr/" + new_name)

    # gzip image if begin image is not .gz
    with open("../imagesTr/" + new_name, 'rb') as src, gzip.open("../imagesTr/" + new_name + '.gz', 'wb') as dst:
        dst.writelines(src)
    os.remove("../imagesTr/" + new_name)


    # Get background to sum
    imageBck = itk.imread(folder[i]+"/0_Patient")
    imageBck_np = gt.applyTransformation(input=imageBck, like=image_ref, force_resample=True, interpolation_mode='NN')
    #imageBck_np = gt.applyTransformation(input=imageBck, like=image_ref, force_resample=True, interpolation_mode='NN', pad=1.0)
    mask_oar = itk.array_view_from_image(imageBck_np)

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
    #image_1S = gt.applyTransformation(input=image1, like=image_ref, force_resample=True, interpolation_mode='NN', pad=1.0)
    #image_2S = gt.applyTransformation(input=image2, like=image_ref, force_resample=True, interpolation_mode='NN', pad=1.0)
    #image_3S = gt.applyTransformation(input=image3, like=image_ref, force_resample=True, interpolation_mode='NN', pad=1.0)
    #image_4S = gt.applyTransformation(input=image4, like=image_ref, force_resample=True, interpolation_mode='NN', pad=1.0)
    
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
    itk.imwrite(save, "../labelsTr/" + oar_name)

    # gzip image if begin image is not .gz
    with open("../labelsTr/" + oar_name, 'rb') as src, gzip.open("../labelsTr/" + oar_name + '.gz', 'wb') as dst:
            dst.writelines(src)
    os.remove("../labelsTr/" + oar_name)

duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)
