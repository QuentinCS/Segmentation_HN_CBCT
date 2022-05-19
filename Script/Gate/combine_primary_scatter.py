# Script to combine primary and scatter simulations from Gate for CBCT

import itk
import sys 
import shutil
import os
import numpy 
import glob
import fileinput
import gatetools as gt 

# Get number of primary particles per projections for scatter 
def get_primary_per_proj(file_name):
	prim_per_proj = 0
	with open(file_name) as f:
		for line in f:
			if '/gate/application/setTotalNumberOfPrimaries' in line:
				_, prim_per_proj = line.split(' ')
	if prim_per_proj == 0:
		print('Error: missing "/gate/application/setTotalNumberOfPrimaries" line in file ')
		exit()

	return prim_per_proj

# Get sizes of the images 
def get_size(file_name):
	size = [0, 0]
	with open(file_name) as f:
		for line in f:
			if '/gate/actor/ffda/setDetectorResolution' in line:
				_, size[0], size[1] = line.split(' ')
	if size[0] == 0 or size[1] == 0 :
		print('Error: missing "/gate/actor/ffda/setDetectorResolution" line in file ')
		exit()

	return size

# Create folder for saving the combined projections
Dir = 'res_proj' 
if os.path.exists(Dir):
    shutil.rmtree(Dir)
os.makedirs(Dir)

# Get parameters values 
prim_per_proj = get_primary_per_proj('mac/scatter-patient.mac')
projection = get_primary_per_proj('mac/primary-patient.mac')
size_primary = get_size('mac/primary-patient.mac')[0]
size_scatter = get_size('mac/scatter-patient.mac')[0]
factor = prim_per_proj*pow(size_primary/size_scatter,2)

# Get list of projections 
flatfield_proj = sorted(glob.glob('run.qyx65x7v/output.7821633/flatfield*.mha'))
primary_proj = sorted(glob.glob('run.qyx65x7v/output.7821633/primary*.mha'))
scatter_proj = sorted(glob.glob('run.pym9hryo/output.7870620/secondary*.mha'))


for i in range(0, len(primary_proj)):
	print(primary_proj[i])
	flatfield = itk.imread(flatfield_proj[i])
	primary = itk.imread(primary_proj[i])
	scatter = itk.imread(scatter_proj[i])

	scatter = gt.applyTransformation(input=scatter, newsize=itk.size(primary), neworigin=itk.origin(primary), adaptive=True, force_resample=True)

	flatfield = itk.MultiplyImageFilter(flatfield, factor)
	primary = itk.MultiplyImageFilter(primary, factor)

	full = itk.AddImageFilter(primary, scatter)
	full = itk.DivideImageFilter(full, flatfield)
	full = itk.MultiplyImageFilter(full, itk.MedianImageFilter(flatfield))
	attenuation = itk.LogImageFilter(full)
	attenuation = itk.MultiplyImageFilter(attenuation, -1)
	itk.imwrite(attenuation, f'{Dir}/attenuation_{i:04d}.mha')
