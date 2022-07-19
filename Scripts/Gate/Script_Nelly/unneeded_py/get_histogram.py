#!/usr/bin/env python
import itk
import os
import numpy as np
from matplotlib import pyplot as plt
import pathlib
import gatetools as gt
import math

def plot_all_hist(realcbct_path, withscatter_path, withoutscatter_path, mask_path):
    # load images
    realcbct_image = itk.imread(realcbct_path)
    realcbct =itk.GetArrayFromImage(realcbct_image)
    withscatter = itk.GetArrayFromImage(itk.imread(withscatter_path))
    withoutscatter = itk.GetArrayFromImage(itk.imread(withoutscatter_path))
    mask_image = itk.imread(mask_path)
    mask = itk.GetArrayFromImage(mask_image)

    # resize mask
    #resized_mask = itk.GetArrayFromImage(gt.applyTransformation(input=mask_image, like=realcbct_image, force_resample=True))

    # create the histograms
    histogram1, bin_edges1 = np.histogram(realcbct[mask == 1], bins=1500, range=(200,1700))
    histogram2, bin_edges2 = np.histogram(withscatter[mask == 1], bins=1500, range=(200,1700))
    histogram3, bin_edges3 = np.histogram(withoutscatter[mask == 1], bins=1500, range=(200,1700))

    # configure and draw the histogram figure
    plt.figure()
    plt.title("Images Histogram")
    plt.xlabel("Pixel value")
    plt.ylabel("pixels")
    #plt.xlim([0.0, 1.0]) 

    plt.plot(bin_edges1[0:-1], histogram1, label='real cbct')  
    plt.plot(bin_edges2[0:-1], histogram2, label='with scatter')  
    plt.plot(bin_edges3[0:-1], histogram3, label='without scatter') 
    plt.legend()
    plt.savefig('histograms.png')
    plt.close()
    # plt.show()


