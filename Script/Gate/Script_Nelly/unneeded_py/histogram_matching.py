#!/usr/bin/env python
import itk
import os
import numpy as np
from matplotlib import pyplot as plt
import pathlib
import gatetools as gt
import math
import glob


def plot_all_hist(realcbct_path, withscatter_path, withoutscatter_path, FOV_mask_path,patient_mask_path):
    # load images and mask and resize
    realcbct_image = itk.imread(realcbct_path)
    realcbct_origin = realcbct_image.GetOrigin()
    realcbct =itk.GetArrayFromImage(realcbct_image)
    #realcbct = realcbct

    withscatter_image = itk.imread(withscatter_path)
    # resize if different from the real cbct
    if itk.size(withscatter_image) == itk.size(realcbct_image):
        withscatter = itk.GetArrayFromImage(withscatter_image)
    else:
        withscatter = itk.GetArrayFromImage(gt.applyTransformation(input=withscatter_image, like=realcbct_image, force_resample=True))
    # rescale value
    withscatter = withscatter * 65536


    withoutscatter_image = itk.imread(withoutscatter_path)
    #withoutscatter_origin = withoutscatter_image.GetOrigin()
    # resize if different from the real cbct
    if itk.size(withoutscatter_image) == itk.size(realcbct_image):
        withoutscatter = itk.GetArrayFromImage(withoutscatter_image)
    else:
        withoutscatter = itk.GetArrayFromImage(gt.applyTransformation(input=withoutscatter_image, like=realcbct_image, force_resample=True))
    withoutscatter = withoutscatter * 65536

    FOV_mask_image = itk.imread(FOV_mask_path)
    if itk.size(FOV_mask_image) == itk.size(realcbct_image):
        FOV_mask = itk.GetArrayFromImage(FOV_mask_image)
    else:
        FOV_mask = itk.GetArrayFromImage(gt.applyTransformation(input=FOV_mask_image, like=realcbct_image, force_resample=True))

    patient_mask_image = itk.imread(patient_mask_path)
    if itk.size(patient_mask_image) == itk.size(realcbct_image):
        patient_mask = itk.GetArrayFromImage(patient_mask_image)
    else:
        patient_mask = itk.GetArrayFromImage(gt.applyTransformation(input=patient_mask_image, like=realcbct_image, force_resample=True))


    # ignore where values > 2000 or < -500 
    valuesmask =np.ma.greater_equal(realcbct,-500) & np.ma.less_equal(realcbct,2000) & np.ma.greater_equal(withscatter,-500) & np.ma.less_equal(withscatter,2000) & np.ma.greater_equal(withoutscatter,-500)  & np.ma.less_equal(withoutscatter,2000)

    # apply the masks, setting values outside the patient to 0
    mask_intersection = (FOV_mask == 1) & (patient_mask == 1) & valuesmask

    realcbct_masked = apply_mask(realcbct, mask_intersection, realcbct_origin, 'realcbct_masked.mha')
    withscatter_masked = apply_mask(withscatter, mask_intersection, realcbct_origin, 'withscatter_masked.mha')
    withoutscatter_masked = apply_mask(withoutscatter, mask_intersection, realcbct_origin, 'withoutscatter_masked.mha')

    # ignore values behind the mask, and where values of the real cbct > 1000
    #newmask =np.ma.greater_equal(realcbct_masked,2000) | np.ma.less_equal(realcbct_masked,-500) | np.ma.greater_equal(withscatter_masked,2000) | np.ma.less_equal(withscatter_masked,-500) | np.ma.greater_equal(withoutscatter_masked,2000)  | np.ma.less_equal(withoutscatter_masked,-500)
    #newmask =np.ma.greater_equal(realcbct,2000) | np.ma.less_equal(realcbct,-500)

    #print(withscatter)
    #realcbct_masked = np.around(np.ma.masked_array(realcbct_masked,newmask) )
    #withscatter_masked = np.around(np.ma.masked_array(withscatter_masked,newmask) )
    #withoutscatter_masked = np.around(np.ma.masked_array(withoutscatter_masked, newmask) )
    realcbct_masked = np.around(realcbct_masked)
    withscatter_masked = np.around(withscatter_masked)
    withoutscatter_masked = np.around(withoutscatter_masked)

    plot_histogram(realcbct_masked,withscatter_masked,withoutscatter_masked, 'histogram_beforematching.png')
    plot_profiles('realcbct_masked.mha', 'withscatter_masked.mha', 'withoutscatter_masked.mha', 'beforematching')

    # print the mean and std dev
    #print(withscatter)
    ratio_withscatter = np.mean(realcbct_masked) /(np.mean(withscatter_masked))
    #print(f'ratio = {ratio_withscatter}')
    realcbct_mean = np.mean(realcbct_masked)
    realcbct_std = np.std(realcbct_masked)
    withscatter_mean = np.mean(withscatter_masked)
    withscatter_std = np.std(withscatter_masked)
    #withscatter_matched = (((withscatter - withscatter_mean)/withscatter_std) * realcbct_std)+realcbct_mean
    withscatter_matched = withscatter* ratio_withscatter
    # shift the values to the negative range: -1024 0
    withscatter_matched_shifted = withscatter_matched -1024
    print(f'mean real cbct = {np.mean(realcbct)}')
    print(f'std real cbct = {np.std(realcbct)}')
    print(f'mean withscatter = {np.mean(withscatter_matched)}')
    print(f'std withscatter = {np.std(withscatter_matched)}')
    
    outputimage = itk.GetImageFromArray(withscatter_matched_shifted)
    outputimage.SetOrigin(realcbct_origin)
    itk.imwrite(outputimage, 'withscatter_matched.mha')

    withoutscatter_mean = np.mean(withoutscatter_masked)
    withoutscatter_std = np.std(withoutscatter_masked)
    #withoutscatter_matched = (((withoutscatter - withoutscatter_mean)/withoutscatter_std) * realcbct_std)+realcbct_mean
    ratio_withoutscatter = np.mean(realcbct_masked) /(np.mean(withoutscatter_masked))
    withoutscatter_matched = withoutscatter * ratio_withoutscatter
    # shift the values to the negative range: -1024 0
    withoutscatter_matched_shifted = withoutscatter_matched -1024

    outputimage = itk.GetImageFromArray(withoutscatter_matched_shifted)
    outputimage.SetOrigin(realcbct_origin)
    itk.imwrite(outputimage, 'withoutscatter_matched.mha')

    # perform histogram matching
    #withscatter_matched = hist_match(withscatter,realcbct,mask_intersection,1500, 'withscatter_matched.mha',realcbct_origin)

    #withoutscatter_matched = hist_match(withoutscatter,realcbct,mask_intersection,1500, 'withoutscatter_matched.mha',realcbct_origin)





    # ignore where values > 2000 or < -500 
    valuesmask =np.ma.greater_equal(realcbct,-500) & np.ma.less_equal(realcbct,2000) & np.ma.greater_equal(withscatter_matched,-500) & np.ma.less_equal(withscatter_matched,2000) & np.ma.greater_equal(withoutscatter_matched,-500)  & np.ma.less_equal(withoutscatter_matched,2000)

    # apply the masks, setting values outside the patient to 0
    mask_intersection = (FOV_mask == 1) & (patient_mask == 1) & valuesmask

    realcbct_masked = apply_mask(realcbct, mask_intersection, realcbct_origin, 'realcbct_masked.mha')
    withscatter_matched_masked = apply_mask(withscatter_matched, mask_intersection, realcbct_origin, 'withscatter_matched_masked.mha')
    withoutscatter_matched_masked = apply_mask(withoutscatter_matched, mask_intersection, realcbct_origin, 'withoutscatter_matched_masked.mha')

    realcbct_masked = np.around(realcbct_masked)
    withscatter_matched_masked = np.around(withscatter_matched_masked)
    withoutscatter_matched_masked = np.around(withoutscatter_matched_masked)

    # plot the histograms after matching
    plot_histogram(realcbct_masked,withscatter_matched_masked,withoutscatter_matched_masked, 'histogram_aftermatching.png')
    plot_profiles( 'realcbct_masked.mha', 'withscatter_matched_masked.mha', 'withoutscatter_matched_masked.mha', 'aftermatching')


