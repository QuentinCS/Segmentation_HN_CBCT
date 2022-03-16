OAR = {'Patient': ['patient.nii', 'Patient.nii', 'patientcf.nii'],
       'Parotide_G': ['ParotideG.nii', 'parotideG.nii', 'parotide_G.nii', 'Parotide_G.nii', 'ParotidGlandLeft.nii', 'parotG.nii', 'Parotideg.nii', 'ParotideGcf.nii', 'PAROTIDEG.nii', 'PAROTIDEGAUCHE.nii', 'parotideg.nii', 'parotideg1.nii'],
       'Parotide_D': ['ParotideD.nii', 'parotideD.nii', 'Parotide_D.nii', 'parotide_D.nii', 'ParotidGlandRight.nii', 'parotD.nii', 'Parotided.nii', 'ParotideDcf.nii', 'PAROTIDEDROITE.nii', 'parotidedte.nii', 'parotidedte1.nii'],
       'Larynx': ['Larynx.nii', 'larynx.nii', 'LARYNX.nii', 'LarynxSansCTV.nii', 'larynx1.nii'], 
       'Tronc_Cerebral': ['TroncCerebral.nii', 'TRONC.nii', 'TC.nii', 'TRONCart.nii', 'tronccerebral.nii', 'tronc.nii', 'troncART.nii', 'TroncART.nii', 'tronccerebralcf.nii', 'Tronccerebral.nii']}

Label = {'Background': 0,
        'Patient': 1,
        'Parotide_D': 1,
       'Parotide_G': 2,
       'Larynx': 3, 
       'Tronc_Cerebral': 4}

list_remove = []
for i in range(100, -1, -1):
    list_remove.append(str(i) + "_")


