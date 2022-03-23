 # Script to check if the parotids glands are well labeled and not inversed in some images
import gatetools as gt
import time
import sys
import itk
import os

start_time = time.time()


i = 0
name = 'Data_set_%.3i'%(i)
while os.path.exists(name) == True:

    if i == 0:
        image_CT = itk.imread(name + '/Patient.nii')
        image_G = itk.array_view_from_image(image_CT)
        image_CT1 = itk.imread(name + '/Patient.nii')
        image_D = itk.array_view_from_image(image_CT1)
    
    if os.path.isfile(name + '/Parotide_G.nii') == True:
        image_g = itk.imread(name + '/Parotide_G.nii')
        image_rescale_g = gt.applyTransformation(input=image_g, like=image_CT, force_resample=True, interpolation_mode='NN')
        image_npg = itk.array_view_from_image(image_rescale_g)
        image_G += image_npg

    if os.path.isfile(name + '/Parotide_D.nii') == True:
        image_d = itk.imread(name + '/Parotide_D.nii')
        image_rescale_d = gt.applyTransformation(input=image_d, like=image_CT, force_resample=True, interpolation_mode='NN')
        image_npd = itk.array_view_from_image(image_rescale_d)
        image_D += image_npd

    i += 1
    name = 'Data_set_%.3i'%(i)

print("Number of images :", i)

save_g = itk.image_from_array(image_G)
save_g.CopyInformation(image_CT) # Important to save the image with correct spacing, size!!
itk.imwrite(save_g, 'Parotid_left_sum.nii')

save_d = itk.image_from_array(image_D)
save_d.CopyInformation(image_CT) # Important to save the image with correct spacing, size!!
itk.imwrite(save_d, 'Parotid_right_sum.nii')

duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)

