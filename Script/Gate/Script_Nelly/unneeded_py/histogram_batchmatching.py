#!/usr/bin/env python
import itk
import os
import numpy as np
from matplotlib import pyplot as plt
import pathlib
import gatetools as gt
import math
import glob
from skimage.measure import profile_line

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
    original = np.ma.masked_array(original, ~mask)
    specified = np.ma.masked_array(specified, ~mask)
    original = original.ravel() 
    specified = specified.ravel()


    # get the set of unique pixel values and their corresponding indices and counts
    s_values, bin_idx, s_counts = np.unique(original, return_inverse=True,return_counts=True)
    t_values, t_counts = np.unique(specified, return_counts=True)

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




def match_rennesCBCT(realcbct_path, withscatter_path, FOV_mask_path,patient_mask_path):
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
    #valuesmask =np.ma.greater_equal(realcbct,-500) & np.ma.less_equal(realcbct,2000) & np.ma.greater_equal(withscatter,-500) & np.ma.less_equal(withscatter,2000)

    # apply the masks, setting values outside the patient to 0
    mask_intersection = (FOV_mask == 1) & (patient_mask == 1) #& valuesmask

    realcbct_masked = apply_mask(realcbct, mask_intersection, realcbct_origin, 'realcbct_masked.mha')
    withscatter_masked = apply_mask(withscatter, mask_intersection, realcbct_origin, 'withscatter_masked.mha')

 
    #print(withscatter)
    #realcbct_masked = np.around(np.ma.masked_array(realcbct_masked,newmask) )
    #withscatter_masked = np.around(np.ma.masked_array(withscatter_masked,newmask) )
    realcbct_masked = np.around(realcbct_masked)
    withscatter_masked = np.around(withscatter_masked)

    plot_histogram(realcbct_masked,withscatter_masked, 'histogram_beforematching.png')
    plot_profiles('realcbct_masked.mha','real cbct', 'withscatter_masked.mha','with scatter', 'beforematching')

    # calculate the mean and std of a group of images (real CBCT images from Rennes)
    #outliermask = np.ma.greater_equal(withscatter,-500) & np.ma.less_equal(withscatter,2000)
    #withscatter_masked_general = apply_mask(withscatter, mask_intersection, realcbct_origin, 'withscatter_masked_general.mha')

    PATH = '../../../Rennes_images'
    files = glob.glob(f'{PATH}/*/*.nii.gz')
    imgshape = realcbct_image.shape
    x=np.zeros((len(files),imgshape[0],imgshape[1],imgshape[2]))
    for ind, fname in enumerate(files):
        rennes_image = itk.imread(fname)
        # resize the image
        img_name = 'rennes_' + os.path.basename(fname).replace('.nii.gz','')
        resized_rennesimg = gt.applyTransformation(input=rennes_image,newsize=itk.size(realcbct_image), force_resample=True)
        rennesimg_origin = resized_rennesimg.GetOrigin()
        rennes_array = itk.GetArrayFromImage(resized_rennesimg)
        img_masked = apply_mask(rennes_array, mask_intersection, rennesimg_origin, f'{img_name}_masked.mha')
        x[ind,:,:,:]=img_masked

    #x = np.mean(x,axis=0)
    #x = np.array([np.around(itk.GetArrayFromImage(itk.imread(f'{fname}'))) for fname in files])
    print(x.shape)
    print(np.mean(x))
    print(np.std(x)) 
    withscatter_shifted = np.around(withscatter-1024)
    withscatter_masked_shifted = np.around(withscatter_masked-1024)
    print(np.mean(withscatter_masked_shifted))
    print(np.std(withscatter_masked_shifted)) 

    meandiff_withscatter = np.mean(x) - (np.mean(withscatter_masked_shifted))
    stdratio_withscatter = np.std(x) /np.std(withscatter_masked_shifted)
    withscatter_shifted_matched = np.where(mask_intersection, (withscatter_shifted + meandiff_withscatter) * stdratio_withscatter ,withscatter_shifted)
    #withscatter_shifted_matched = np.where(mask_intersection, withscatter_shifted * (np.mean(x) /np.mean(withscatter_masked_shifted)) ,withscatter_shifted)
    #withscatter_shifted_matched = (withscatter-1024) * ratio_withscatter

    withscatter_matched = withscatter_shifted_matched +1024
    print(f'mean real cbct = {np.mean(realcbct)}')
    print(f'std real cbct = {np.std(realcbct)}')
    print(f'mean withscatter = {np.mean(withscatter_matched)}')
    print(f'std withscatter = {np.std(withscatter_matched)}')

    outputimage = itk.GetImageFromArray(withscatter_shifted_matched)
    outputimage.SetOrigin(realcbct_origin)
    itk.imwrite(outputimage, 'withscatter_matched_withrennes.mha')

    # print the mean and std dev
    #print(withscatter)
    #ratio_withscatter = np.mean(realcbct_masked) /(np.mean(withscatter_masked))
    #print(f'ratio = {ratio_withscatter}')
    #realcbct_mean = np.mean(realcbct_masked)
    #realcbct_std = np.std(realcbct_masked)
    #withscatter_mean = np.mean(withscatter_masked)
    #withscatter_std = np.std(withscatter_masked)
    ##withscatter_matched = (((withscatter - withscatter_mean)/withscatter_std) * realcbct_std)+realcbct_mean
    # shift the values to the negative range: -1024 0
    #withscatter_matched_shifted = withscatter_matched -1024
    #print(f'mean real cbct = {np.mean(realcbct)}')
    #print(f'std real cbct = {np.std(realcbct)}')
    #print(f'mean withscatter = {np.mean(withscatter_matched)}')
    #print(f'std withscatter = {np.std(withscatter_matched)}')

    
    #outputimage = itk.GetImageFromArray(withscatter_matched_shifted)
    #outputimage = itk.GetImageFromArray(withscatter_matched_shifted)
    #outputimage.SetOrigin(realcbct_origin)
    #itk.imwrite(outputimage, 'withscatter_matched.mha')

   
    # ignore where values > 2000 or < -500 
    #valuesmask =np.ma.greater_equal(realcbct,-500) & np.ma.less_equal(realcbct,2000) & np.ma.greater_equal(withscatter_matched,-500) & np.ma.less_equal(withscatter_matched,2000)

    # apply the masks, setting values outside the patient to 0
    #mask_intersection = (FOV_mask == 1) & (patient_mask == 1) & valuesmask

    #realcbct_masked = apply_mask(realcbct, mask_intersection, realcbct_origin, 'realcbct_masked.mha')
    withscatter_matched_masked = np.around(apply_mask(withscatter_matched, mask_intersection, realcbct_origin, 'withscatter_matched_masked.mha'))

    #realcbct_masked = np.around(realcbct_masked)

    # plot the histograms after matching
    plot_histogram(realcbct_masked,withscatter_matched_masked, 'histogram_aftermatchingwithrennes.png')
    plot_profiles( 'realcbct_masked.mha','real cbct', 'withscatter_matched_masked.mha','with scatter', 'aftermatchingwithrennes')
    plot_profiles( 'rennes_cbct_0_0_masked.mha','real cbct', 'withscatter_matchedbypatient.mha','with scatter', 'rennes_aftermatching')


