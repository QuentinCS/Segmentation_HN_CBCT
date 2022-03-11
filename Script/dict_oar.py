OAR = {'Patient': ['patient.nii', 'Patient.nii'],
       'Parotide_G': ['ParotideG.nii', 'parotideG.nii', 'parotide_G.nii', 'Parotide_G'],
       'Parotide_D': ['ParotideD.nii', 'parotideD.nii', 'Parotide_D.nii', 'parotide_D.nii'],
       'Larynx': ['Larynx.nii', 'larynx.nii', 'LARYNX.nii'], 
       'Tronc_Cerebral': ['TroncCerebral.nii', 'TRONC.nii', 'TC.nii', 'TRONCart.nii']}


Name = {'Patient': '0_Patient.nii',
        'Parotide_D': '1_Parotide_D',
       'Parotide_G': '2_Parotide_G',
       'Larynx': '3_Larynx', 
       'Tronc_Cerebral': '4_Tronc_Cerebral'}


list_remove = []
for i in range(100, -1, -1):
    list_remove.append(str(i) + "_")