def apply_mask(img, mask, origin, maskedimage_name):

    img =np.where(mask, img,0)
    masked_img = itk.GetImageFromArray(img)
    masked_img.SetOrigin(origin)

    # save the image
    itk.imwrite(masked_img, maskedimage_name)

    # ignore values behind the mask,
    masked_img = np.ma.masked_array(masked_img,~mask)
    return masked_img

def plot_histogram(realcbct,withscatter,withoutscatter, histogram_name):
    # create the histograms
    #histogram1, bin_edges1 = np.histogram(realcbct[mask_intersection], bins=1500)
    #histogram2, bin_edges2 = np.histogram(withscatter[mask_intersection], bins=1500)
    #histogram3, bin_edges3 = np.histogram(withoutscatter[mask_intersection], bins=1500)
    realcbct = np.ma.compressed(realcbct)
    withscatter = np.ma.compressed(withscatter)
    withoutscatter = np.ma.compressed(withoutscatter)
    bin_edges1, histogram1 = np.unique(realcbct, return_counts=True)
    bin_edges2, histogram2 = np.unique(withscatter, return_counts=True)
    bin_edges3, histogram3 = np.unique(withoutscatter, return_counts=True)

    # configure and draw the histogram figure
    plt.figure()
    plt.title("Images Histogram")
    plt.xlabel("Pixel value")
    plt.ylabel("pixels")
    #plt.xlim([0.0, 1.0]) 

    #plt.plot(bin_edges1[0:-1], histogram1, label='real cbct')  
    #plt.plot(bin_edges2[0:-1], histogram2, label='with scatter')  
    #plt.plot(bin_edges3[0:-1], histogram3, label='without scatter') 
    plt.plot(bin_edges1, histogram1, label='real cbct')  
    plt.plot(bin_edges2, histogram2, label='with scatter')  
    plt.plot(bin_edges3, histogram3, label='without scatter') 
    plt.legend()
    plt.savefig(histogram_name)
    plt.close()
    # plt.show()

    # plot the ratio of the histograms
    plt.figure()
    plt.title("Ratio Histogram")
    plt.xlabel("Pixels")
    plt.ylabel("Ratio")
    #plt.xlim([0.0, 1.0]) 

    histogram1, bin_edges1 = np.histogram(realcbct, bins=1500, range=(-500,2000))
    histogram2, bin_edges2 = np.histogram(withscatter, bins=1500, range=(-500,2000))
    ratio = np.zeros_like(histogram1)
    ratio_withscatter = np.divide(histogram1, histogram2, out=ratio, where=histogram2!=0, casting='unsafe')

    #plt.plot(bin_edges1[0:-1], histogram1, label='real cbct')  
    #plt.plot(bin_edges2[0:-1], histogram2, label='with scatter')  
    #plt.plot(bin_edges3[0:-1], histogram3, label='without scatter') 
    plt.plot(bin_edges1[0:-1], ratio_withscatter, label='Ratio')  
    plt.legend()
    plt.savefig(f'ratio_{histogram_name}')
    plt.close()