def match_realCBCT(realcbct_path, withscatter_path, FOV_mask_path,patient_mask_path):
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
    #valuesmask =np.ma.greater_equal(realcbct,-500) & np.ma.less_equal(realcbct,2000) & np.ma.greater_equal(withscatter,-500) & np.ma.less_equal(withscatter,2000)

    # apply the masks, setting values outside the patient to 0
    mask_intersection = (FOV_mask == 1) & (patient_mask == 1)

    realcbct_masked = np.around(apply_mask(realcbct, mask_intersection, realcbct_origin, 'realcbct_masked.mha'))
    withscatter_masked = np.around(apply_mask(withscatter, mask_intersection, realcbct_origin, 'withscatter_masked.mha'))


    plot_histogram(realcbct_masked,withscatter_masked, 'histogram_beforematching.png')
    plot_profiles('realcbct_masked.mha','real cbct', 'withscatter_masked.mha','with scatter', 'beforematching')


    meandiff_withscatter = np.mean(realcbct_masked) - (np.mean(withscatter_masked))
    stdratio_withscatter = np.std(realcbct_masked) /(np.std(withscatter_masked))
    #withscatter_matched = np.where(mask_intersection, withscatter * (np.mean(realcbct_masked) /np.mean(withscatter_masked)) ,withscatter)
    withscatter_matched = np.where(mask_intersection, (withscatter + meandiff_withscatter) * stdratio_withscatter ,withscatter)

   
    #withscatter_matched = (((withscatter - withscatter_mean)/withscatter_std) * realcbct_std)+realcbct_mean
    # shift the values to the negative range: -1024 0
    withscatter_shifted_matched = withscatter_matched -1024
    print(f'mean real cbct = {np.mean(realcbct)}')
    print(f'std real cbct = {np.std(realcbct)}')
    print(f'mean withscatter = {np.mean(withscatter_matched)}')
    print(f'std withscatter = {np.std(withscatter_matched)}')

    outputimage = itk.GetImageFromArray(withscatter_shifted_matched)
    outputimage.SetOrigin(realcbct_origin)
    itk.imwrite(outputimage, 'withscatter_matchedbypatient.mha')

    withscatter_matched_masked = np.around(apply_mask(withscatter_matched, mask_intersection, realcbct_origin, 'withscatter_matched_masked.mha'))

    #realcbct_masked = np.around(realcbct_masked)


    # plot the histograms after matching
    plot_histogram(realcbct_masked,withscatter_matched_masked, 'histogram_aftermatching.png')
    plot_profiles( 'realcbct_masked.mha','real cbct', 'withscatter_matched_masked.mha','with scatter', 'aftermatching')
    #plot_profiles( 'rennes_cbct_0_0_masked.mha','real cbct', 'withscatter_matched.mha','with scatter', 'rennes_aftermatching')


