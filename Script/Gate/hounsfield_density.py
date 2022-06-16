import matplotlib.pyplot as plt
import numpy as np

# Density and HU units from Schneider 2000
rho = [0.26, 0.93, 0.95, 0.97, 0.99, 1.02, 1.01, 1.03, 1.03, 1.02, 1.03, 1.03, 1.04, 1.04, 1.04, 1.04, 1.04, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05, 1.06, 1.05, 1.05, 1.07, 1.06, 1.06, 1.06, 1.06, 1.06, 1.07, 1.09, 1.09, 1.09, 1.12, 1.25, 1.29, 1.3, 1.33, 1.33, 1.33, 1.33, 1.36, 1.38, 1.39, 1.39, 1.41, 1.41, 1.42, 1.42, 1.43, 1.46, 1.46, 1.46, 1.49, 1.52, 1.61, 1.68, 1.75, 1.92]
HU = [-741, -98, -77, -55, -37, -1, 13, 14, 23, 26, 27, 29, 32, 34, 34, 36, 40, 40, 41, 41, 41, 42, 43, 43, 43, 43, 43, 44, 45, 45, 46, 46, 49, 53, 54, 54, 56, 56, 63, 72, 74, 77, 100, 385, 454, 466, 514, 526, 538, 538, 586, 599, 621, 636, 657, 658, 672, 688, 702, 742, 756, 756, 805, 843, 999, 1113, 1239, 1524]

rho_2 = []
HU_2 = []
i = 0

# Select data in the linera region after 100 HU
for i in range(len(rho)):
	if HU[i] > 100:
		rho_2.append(rho[i])
		HU_2.append(HU[i])

# Linear fit 
fit_param = np.polyfit(rho_2, HU_2, 1)
fit = np.poly1d(fit_param) 
print(fit_param)

# Plot 
fig = plt.figure(figsize=(20, 10))
plt.plot(rho, HU, label='Label')
plt.plot(rho_2, fit(rho_2), label=f'Fit \nHU = {fit_param[0]:.2f}' +r' $\rho$' + f'  {fit_param[1]:.2f}')
plt.ylabel(r'HU (-)')
plt.xlabel(r'$\rho \ (g.cm^{-3})$')
plt.legend(fontsize=20)
plt.savefig(f'Houndsfield_unit.pdf')
#plt.show()

# Estimation of HU for dentin and enamel tooth 
dentin = 1.66
enamel = 2.04
print(f'HU unit for dentin tooth : {fit(dentin)}')
print(f'HU unit for enamel tooth : {fit(enamel)}')
print(f'HU unit for 1.97 : {fit(1.97)}')
print(f'HU unit for 2.72 : {fit(2.72)}')





