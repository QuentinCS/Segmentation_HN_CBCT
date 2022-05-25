# Script to combine primary and scatter simulations from Gate for CBCT

import itk
import sys 
import shutil
import os
import numpy 
import glob
import gatetools as gt 
import time

# Get number of primary particles per projections for scatter 
def get_primary_per_proj(file_name):
	prim_per_proj = 0
	with open(file_name) as f:
		for line in f:
			if '/gate/application/setTotalNumberOfPrimaries' in line:
				_, prim_per_proj = line.split()
	if prim_per_proj == 0:
		print('Error: missing "/gate/application/setTotalNumberOfPrimaries" line in file ')
		exit()

	return prim_per_proj

# Get sizes of the images 
def get_size(file_name):
	size = 0
	with open(file_name) as f:
		for line in f:
			if '/gate/actor/ffda/setDetectorResolution' in line:
				_, size, _ = line.split()
	if size == 0:
		print('Error: missing "/gate/actor/ffda/setDetectorResolution" line in file ')
		exit()
	return size

start_time = time.time()

# Create folder for saving the combined projections
Dir = 'projections' 
if os.path.exists(Dir):
    shutil.rmtree(Dir)
os.makedirs(Dir)

# Get parameters values 
prim_per_proj = int(get_primary_per_proj('mac/scatter-patient.mac'))
projection = int(get_primary_per_proj('mac/primary-patient.mac'))
size_primary = int(get_size('mac/primary-patient.mac'))
size_scatter = int(get_size('mac/scatter-patient.mac'))
factor = prim_per_proj*pow(size_primary/size_scatter,2)

# Get list of projections 
flatfield_proj = sorted(glob.glob('run*/output*/flatfield????.mha'))
primary_proj = sorted(glob.glob('run*/output*/primary????.mha'))
scatter_proj = sorted(glob.glob('run*/output*/secondary????.mha'))

for i in range(0, len(primary_proj)):
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

print("Projection combined!")

# Create folder for saving the reconstruction
dir_rec = 'reconstruct' 
if os.path.exists(dir_rec):
    shutil.rmtree(dir_rec)
os.makedirs(dir_rec)

# Reconstruct CBCT with FDK 
print("Reconstruction ...")
fdkcommand = f'rtkfdk -p {Dir} -r attenuation.*mha --pad=0.1 -o reconstruct/fdk.mha -g data/elektaGeometry.xml'
os.system(fdkcommand)

duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)