def match_CT(CT_path, realcbct_path, FOV_mask_path,patient_mask_path):
    # load images and mask and resize
    realcbct_image = itk.imread(realcbct_path)
    realcbct_origin = realcbct_image.GetOrigin()
    realcbct_size = itk.size(realcbct_image)
    realcbct =itk.GetArrayFromImage(realcbct_image)
    realcbct_shifted = realcbct - 1024

    CT_image = itk.imread(CT_path)
    CT_image_resized = gt.applyTransformation(input=CT_image, like=realcbct_image, force_resample=True)
    realCT_origin = CT_image_resized.GetOrigin()
    realCT = itk.GetArrayFromImage(CT_image_resized)

   
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
    #valuesmask =np.ma.greater_equal(realcbct_shifted,-2000) & np.ma.less_equal(realcbct_shifted,500) & np.ma.greater_equal(realCT,-2000) & np.ma.less_equal(realCT,500)

    # apply the masks, setting values outside the patient to 0
    mask_intersection = (FOV_mask == 1) & (patient_mask == 1) #& valuesmask

    realcbct_shifted_masked = np.around(apply_mask(realcbct_shifted, mask_intersection, realcbct_origin, 'realcbct_shifted_masked.mha'))
    realCT_masked = np.around(apply_mask(realCT, mask_intersection, realCT_origin, 'realCT_masked.mha'))


    plot_histogram_CT(realcbct_shifted_masked,realCT_masked, 'histogram_CT_beforematching.png')
    plot_profiles('realcbct_shifted_masked.mha','real CBCT', 'realCT_masked.mha','real CT', 'CT_beforematching')

    # match with real cbct
    meandiff_realcbct = np.mean(realcbct_shifted_masked) - (np.mean(realCT_masked))
    stdratio_realcbct = np.std(realcbct_shifted_masked) /(np.std(realCT_masked))
    realCT_matchedbypatient = np.where(mask_intersection, (realCT + meandiff_realcbct) * stdratio_realcbct ,realCT)
    #realCT_matchedbypatient = np.where(mask_intersection, realCT * (np.mean(realcbct_shifted_masked) /np.mean(realCT_masked)) ,realCT)
    print(f'mean real cbct = {np.mean(realcbct_shifted)}')
    print(f'std real cbct = {np.std(realcbct_shifted)}')
    print(f'mean real ct = {np.mean(realCT_matchedbypatient)}')
    print(f'std real ct = {np.std(realCT_matchedbypatient)}')

    outputimage = itk.GetImageFromArray(realCT_matchedbypatient)
    outputimage.SetOrigin(realCT_origin)
    itk.imwrite(outputimage, 'realCT_matchedbypatient.mha')

    realCT_matchedbypatient_masked = np.around(apply_mask(realCT_matchedbypatient, mask_intersection, realCT_origin, 'realCT_matchedbypatient_masked.mha'))

    # plot the histograms after matching
    plot_histogram_CT(realcbct_shifted_masked,realCT_matchedbypatient_masked, 'histogram_CT_aftermatchingbypatient.png')
    plot_profiles('realcbct_shifted_masked.mha','real CBCT', 'realCT_matchedbypatient_masked.mha','real CT', 'CT_aftermatchingbypatient')


    # match with rennes images
    PATH = '../../../Rennes_images'
    files = glob.glob(f'{PATH}/*/*.nii.gz')
    imgshape = realcbct_image.shape
    x=np.zeros((len(files),imgshape[0],imgshape[1],imgshape[2]))
    for ind, fname in enumerate(files):
        rennes_image = itk.imread(fname)
        # resize the image
        img_name = 'rennes_' + os.path.basename(fname).replace('.nii.gz','')
        resized_rennesimg = gt.applyTransformation(input=rennes_image,newsize=itk.size(realcbct_image), force_resample=True)
        rennesimg_origin = resized_rennesimg.GetOrigin()
        rennes_array = itk.GetArrayFromImage(resized_rennesimg)
        img_masked = apply_mask(rennes_array, mask_intersection, rennesimg_origin, f'{img_name}_masked.mha')
        x[ind,:,:,:]=img_masked

    #x = np.array([np.around(itk.GetArrayFromImage(itk.imread(f'{fname}'))) for fname in files])
    print(x.shape)
    print(np.mean(x))
    print(np.std(x)) 
    print(np.mean(realCT_masked))
    print(np.std(realCT_masked)) 

    #mean_ratio = np.mean(x) / np.mean(realCT_masked)
    meandiff_rennes = np.mean(x) - (np.mean(realCT_masked))
    stdratio_rennes = np.std(x) /(np.std(realCT_masked))
    realCT_matched = np.where(mask_intersection, (realCT + meandiff_rennes) * stdratio_rennes ,realCT)
    #realCT_matched = np.where(mask_intersection, realCT * (np.mean(x) /np.mean(realCT_masked)),realCT)
    print(f'mean real cbct = {np.mean(realcbct_shifted)}')
    print(f'std real cbct = {np.std(realcbct_shifted)}')
    print(f'mean real ct = {np.mean(realCT_matched)}')
    print(f'std real ct = {np.std(realCT_matched)}')

    outputimage = itk.GetImageFromArray(realCT_matched)
    outputimage.SetOrigin(realCT_origin)
    itk.imwrite(outputimage, 'realCT_matched_withrennes.mha')

    realCT_matched_masked = np.around(apply_mask(realCT_matched, mask_intersection, realCT_origin, 'realCT_matched_masked.mha'))

    # plot the histograms after matching
    plot_histogram_CT(realcbct_shifted_masked,realCT_matched_masked, 'histogram_CT_aftermatching.png')
    plot_profiles('realcbct_shifted_masked.mha','real CBCT', 'realCT_matched_masked.mha','real CT', 'CT_aftermatching')
    plot_profiles('rennes_cbct_0_0_masked.mha','real cbct', 'realCT_matched_masked.mha','real CT', 'rennes_aftermatching')