def plot_profiles(cbct_path, withscatter_path, withoutscatter_path):
    profiles_folder = './profiles'
    if not os.path.exists(profiles_folder):
        os.makedirs(profiles_folder)
    
    # load the images and their info
    realcbct, origin_cbct, spacing_cbct, isocenter_cbct, size_cbct = get_image_info(cbct_path)
    withscatter, origin_withscatter, spacing_withscatter, isocenter_withscatter, size_withscatter = get_image_info(withscatter_path)
    withoutscatter, origin_withoutscatter, spacing_withoutscatter, isocenter_withoutscatter, size_withoutscatter = get_image_info(withoutscatter_path)

    # configure and draw the profile of each image through the isocenter in all 3 directions
    # profile along x
    plt.figure()
    plt.title("Images profiles along x")
    plt.xlabel("Distance (mm)")
    plt.ylabel("Intensity")
    #plt.xlim([0.0, 1.0]) 

    # cbct
    p1 = f'0,{isocenter_cbct[1]},{isocenter_cbct[2]}'
    p2 = f'{size_cbct[0]-1},{isocenter_cbct[1]},{isocenter_cbct[2]}'
    profile_filepath_cbct = f'{profiles_folder}/cbctprofile_x'
    profile_command= f'clitkProfileImage -i {cbct_path} -o {profile_filepath_cbct} -f {p1} -s {p2}'
    os.system(profile_command)
    cbct_pixelvalues, cbct_distances = read_profile_file(profile_filepath_cbct)
    plt.plot(cbct_distances, cbct_pixelvalues, label='real cbct')  

    # with scatter
    p1 = f'0,{isocenter_withscatter[1]},{isocenter_withscatter[2]}'
    p2 = f'{size_withscatter[0]-1},{isocenter_withscatter[1]},{isocenter_withscatter[2]}'
    profile_filepath_withscatter = f'{profiles_folder}/withscatterprofile_x'
    profile_command= f'clitkProfileImage -i {withscatter_path} -o {profile_filepath_withscatter} -f {p1} -s {p2}'
    os.system(profile_command)
    withscatter_pixelvalues, withscatter_distances = read_profile_file(profile_filepath_withscatter)
    plt.plot(withscatter_distances, withscatter_pixelvalues, label='with scatter')  

    # without scatter
    p1 = f'0,{isocenter_withoutscatter[1]},{isocenter_withoutscatter[2]}'
    p2 = f'{size_withoutscatter[0]-1},{isocenter_withoutscatter[1]},{isocenter_withoutscatter[2]}'
    profile_filepath_withoutscatter = f'{profiles_folder}/withoutscatterprofile_x'
    profile_command= f'clitkProfileImage -i {withoutscatter_path} -o {profile_filepath_withoutscatter} -f {p1} -s {p2}'
    os.system(profile_command)
    withoutscatter_pixelvalues, withoutscatter_distances = read_profile_file(profile_filepath_withoutscatter)
    plt.plot(withoutscatter_distances, withoutscatter_pixelvalues, label='without scatter')  

    plt.legend()
    plt.savefig('profiles_x.png')
    plt.close()


    # profile along y
    plt.figure()
    plt.title("Images profiles along y")
    plt.xlabel("Distance (mm)")
    plt.ylabel("Intensity")
    #plt.xlim([0.0, 1.0]) 

    # cbct
    p1 = f'{isocenter_cbct[0]},0,{isocenter_cbct[2]}'
    p2 = f'{isocenter_cbct[0]},{size_cbct[1]-1},{isocenter_cbct[2]}'
    profile_filepath_cbct = f'{profiles_folder}/cbctprofile_y'
    profile_command= f'clitkProfileImage -i {cbct_path} -o {profile_filepath_cbct} -f {p1} -s {p2}'
    os.system(profile_command)
    cbct_pixelvalues, cbct_distances = read_profile_file(profile_filepath_cbct)
    plt.plot(cbct_distances, cbct_pixelvalues, label='real cbct')  

    # with scatter
    p1 = f'{isocenter_withscatter[0]},0,{isocenter_withscatter[2]}'
    p2 = f'{isocenter_withscatter[0]},{size_withscatter[1]-1},{isocenter_withscatter[2]}'
    profile_filepath_withscatter = f'{profiles_folder}/withscatterprofile_y'
    profile_command= f'clitkProfileImage -i {withscatter_path} -o {profile_filepath_withscatter} -f {p1} -s {p2}'
    os.system(profile_command)
    withscatter_pixelvalues, withscatter_distances = read_profile_file(profile_filepath_withscatter)
    plt.plot(withscatter_distances, withscatter_pixelvalues, label='with scatter')  

    # without scatter
    p1 = f'{isocenter_withoutscatter[0]},0,{isocenter_withoutscatter[2]}'
    p2 = f'{isocenter_withoutscatter[0]},{size_withoutscatter[1]-1},{isocenter_withoutscatter[2]}'
    profile_filepath_withoutscatter = f'{profiles_folder}/withoutscatterprofile_y'
    profile_command= f'clitkProfileImage -i {withoutscatter_path} -o {profile_filepath_withoutscatter} -f {p1} -s {p2}'
    os.system(profile_command)
    withoutscatter_pixelvalues, withoutscatter_distances = read_profile_file(profile_filepath_withoutscatter)
    plt.plot(withoutscatter_distances, withoutscatter_pixelvalues, label='without scatter')  

    plt.legend()
    plt.savefig('profiles_y.png')
    plt.close()



    # profile along z
    plt.figure()
    plt.title("Images profiles along z")
    plt.xlabel("Distance (mm)")
    plt.ylabel("Intensity")
    #plt.xlim([0.0, 1.0]) 

    # cbct
    p1 = f'{isocenter_cbct[0]},{isocenter_cbct[1]},0'
    p2 = f'{isocenter_cbct[0]},{isocenter_cbct[1]},{size_cbct[2]-1}'
    profile_filepath_cbct = f'{profiles_folder}/cbctprofile_z'
    profile_command= f'clitkProfileImage -i {cbct_path} -o {profile_filepath_cbct} -f {p1} -s {p2}'
    os.system(profile_command)
    cbct_pixelvalues, cbct_distances = read_profile_file(profile_filepath_cbct)
    plt.plot(cbct_distances, cbct_pixelvalues, label='real cbct')  

    # with scatter
    p1 = f'{isocenter_withscatter[0]},{isocenter_withscatter[1]},0'
    p2 = f'{isocenter_withscatter[0]},{isocenter_withscatter[1]},{size_withscatter[2]-1}'
    profile_filepath_withscatter = f'{profiles_folder}/withscatterprofile_z'
    profile_command= f'clitkProfileImage -i {withscatter_path} -o {profile_filepath_withscatter} -f {p1} -s {p2}'
    os.system(profile_command)
    withscatter_pixelvalues, withscatter_distances = read_profile_file(profile_filepath_withscatter)
    plt.plot(withscatter_distances, withscatter_pixelvalues, label='with scatter')  

    # without scatter
    p1 = f'{isocenter_withoutscatter[0]},{isocenter_withoutscatter[1]},0'
    p2 = f'{isocenter_withoutscatter[0]},{isocenter_withoutscatter[1]},{size_withoutscatter[2]-1}'
    profile_filepath_withoutscatter = f'{profiles_folder}/withoutscatterprofile_z'
    profile_command= f'clitkProfileImage -i {withoutscatter_path} -o {profile_filepath_withoutscatter} -f {p1} -s {p2}'
    os.system(profile_command)
    withoutscatter_pixelvalues, withoutscatter_distances = read_profile_file(profile_filepath_withoutscatter)
    plt.plot(withoutscatter_distances, withoutscatter_pixelvalues, label='without scatter')  

    plt.legend()
    plt.savefig('profiles_z.png')
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
        isocenter[0] =  size[0]//2
    if isocenter[1] < 0 or isocenter[1] > size[1]:
        isocenter[1] =  size[1]//2
    if isocenter[2] < 0 or isocenter[2] > size[2]:
        isocenter[2] =  size[2]//2

    return img, origin, spacing, isocenter, size


if __name__ == "__main__":
    # image path
    realcbct_path = './data/cbct.0.nii'
    withscatter_path = './withscatter/Reconstruction/fdk_rotated.mha'
    withoutscatter_path = './withoutscatter/Reconstruction/fdk_rotated.mha'
    mask_path = './withscatter/Reconstruction/mask.mha'
    plot_all_hist(realcbct_path, withscatter_path, withoutscatter_path,mask_path)
    plot_profiles(realcbct_path, withscatter_path, withoutscatter_path)
