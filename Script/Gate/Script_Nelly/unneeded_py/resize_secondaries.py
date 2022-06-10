#!/usr/bin/env python
import itk
import sys
import glob
import numpy as np 
import gatetools as gt
import os

def resize_all():
    # find folder containing the secondaries and the folder containing the primary images
    for results_folder in glob.glob("results.*"):
        if os.path.isfile(f'{results_folder}/primary0000.mha'):
            primary_folder = results_folder
        elif os.path.isfile(f'{results_folder}/secondary0000.mha'):
            secondary_folder = results_folder

    # get all the secondary images and save them in the same directory as the primaries
    sec_files = glob.glob(f'{secondary_folder}/secondary????.mha')
    for imagepath in sec_files:
        image = itk.imread(imagepath)
        resizedImage = gt.applyTransformation(input=image, newsize=[512,512,1], adaptive=True, force_resample=True)
        new_imagepath = imagepath.replace(secondary_folder,primary_folder)
        itk.imwrite(resizedImage,new_imagepath)

def resize_all_local():
    # get all the secondary images
    sec_files = glob.glob('./output/secondary????.mha')
    for imagepath in sec_files:
        image = itk.imread(imagepath)
        resizedImage = gt.applyTransformation(input=image, newsize=[512,512,1], adaptive=True, force_resample=True)
        itk.imwrite(resizedImage,imagepath)

if __name__ == "__main__":
    resize_all()