def find_nearest_above(my_array, target):
    diff = my_array - target
    #return np.abs(diff).argmin()
    mask = np.ma.less_equal(diff, -1)
    # We need to mask the negative differences
    # since we are looking for values above
    if np.all(mask): 
        c = np.abs(diff).argmin()
        return c # returns min index of the nearest if target is greater than any value
    masked_diff = np.ma.masked_array(diff, mask)
    return masked_diff.argmin()

def hist_match(original, specified, mask ,bins, matchedimage_name, origin):

    oldshape = original.shape
    #oldshape = specified.shape
    #newmask = np.ma.greater_equal(original, 1000)
    original = np.ma.masked_array(original, ~mask)
    specified = np.ma.masked_array(specified, ~mask)
    #original = np.ma.masked_array(original, newmask)
    #specified = np.ma.masked_array(specified, newmask)
    #print((original.shape))
    #print((np.ma.compressed(original)).shape)
    original = original.ravel() 
    specified = specified.ravel()
    #mask = mask.ravel()
    #print(specified)
    #specified = specified.ravel()
    # get only the values where mask = true 

    #s_counts = np.zeros([2001]) # count values up to 2000
    #t_counts = np.zeros([2001]) # count values up to 2000
    # loop through the pixels of the original
    #original_comp = np.ma.compressed(original)
    #specified_comp = np.ma.compressed(specified)
    #for idx, pix in enumerate(original_comp):
    #    s_counts[pix.astype(int)] += 1
    #    t_counts[specified_comp[idx].astype(int)] += 1
    #print(s_counts)
    #print(t_counts)

    # get the set of unique pixel values and their corresponding indices and counts
    s_values, bin_idx, s_counts = np.unique(original, return_inverse=True,return_counts=True)
    t_values, t_counts = np.unique(specified, return_counts=True)
    #print(s_counts2)
    #print(t_counts2)
    # Calculate s_k for original image
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_quantiles /= s_quantiles[-1]
    
    # Calculate s_k for specified image
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_quantiles /= t_quantiles[-1]

    # Round the values
    sour = np.around(s_quantiles*65536)
    temp = np.around(t_quantiles*65536)

    # Map the rounded values
    b=[]
    for data in sour[:]:
        b.append(find_nearest_above(temp,data))
    #print(b)
    b= np.array(b,dtype='uint16')
    #print(b)


    #interp_t_values = np.interp(b, temp, t_values)
    interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

    #b= np.array(b,dtype='uint16')
    output = interp_t_values[bin_idx].reshape(oldshape)
    #output = b[bin_idx].reshape(oldshape)

    # set values outside the mask to 0
    output= np.where(mask,output,0)

    # save the output image
    outputimage = itk.GetImageFromArray(output)
    outputimage.SetOrigin(origin)
    itk.imwrite(outputimage, matchedimage_name)

    # ignore values outside the mask
    output = np.ma.masked_array(output, ~mask)
    return output


def plot_profiles(cbct_path, withscatter_path, withoutscatter_path, nameext):
    profiles_folder = f'./profiles_{nameext}'
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
    #print(profile_command)
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
    plt.savefig(f'profiles_x_{nameext}.png')
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
    plt.savefig(f'profiles_y_{nameext}.png')
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
    plt.savefig(f'profiles_z_{nameext}.png')
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
    for patient_folders in glob.glob('./cbct_images/*'):
        # go to patient folder and get histogram
        main_path=os.getcwd()
        os.chdir(patient_folders)
        print(patient_folders)
        # images name
        realcbct_path = 'cbct.0.nii'#
        withscatter_path = 'fdk_rotated_withscatter.mha'
        withoutscatter_path = 'fdk_rotated_withoutscatter.mha'
        FOV_mask_path = 'mask_withscatter.mha'
        patient_mask_path = 'patient_mask.mha'

        if os.path.exists(withscatter_path):
            plot_all_hist(realcbct_path, withscatter_path, withoutscatter_path,FOV_mask_path,patient_mask_path)

        os.chdir(main_path)


