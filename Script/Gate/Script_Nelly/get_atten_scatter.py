
#!/usr/bin/env python
import itk
import sys
import glob
import os
import numpy as np
import gatetools as gt

def attenuation(prim_per_proj,proj_path,num_jobs):
    if not os.path.exists(proj_path):
        os.makedirs(proj_path)
    interp_secfolder = 'interpolated_secondaries'
    if not os.path.exists(interp_secfolder):
        os.makedirs(interp_secfolder)

    for results_dir in glob.glob('./results.*'):
        if os.path.isfile(f'{results_dir}/primary0000.mha'):
            primary_folder = results_dir
        elif os.path.isfile(f'{results_dir}/secondary0000.mha'):
            secondary_folder = results_dir

    #IMC=PMC×#primaries_per_projection×(512/128)^2+SMC 
    size_primary = 512
    size_scatter = 64
    # get the number of jobs actually completed from the run folder of the scatter simulation
    #secondary_runfolder = secondary_folder.replace('results','run')
    #job_completed = len(glob.glob(f"{secondary_runfolder}/output.*"))
    with open(f"num_completed_jobs.txt", "r") as f:
        job_completed = int(f.readline())

    factor = (prim_per_proj * job_completed/num_jobs) * pow(size_primary/size_scatter,2)

    # get all the primary projections
    primary_files = sorted(glob.glob(f'{primary_folder}/primary*.mha'))
    interpolate_secondaries(secondary_folder,interp_secfolder, 4, len(primary_files))

    for projnum, primary_filename in enumerate(primary_files):
      # load the primary, secondary, and flatfield
      primary = itk.imread(primary_filename)
      flatfield = itk.imread(primary_filename.replace("primary", "flatfield"))
      #not needed anymore - secondaries only have half the projections, so the secondary projection number = projnum/2
      #second_projnum = projnum // 4
      #secondary = itk.imread(f'{secondary_folder}/secondary{second_projnum:04d}.mha')
      secondary = itk.imread(f'{interp_secfolder}/secondary{projnum:04d}.mha')
      resizedsecondary = gt.applyTransformation(input=secondary, newsize=itk.size(primary), neworigin=itk.origin(primary), adaptive=True, force_resample=True)

      flatfield = itk.MultiplyImageFilter(flatfield,factor)

      prim_second = itk.AddImageFilter(itk.MultiplyImageFilter(primary,factor),resizedsecondary)
      #flatfield_sq = itk.MultiplyImageFilter(flatfield,flatfield) 

      S = itk.DivideImageFilter(prim_second,flatfield)
      S = itk.MultiplyImageFilter(S,itk.MedianImageFilter(flatfield))
      attenuation = itk.LogImageFilter(S)
      #attenuation = itk.LogImageFilter(itk.DivideImageFilter(prim_second,flatfield))
      attenuation = itk.MultiplyImageFilter(attenuation, -1)

      attenuation_path = primary_filename.replace(f'{os.path.dirname(primary_filename)}/primary', f'{proj_path}/attenuation_sec')
      itk.imwrite(attenuation, attenuation_path)

