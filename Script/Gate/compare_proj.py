# Script to compare the profiles and histograms for simulations from Gate for CBCT and real CBCT projections 

import itk
import sys 
import shutil
import os
import numpy as np 
import glob
import gatetools as gt 
import matplotlib.pyplot as plt
import time

start_time = time.time()

proj_sim = '../projections'
proj_real = '../projections_real'

list_proj_sim = sorted(glob.glob(f'{proj_sim}/*.mha'))

# Open images
image_sim_1 = itk.imread(list_proj_sim[66])
image_sim_2 = itk.imread(list_proj_sim[140])
image_real = itk.imread(f'{proj_real}/merged.mhd')
image_sim_1_np = itk.array_view_from_image(image_sim_1)
image_sim_2_np = itk.array_view_from_image(image_sim_2)
image_real_np = itk.array_view_from_image(image_real)

# Get profile
profil_sim_1 = image_sim_1_np[0, 254]
profil_sim_2 = image_sim_2_np[0, 254]
profil_real_1 = image_real_np[66, 254]
profil_real_2 = image_real_np[140, 254]


# Get histograms 
hist_sim = []
hist_real = []
for i in range(np.shape(image_sim_1_np)[1]):
	for j in range(np.shape(image_sim_1_np)[2]):
		hist_sim.append(image_sim_1_np[0][i][j])
		hist_real.append(image_real_np[66][i][j])

# Plot profiles 
fig,ax = plt.subplots(figsize=(20,15))
# make a plot
ax.plot(profil_sim_1, color="red")
# set x-axis label
ax.set_xlabel("x", fontsize = 14)
# set y-axis label
ax.set_ylabel("Simulation", color="red", fontsize=14)
ax2=ax.twinx()
ax2.plot(profil_real_1, color="blue")
ax2.set_ylabel("Real", color="blue", fontsize=14)
#plt.show()
plt.savefig('profiles_1.png', dpi=600)

# Plot profiles 
fig,ax = plt.subplots(figsize=(20,15))
# make a plot
ax.plot(profil_sim_2, color="red")
# set x-axis label
ax.set_xlabel("y", fontsize = 14)
# set y-axis label
ax.set_ylabel("Simulation", color="red", fontsize=14)
ax2=ax.twinx()
ax2.plot(profil_real_2, color="blue")
ax2.set_ylabel("Real", color="blue", fontsize=14)
#plt.show()
plt.savefig('profiles_2.png', dpi=600)


# Plot profiles 
fig,ax = plt.subplots(figsize=(20,15))
# make a plot
ax.hist(hist_sim, 1000, color='red')
# set x-axis label
ax.set_xlabel("x", fontsize = 14)
# set y-axis label
ax.set_ylabel("Simulation", color='red', fontsize=14)
ax2=ax.twinx()
ax2.hist(hist_real, 1000, color='blue')
ax2.set_ylabel("Real", fontsize=14, color='blue')
#plt.show()
plt.savefig('hists.png')


plot = False
#plot = True
if plot == True:
	plt.imshow(image_sim_1[0])
	plt.show()
	plt.imshow(image_real_1[66])
	plt.show()

duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)
