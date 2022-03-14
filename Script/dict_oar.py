OAR = {'Patient': ['patient.nii', 'Patient.nii'],
       'Parotide_G': ['ParotideG.nii', 'parotideG.nii', 'parotide_G.nii', 'Parotide_G.nii'],
       'Parotide_D': ['ParotideD.nii', 'parotideD.nii', 'Parotide_D.nii', 'parotide_D.nii'],
       'Larynx': ['Larynx.nii', 'larynx.nii', 'LARYNX.nii'], 
       'Tronc_Cerebral': ['TroncCerebral.nii', 'TRONC.nii', 'TC.nii', 'TRONCart.nii']}

Label = {'Background': 0,
        'Patient': 1,
        'Parotide_D': 1,
       'Parotide_G': 2,
       'Larynx': 3, 
       'Tronc_Cerebral': 4}

list_remove = []
for i in range(100, -1, -1):
    list_remove.append(str(i) + "_")


