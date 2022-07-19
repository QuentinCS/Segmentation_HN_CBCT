#!/usr/bin/env python
import itk
import sys
import glob
import os

def attenuation(proj_path):
    if not os.path.exists(proj_path):
        os.makedirs(proj_path)
    # get all the primary projections
    primary_files = glob.glob('./results.*/primary*.mha')
    for primary_filename in primary_files:
      # load the primary and flatfield
      primary = itk.imread(primary_filename)
      flatfield = itk.imread(primary_filename.replace("primary", "flatfield"))

      I_CBCT = itk.DivideImageFilter(primary,flatfield)

      attenuation = itk.LogImageFilter(I_CBCT)
      attenuation = itk.MultiplyImageFilter(attenuation, -1)#(65536-max_FF))

      attenuation_path = primary_filename.replace(f'{os.path.dirname(primary_filename)}/primary', f'{proj_path}/attenuation')
      itk.imwrite(attenuation, attenuation_path)

def attenuation_local(proj_path):
    if not os.path.exists(proj_path):
        os.makedirs(proj_path)
    # get all the primary projections
    primary_files = glob.glob('./output/primary*.mha')
    for primary_filename in primary_files:
      # load the primary and flatfield
      primary = itk.imread(primary_filename)
      flatfield = itk.imread(primary_filename.replace("primary", "flatfield"))

      I_CBCT = itk.DivideImageFilter(primary,flatfield)

      attenuation = itk.LogImageFilter(I_CBCT)
      attenuation = itk.MultiplyImageFilter(attenuation, -1)

      itk.imwrite(attenuation, primary_filename.replace('./output/primary', f'{proj_path}/attenuation_sec'))

if __name__ == "__main__":
    proj_path = sys.argv[1]
    attenuation(proj_path)
