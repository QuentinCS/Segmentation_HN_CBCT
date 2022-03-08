# Script for adding labbel's masks and return label file .nii.gz  
# Call first the CT scan, the background, and then the OARs

import gatetools as gt
import numpy as np
import sys 
import itk
import gzip

# Get CT scan for the size 
image1 = itk.imread(sys.argv[1])

# Get background to sum
imageBck = itk.imread(sys.argv[2])
imageBck_np = gt.applyTransformation(input=imageBck, like=image1 , force_resample=True)#, adaptive=True)
mask_oar = itk.array_view_from_image(imageBck_np)

#Get the OARs, scale up, resize and sum
for i in range (3, len(sys.argv)):
    image = itk.imread(sys.argv[i])
    image_np = itk.array_view_from_image(image)

    # Resize to CT size
    image_new = gt.applyTransformation(input=image, like=image1, force_resample=True)#, adaptive=True)
    img_resized = itk.array_view_from_image(image_new)

    # Scale up to label
    label = int(sys.argv[i][0])
    img_resized *= label

    # Adding labels  
    mask_oar += img_resized

# Save file with correct name and extension
file1 = open("name")
name = str(file1.read())
name = name.replace("\n","")

save = itk.image_from_array(mask_oar)
itk.imwrite(save, name + ".nii")

# gzip to .nii.gz
with open(name + ".nii", 'rb') as src, gzip.open(name + '.nii.gz', 'wb') as dst:
    dst.writelines(src)