def apply_mask(img, mask, origin, maskedimage_name):

    img =np.where(mask, img,0)
    masked_img = itk.GetImageFromArray(img)
    masked_img.SetOrigin(origin)

    # save the image
    itk.imwrite(masked_img, maskedimage_name)

    # ignore values behind the mask,
    masked_img = np.ma.masked_array(masked_img,~mask)
    return masked_img

def plot_histogram(realcbct,withscatter, histogram_name):
    # create the histograms
    #histogram1, bin_edges1 = np.histogram(realcbct[mask_intersection], bins=1500)
    #histogram2, bin_edges2 = np.histogram(withscatter[mask_intersection], bins=1500)
    realcbct = np.ma.compressed(realcbct)
    withscatter = np.ma.compressed(withscatter)
    bin_edges1, histogram1 = np.unique(realcbct, return_counts=True)
    bin_edges2, histogram2 = np.unique(withscatter, return_counts=True)

    # configure and draw the histogram figure
    plt.figure()
    plt.title("Images Histogram")
    plt.xlabel("Pixel value")
    plt.ylabel("pixels")
    #plt.xlim([0.0, 1.0]) 

    #plt.plot(bin_edges1[0:-1], histogram1, label='real cbct')  
    #plt.plot(bin_edges2[0:-1], histogram2, label='with scatter')  
    plt.plot(bin_edges1, histogram1, label='real cbct')  
    plt.plot(bin_edges2, histogram2, label='with scatter')  
    plt.legend()
    plt.savefig(histogram_name)
    plt.close()
    # plt.show()

