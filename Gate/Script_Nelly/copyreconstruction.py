
#!/usr/bin/env python
import shutil
import sys
import glob
import os

def copy_cbct():
    images_folder = 'cbct_images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    for patients in glob.glob('./Simulations/*'):
        copy_directory = f'{images_folder}/{os.path.basename(patients)}'
        if not os.path.exists(copy_directory):
            os.makedirs(copy_directory)

        # copy real cbct, and reconstructed with and without scatter, and mask
        filename = f'{patients}/withscatter/Reconstruction/fdk_rotated.mha'
        if os.path.exists(filename):
            shutil.copy(filename,f'{copy_directory}/fdk_rotated_withscatter.mha')

        filename = f'{patients}/withoutscatter/Reconstruction/fdk_rotated.mha'
        if os.path.exists(filename):
            shutil.copy(filename,f'{copy_directory}/fdk_rotated_withoutscatter.mha')

        filename = f'{patients}/withscatter/Reconstruction/mask.mha'
        if os.path.exists(filename):
            shutil.copy(filename,f'{copy_directory}/mask_withscatter.mha')

        filename = f'{patients}/data/cbct.0.nii'
        if os.path.exists(filename):
            shutil.copy(filename,copy_directory)

        # get patient mask
        extractpatient_command = f'clitkExtractPatient -i {patients}/data/CT.nii -o {copy_directory}/patient_mask.mha'
        os.system(extractpatient_command)
      

if __name__ == "__main__":
    copy_cbct()

