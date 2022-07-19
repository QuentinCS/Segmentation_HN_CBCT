
#!/usr/bin/env python
import shutil
import sys
import glob
import os

def copy_matchedimages():
    images_folder = 'matched_images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    for patients in glob.glob('./cbct_images/*'):
        copy_directory = f'{images_folder}/{os.path.basename(patients)}'
        if not os.path.exists(copy_directory):
            os.makedirs(copy_directory)

        # copy simulated cbct matched with real cbct and with rennes, and CT matched with real cbct and with rennes
        filename = f'{patients}/withscatter_matchedbypatient.mha'
        if os.path.exists(filename):
            shutil.copy(filename,copy_directory)

        filename = f'{patients}/withscatter_matched_withrennes.mha'
        if os.path.exists(filename):
            shutil.copy(filename,copy_directory)

        filename = f'{patients}/realCT_matchedbypatient.mha'
        if os.path.exists(filename):
            shutil.copy(filename,copy_directory)

        filename = f'{patients}/realCT_matched_withrennes.mha'
        if os.path.exists(filename):
            shutil.copy(filename,copy_directory)
     
        # copy ROI folder
        foldername = f'{patients}/ROI'
        ROIdirName_output=f'{copy_directory}/ROI'
        if not os.path.exists(ROIdirName_output):
            os.mkdir(ROIdirName_output)
        for ROI in glob.glob(f'{foldername}/*.nii'):
            shutil.copy(ROI, ROIdirName_output)

if __name__ == "__main__":
    copy_matchedimages()

