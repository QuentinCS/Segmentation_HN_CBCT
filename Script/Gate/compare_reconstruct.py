# Script to compare the profiles and histograms for simulations from Gate for CBCT and real CBCT projections 

import itk
import numpy as np 
import gatetools as gt 
import matplotlib.pyplot as plt
import time

def is_in_sphere(a, b, c, R):
    if (a*a+ b*b + c*c) <= R*R:
        return True
    else:
        return False

start_time = time.time()

rec_sim = itk.imread('result_registration.mhd')
rec_real = itk.imread('../../cbct_images/1.2.840.113854.261407832220960147202645796066740913654.1/cbct.0.nii')

rec_real = gt.applyTransformation(input=rec_real, newsize=itk.size(rec_sim), neworigin=itk.origin(rec_sim), adaptive=True, force_resample=True, interpolation_mode='NN')
#rec_real = np.flip(rec_real, axis=0)
#rec_sim = np.swapaxes(rec_sim, 0, 2)
#rec_real = np.swapaxes(rec_real, 0, 2)


# Creation of spherical mask
rec_real_np = itk.array_from_image(rec_real)
mask_sphere = rec_real_np.copy()
mask_sphere.fill(0)
for i in range(-int(np.shape(mask_sphere)[0]/2), int(np.shape(mask_sphere)[0]/2)):
	for j in range(-int(np.shape(mask_sphere)[1]/2), int(np.shape(mask_sphere)[1]/2)):
		for k in range(-int(np.shape(mask_sphere)[2]/2), int(np.shape(mask_sphere)[2]/2)):
			if is_in_sphere(i, j, k, 110) == True:
				mask_sphere[i+int(np.shape(mask_sphere)[0]/2)][j+int(np.shape(mask_sphere)[1]/2)][k+int(np.shape(mask_sphere)[0]/2)] = 1

# Application of mask to analyse same region
mask = itk.image_from_array(mask_sphere.astype(np.float32))
rec_real = itk.image_from_array(rec_real_np.astype(np.float32))

mask1 = gt.applyTransformation(input=mask, like=rec_sim)
mask2 = gt.applyTransformation(input=mask, like=rec_real)
simu_resized = itk.MultiplyImageFilter(rec_sim, mask1)
real_resized = itk.MultiplyImageFilter(rec_real, mask2)


scale = 0.68
Slice = 140
simu_resized = itk.MultiplyImageFilter(simu_resized, scale)
#print(np.shape(rec_sim))
#print(np.shape(rec_real))

# Get profile
profil_sim_1 = simu_resized[Slice, 50]
profil_sim_2 = simu_resized[Slice, 150]
profil_real_1 = real_resized[Slice, 50]
profil_real_2 = real_resized[Slice, 150]

# Plot profiles 
fig,ax = plt.subplots(figsize=(20,15))
ax.plot(profil_sim_1, color="red", label='CBCT Simulé')
ax.set_xlabel("x", fontsize = 14)
ax.set_ylabel("Pixel value (#CT)", fontsize=16)
ax.plot(profil_real_1, color="blue", label='CBCT Réel')
plt.plot([], [], ' ', label=f'Correction factor : {scale}')
plt.legend()
plt.savefig('profiles_1.png', dpi=400)
#plt.show()

# Plot profiles 
fig,ax = plt.subplots(figsize=(20,15))
ax.plot(profil_sim_2, color="red", label='CBCT Simulé')
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
for i in range(0, np.shape(real_resized)[0]):
	for j in range(0, np.shape(real_resized)[1]):
		if simu_resized[Slice][i][j]>10:
			hist_sim.append(simu_resized[Slice][i][j])
		if real_resized[Slice][i][j]>10:
			hist_real.append(real_resized[Slice][i][j])

# Plot histogram 
fig,ax = plt.subplots(figsize=(20,15))
ax.hist(hist_sim, 1000, color='red', label='CBCT Simulé')
ax.set_xlabel("#CT", fontsize = 14)
ax.set_ylabel("dN/d#CT", fontsize=14)
ax.hist(hist_real, 1000, color='blue', alpha=0.5, label='CBCT Réel')
plt.plot([], [], ' ', label=f'Correction factor : {scale}')
plt.xlim([0, 3500])
plt.legend()
plt.savefig('hists.png')
#plt.show()

#plot = False
plot = True
if plot == True:
	fig,ax = plt.subplots(figsize=(20,15))
	plt.subplot(1, 2, 1)
	plt.gca().set_title('CBCT Simulé')
	plt.imshow(simu_resized[Slice])
	plt.subplot(1, 2, 2)
	plt.gca().set_title('CBCT Réel')
	plt.imshow(real_resized[Slice])
	plt.savefig('image.png')
	#plt.show()

duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)