def attenuation_local(prim_per_proj,proj_path):
    if not os.path.exists(proj_path):
        os.makedirs(proj_path)
    interp_secfolder = 'interpolated_secondaries'
    if not os.path.exists(interp_secfolder):
        os.makedirs(interp_secfolder)

    #IMC=PMC×#primaries_per_projection×(512/128)^2+SMC 
    size_primary = 512
    size_scatter = 64
    factor = prim_per_proj*pow(size_primary/size_scatter,2)

    # get all the primary projections
    primary_files = sorted(glob.glob('./output/primary*.mha'))
    interpolate_secondaries(secondary_folder,interp_secfolder, 4, len(primary_files))

    for projnum, primary_filename in enumerate(primary_files):
      # load the primary, secondary, and flatfield
      primary = itk.imread(primary_filename)
      flatfield = itk.imread(primary_filename.replace("primary", "flatfield"))

      #not needed anymore - secondaries only have half the projections, so the secondary projection number = projnum/2
      #second_projnum = projnum // 4
      #secondary = itk.imread(f'./output/secondary{second_projnum:04d}.mha')
      secondary = itk.imread(f'{interp_secfolder}/secondary{projnum:04d}.mha')
      resizedsecondary = gt.applyTransformation(input=secondary, newsize=itk.size(primary), neworigin=itk.origin(primary), adaptive=True, force_resample=True)

      flatfield = itk.MultiplyImageFilter(flatfield,factor)

      prim_second = itk.AddImageFilter(itk.MultiplyImageFilter(primary,factor),resizedsecondary)
      #flatfield_sq = itk.MultiplyImageFilter(flatfield,flatfield) 

      S = itk.DivideImageFilter(prim_second,flatfield)
      S = itk.MultiplyImageFilter(S,itk.MedianImageFilter(flatfield))
      attenuation = itk.LogImageFilter(S)
      #attenuation = itk.LogImageFilter(itk.DivideImageFilter(prim_second,flatfield))

      attenuation = itk.MultiplyImageFilter(attenuation, -1)

      itk.imwrite(attenuation, primary_filename.replace('./output/primary', f'{proj_path}/attenuation_sec'))


def interpolate_secondaries(input_folder,output_folder, factor, target_numprojs):
    sec_numprojs = len(glob.glob(f'./{input_folder}/secondary????.mha'))

    img0 = itk.imread(f'./{input_folder}/secondary0000.mha') 
    img_origin = itk.origin(img0)
    img_spacing = itk.spacing(img0)

    image_ind = 0
    for projnum in range(sec_numprojs-1):
        # get 
        image1 = f'./{input_folder}/secondary{projnum:04d}.mha'
        image2 = f'./{input_folder}/secondary{projnum+1:04d}.mha'

        img1_array = itk.GetArrayFromImage(itk.imread(image1))
        img2_array = itk.GetArrayFromImage(itk.imread(image2))

        # save the first image
        itk.imwrite(itk.imread(image1),  f'./{output_folder}/secondary{image_ind:04d}.mha')

        # interpolate xfactor images between those 2 images
        image_interpolate_recurrence(img1_array,img2_array,image_ind,image_ind+factor,output_folder,img_origin, img_spacing)
        image_ind = image_ind+factor

    # read the last image and save it until the target_numprojs is reached
    lastimage = itk.imread(f'./{input_folder}/secondary{sec_numprojs-1:04d}.mha')
    while image_ind < target_numprojs:
        itk.imwrite(lastimage,  f'./{output_folder}/secondary{image_ind:04d}.mha')
        image_ind = image_ind +1


def image_interpolate_recurrence(image1,image2,ind1,ind2,output_folder,img_origin,img_spacing):
    avg_img = (image1+image2)/2
    new_ind = (ind1+ind2)/2
    integer_ind = int(new_ind)
    if (new_ind == integer_ind): # even number
        # save this projection
        output_imagename = f'./{output_folder}/secondary{int(integer_ind):04d}.mha'
        outputimage = itk.GetImageFromArray(avg_img)
        outputimage.SetOrigin(img_origin)
        outputimage.SetSpacing(img_spacing)
        itk.imwrite( outputimage, output_imagename)

        # check if can divide more
        if integer_ind-ind1 > 1:
            # call this function again twice, once to the left and once to the right
            image_interpolate_recurrence(image1,avg_img,ind1,integer_ind,output_folder,img_origin,img_spacing)
            image_interpolate_recurrence(avg_img,image2,integer_ind,ind2,output_folder,img_origin,img_spacing)

    else:
        # check if can divide more
        if new_ind-ind1 > 1:
            # call this function again twice, once to the left and once to the right
            image_interpolate_recurrence(image1,avg_img,ind1,int(math.ceil(new_ind)),output_folder,img_origin,img_spacing)
            image_interpolate_recurrence(avg_img,image2,int(math.floor(new_ind)),ind2,output_folder,img_origin, img_spacing)


if __name__ == "__main__":
    prim_per_proj = int(sys.argv[1])
    proj_path = sys.argv[2]
    num_jobs = int(sys.argv[3])
    attenuation(prim_per_proj,proj_path,num_jobs)

