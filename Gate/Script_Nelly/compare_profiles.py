#!/usr/bin/env python
import itk
import os
import numpy as np
from matplotlib import pyplot as plt
import pathlib
import gatetools as gt
import math
import glob


def plot_profiles(real_profile, simu_profile, direction):

    # profile along x
    plt.figure()
    plt.title(f"Images profiles along {direction}")
    plt.xlabel("Distance (mm)")
    plt.ylabel("Intensity")
    #plt.xlim([0.0, 1.0]) 

    # real
    pixelvalues1, distances1 = read_profile_file(real_profile)
    plt.plot(distances1, pixelvalues1, label='real')  

    # real
    pixelvalues2, distances2 = read_profile_file(simu_profile)
    plt.plot(distances2, pixelvalues2, label='simu')  

    plt.legend()
    plt.savefig(f'profiles_{direction}.png')
    plt.close()


def read_profile_file(file_path):
    file1 = open(file_path, 'r') 
    Lines = file1.readlines() 
    column_values = 1
    column_xcoord_mm = 5
    pixel_values = []
    distances = []
    headerfound = False
    valuefound = False
    for line in Lines: 
        # find line containing the table headers
        if 'Id' in line:
            headerfound = True
        elif headerfound == True:
            if valuefound == False:
                value = float(line.split()[column_values])
                x1 = float(line.split()[column_xcoord_mm])
                y1 = float(line.split()[column_xcoord_mm + 1])
                z1 = float(line.split()[column_xcoord_mm + 2])
                distances.append(0)
                pixel_values.append(value)
                valuefound = True
            else:
            # compute distance to first point
                x2 = float(line.split()[column_xcoord_mm])
                y2 = float(line.split()[column_xcoord_mm + 1])
                z2 = float(line.split()[column_xcoord_mm + 2])
                dist =  math.sqrt( ((x1-x2)**2)+((y1-y2)**2)+((z1-z2)**2) )
                distances.append(dist)
                pixel_values.append(float(line.split()[column_values]))

    return pixel_values, distances

def get_image_info(input_image):
    # load images
    img = itk.imread(input_image)
    # get origin in mm
    origin = itk.origin(img)
    # get spacing in mm
    spacing = itk.spacing(img)
    # get isocenter (pixels) = (0-origin)/spacing
    isocenter = - np.divide(origin,spacing).astype(int)
    # get size in pixels
    size = np.divide(itk.size(img),spacing).astype(int)

    # check if isocenter pixel is within the size, if not set it as the middle point
    if isocenter[0] < 0 or isocenter[0] > size[0]:
        isocenter[0] =  (size[0]//2).astype(int)
    if isocenter[1] < 0 or isocenter[1] > size[1]:
        isocenter[1] =  (size[1]//2).astype(int)
    if isocenter[2] < 0 or isocenter[2] > size[2]:
        isocenter[2] =  (size[2]//2).astype(int)

    return img, origin, spacing, isocenter, size


if __name__ == "__main__":
    # axial
    profile_real_axial = 'real_axial'
    profile_simu_axial = 'simu_axial'
    plot_profiles(profile_real_axial,profile_simu_axial,'x')

    profile_real_sagital = 'real_sagital'
    profile_simu_sagital = 'simu_sagital'
    plot_profiles(profile_real_sagital,profile_simu_sagital,'y')

    profile_real_coronal = 'real_coronal'
    profile_simu_coronal = 'simu_coronal'
    plot_profiles(profile_real_coronal,profile_simu_coronal,'z')



