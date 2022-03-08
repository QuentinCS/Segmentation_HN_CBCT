# Script for resampling one image with gatetools and compress to .nii.gz 

import gatetools as gt 
import sys
import itk
import gzip

print(sys.argv[1])
image = itk.imread(sys.argv[1]) 
newspacing = itk.Vector[itk.D, 3]()
newspacing.Fill(4.0)
image_newspacing = gt.applyTransformation(input=image, newspacing=newspacing, force_resample=True, adaptive=True)
itk.imwrite(image_newspacing, 'image_resampled.nii')

with open('image_resampled.nii', 'rb') as src, gzip.open('image_resampled.nii.gz', 'wb') as dst:
    dst.writelines(src)