def plot_histogram_CT(realcbct,realCT, histogram_name):
    # create the histograms
    #histogram1, bin_edges1 = np.histogram(realcbct[mask_intersection], bins=1500)
    #histogram2, bin_edges2 = np.histogram(withscatter[mask_intersection], bins=1500)
    realcbct = np.ma.compressed(realcbct)
    withscatter = np.ma.compressed(realCT)
    bin_edges1, histogram1 = np.unique(realcbct, return_counts=True)
    bin_edges2, histogram2 = np.unique(withscatter, return_counts=True)

    # configure and draw the histogram figure
    plt.figure()
    plt.title("Images Histogram")
    plt.xlabel("Pixel value")
    plt.ylabel("pixels")
    #plt.xlim([0.0, 1.0]) 

    #plt.plot(bin_edges1[0:-1], histogram1, label='real cbct')  
    #plt.plot(bin_edges2[0:-1], histogram2, label='with scatter')  
    plt.plot(bin_edges1, histogram1, label='real CBCT')  
    plt.plot(bin_edges2, histogram2, label='real CT')  
    plt.legend()
    plt.savefig(histogram_name)
    plt.close()
    # plt.show()


def plot_profiles(image1_path, label1, image2_path, label2, nameext):
    #profiles_folder = f'./profiles_{nameext}'
    #if not os.path.exists(profiles_folder):
    #    os.makedirs(profiles_folder)

    # load the images and their info
    realcbct, origin_cbct, spacing_cbct, isocenter_cbct, size_cbct = get_image_info(image1_path)
    withscatter, origin_withscatter, spacing_withscatter, isocenter_withscatter, size_withscatter = get_image_info(image2_path)

    # configure and draw the profile of each image through the isocenter in all 3 directions
    # profile along x
    plt.figure()
    plt.title("Images profiles along x")
    plt.xlabel("Distance (mm)")
    plt.ylabel("Intensity")
    #plt.xlim([0.0, 1.0]) 

    # cbct
    #p1 = f'0,{isocenter_cbct[1]},{isocenter_cbct[2]}'
    #p2 = f'{size_cbct[0]-1},{isocenter_cbct[1]},{isocenter_cbct[2]}'
    #p1 = (isocenter_cbct[1],0)
    #p2 = (isocenter_cbct[1],size_cbct[2]-1)
    cbct_array = itk.GetArrayFromImage(itk.imread(image1_path))
    cbct_pixelvalues = cbct_array[isocenter_cbct[2],isocenter_cbct[1],:] #profile_line(cbct_array[isocenter_cbct[0],:,:],  p1, p2)
    x_axis = range(len(cbct_pixelvalues))
    plt.plot(x_axis, cbct_pixelvalues, label=label1)  

    # with scatter
    #p1 = f'0,{isocenter_withscatter[1]},{isocenter_withscatter[2]}'
    #p2 = f'{size_withscatter[0]-1},{isocenter_withscatter[1]},{isocenter_withscatter[2]}'
    #p1 = (isocenter_withscatter[0],isocenter_withscatter[1],0)
    #p2 = (isocenter_withscatter[0],isocenter_withscatter[1],size_withscatter[2]-1)
    withscatter_array = itk.GetArrayFromImage(itk.imread(image2_path))
    withscatter_pixelvalues = withscatter_array[isocenter_withscatter[2],isocenter_withscatter[1],:] #profile_line(withscatter_array,  p1, p2)
    x_axis = range(len(cbct_pixelvalues))
    plt.plot(x_axis, withscatter_pixelvalues, label=label2)  


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
    #p1 = f'{isocenter_cbct[0]},0,{isocenter_cbct[2]}'
    #p2 = f'{isocenter_cbct[0]},{size_cbct[1]-1},{isocenter_cbct[2]}'
    #p1 = (isocenter_cbct[0],0,isocenter_cbct[2])
    #p2 = (isocenter_cbct[0],size_cbct[1]-1,isocenter_cbct[2])
    cbct_array = itk.GetArrayFromImage(itk.imread(image1_path))
    cbct_pixelvalues = cbct_array[isocenter_cbct[2],:,isocenter_cbct[0]] #profile_line(cbct_array,  p1, p2)
    x_axis = range(len(cbct_pixelvalues))
    plt.plot(x_axis, cbct_pixelvalues, label=label1)  


    # with scatter
    #p1 = f'{isocenter_withscatter[0]},0,{isocenter_withscatter[2]}'
    #p2 = f'{isocenter_withscatter[0]},{size_withscatter[1]-1},{isocenter_withscatter[2]}'
    #p1 = (isocenter_withscatter[0],0,isocenter_withscatter[2])
    #p2 = (isocenter_withscatter[0],size_withscatter[1]-1,isocenter_withscatter[2])
    withscatter_array = itk.GetArrayFromImage(itk.imread(image2_path))
    withscatter_pixelvalues = withscatter_array[isocenter_withscatter[2],:,isocenter_withscatter[0]] #profile_line(withscatter_array,  p1, p2)
    x_axis = range(len(cbct_pixelvalues))
    plt.plot(x_axis, withscatter_pixelvalues, label=label2)  

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
    #p1 = f'{isocenter_cbct[0]},{isocenter_cbct[1]},0'
    #p2 = f'{isocenter_cbct[0]},{isocenter_cbct[1]},{size_cbct[2]-1}'
    #p1 = (0,isocenter_cbct[1],isocenter_cbct[2])
    #p2 = (size_cbct[0]-1,isocenter_cbct[1],isocenter_cbct[2])
    cbct_array = itk.GetArrayFromImage(itk.imread(image1_path))
    cbct_pixelvalues = cbct_array[:,isocenter_cbct[1],isocenter_cbct[0]] #profile_line(cbct_array,  p1, p2)
    x_axis = range(len(cbct_pixelvalues))
    plt.plot(x_axis, cbct_pixelvalues, label=label1)  

    # with scatter
    #p1 = f'{isocenter_withscatter[0]},{isocenter_withscatter[1]},0'
    #p2 = f'{isocenter_withscatter[0]},{isocenter_withscatter[1]},{size_withscatter[2]-1}'
    #p1 = (0,isocenter_withscatter[1],isocenter_withscatter[2])
    #p2 = (size_withscatter[0]-1,isocenter_withscatter[1],isocenter_withscatter[2])
    withscatter_array = itk.GetArrayFromImage(itk.imread(image2_path))
    withscatter_pixelvalues = withscatter_array[:,isocenter_withscatter[1],isocenter_withscatter[0]] #profile_line(withscatter_array,  p1, p2)
    x_axis = range(len(cbct_pixelvalues))
    plt.plot(x_axis, withscatter_pixelvalues, label=label2)  

    plt.legend()
    plt.savefig(f'profiles_z_{nameext}.png')
    plt.close()


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
    CT_path = 'CT.nii'#
    realcbct_path = 'cbct.0.nii'#
    withscatter_path = 'fdk_rotated_withscatter.mha'
    FOV_mask_path = 'mask_withscatter.mha'
    patient_mask_path = 'patient_mask.mha'

    for patient_folders in glob.glob('./cbct_images/*'):
        # go to patient folder and get histogram
        main_path=os.getcwd()
        os.chdir(patient_folders)
        print(patient_folders)
        # images name

        if os.path.exists(withscatter_path):
            match_realCBCT(realcbct_path, withscatter_path,FOV_mask_path,patient_mask_path)
            match_rennesCBCT(realcbct_path, withscatter_path,FOV_mask_path,patient_mask_path)
            match_CT(CT_path, realcbct_path, FOV_mask_path,patient_mask_path)

        os.chdir(main_path)

