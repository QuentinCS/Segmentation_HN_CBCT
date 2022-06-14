# Script to compare the profiles and histograms for simulations from Gate for CBCT and real CBCT projections 

import itk
import numpy as np 
import gatetools as gt 
import matplotlib.pyplot as plt
import time

start_time = time.time()

rec_sim = itk.imread('result_registration.mhd')
rec_real = itk.imread('../../cbct_images/1.2.840.113854.261407832220960147202645796066740913654.1/cbct.0.nii')

rec_real = gt.applyTransformation(input=rec_real, newsize=itk.size(rec_sim), neworigin=itk.origin(rec_sim), adaptive=True, force_resample=True, interpolation_mode='NN')
#rec_real = np.flip(rec_real, axis=0)
#rec_sim = np.swapaxes(rec_sim, 0, 2)
#rec_real = np.swapaxes(rec_real, 0, 2)

scale = 0.7
Slice = 140
#print(np.shape(rec_sim))
#print(np.shape(rec_real))

# Get profile
profil_sim_1 = rec_sim[Slice, 50]
profil_sim_2 = rec_sim[Slice, 100]
profil_real_1 = rec_real[Slice, 50]
profil_real_2 = rec_real[Slice, 100]

# Plot profiles 
fig,ax = plt.subplots(figsize=(20,15))
ax.plot(profil_sim_1*scale, color="red", label='CBCT Simulé')
ax.set_xlabel("x", fontsize = 14)
ax.set_ylabel("Pixel value (#CT)", fontsize=16)
ax.plot(profil_real_1, color="blue", label='CBCT Réel')
plt.plot([], [], ' ', label=f'Correction factor : {scale}')
plt.legend()
plt.savefig('profiles_1.png', dpi=400)
#plt.show()

# Plot profiles 
fig,ax = plt.subplots(figsize=(20,15))
ax.plot(profil_sim_2*scale, color="red", label='CBCT Simulé')
ax.set_xlabel("y", fontsize = 14)
ax.set_ylabel("Pixel value (#CT)", fontsize=14)
ax.plot(profil_real_2, color="blue", label='CBCT Réel')
plt.plot([], [], ' ', label=f'Correction factor : {scale}')
plt.legend()
plt.savefig('profiles_2.png', dpi=400)
#plt.show()

# Get histograms 
hist_sim = []
hist_real = []
for i in range(0, np.shape(rec_real)[0]):
	for j in range(0, np.shape(rec_real)[1]):
		if rec_sim[Slice][i][j]>10:
			hist_sim.append(rec_sim[Slice][i][j]*scale)
		if rec_real[Slice][i][j]>10:
			hist_real.append(rec_real[Slice][i][j])

# Plot histogram 
fig,ax = plt.subplots(figsize=(20,15))
ax.hist(hist_sim, 1000, color='red', label='CBCT Simulé')
ax.set_xlabel("x", fontsize = 14)
ax.set_ylabel("dN/d#CT", fontsize=14)
ax.hist(hist_real, 1000, color='blue', alpha=0.5, label='CBCT Réel')
plt.plot([], [], ' ', label=f'Correction factor : {scale}')
plt.legend()
plt.savefig('hists.png')
#plt.show()

plot = False
#plot = True
if plot == True:
	fig,ax = plt.subplots(figsize=(20,15))
	plt.subplot(1, 2, 1)
	plt.imshow(rec_sim[Slice])
	plt.subplot(1, 2, 2)
	plt.imshow(rec_real[Slice])
	plt.savefig('image.png')
	#plt.show()

duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)
