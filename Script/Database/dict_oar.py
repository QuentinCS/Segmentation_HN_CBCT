OAR = {'Patient': ['patient.nii', 'Patient.nii', 'patientcf.nii'],
       'Parotide_G': ['ParotideG.nii', 'parotideG.nii', 'parotide_G.nii', 'Parotide_G.nii', 'ParotidGlandLeft.nii', 'parotG.nii', 'Parotideg.nii', 'ParotideGcf.nii', 'PAROTIDEG.nii', 'PAROTIDEGAUCHE.nii', 'parotideg.nii', 'parotideg1.nii', 'parotideGcf.nii'],
       'Parotide_D': ['ParotideD.nii', 'parotideD.nii', 'Parotide_D.nii', 'parotide_D.nii', 'ParotidGlandRight.nii', 'parotD.nii', 'Parotided.nii', 'ParotideDcf.nii', 'PAROTIDEDROITE.nii', 'parotidedte.nii', 'parotidedte1.nii', 'PAROTIDED', 'ParotideDcf.nii'],
       'Larynx': ['Larynx.nii', 'larynx.nii', 'LARYNX.nii', 'LarynxSansCTV.nii', 'larynx1.nii'], 
       'Tronc_Cerebral': ['TroncCerebral.nii', 'TRONC.nii', 'TC.nii', 'tronccerebral.nii', 'tronc.nii', 'tronccerebralcf.nii', 'Tronccerebral.nii', 'troncc?r?bral.nii', 'tronccerebralcf.nii'],
       'Trachee': ['Trachee.nii', 'TRACHEE.nii', 'trachee.nii', 'Tracheecf.nii', 'trachee1.nii'],
       'Cavite_Buccale': ['CaviteBuccale.nii', 'cavitebuccale.nii', 'cavit?buccale.nii', 'Cacbuccale.nii', 'cavite_buccale.nii', 'caviteorale.nii', 'CAVITEBUCCALE.nii', 'cavorale.nii', 'cavbuccale.nii', 'CavBuccale.nii', 'CAVBUCCALE.nii'],
       'Moelle': ['Moelle.nii', 'moellecf.nii'],
       'Oesophage': ['Oesophage.nii', 'oeso.nii', 'oesophage.nii', 'Oeso.nii'],
       'Thyroide': ['THYROIDE.nii', 'thyroide.nii', 'Thyro?de.nii'],
       'Mandibule': ['Mandibule.nii', 'Mandible.nii', 'mandib.nii', 'mandibule.nii', 'mandibulecf.nii'],
       'Chiasma': ['Chiasma.nii', 'CHIASMA.nii', 'chiasma.nii', 'CHIASM', 'chiasma1.nii']}


Label = {'Background': 0,
        'Patient': 1,
        'Parotide_D': 2,
       'Parotide_G': 3,
       'Larynx': 4, 
       'Tronc_Cerebral': 5,
       'Trachee': 6,
       'Cavite_Buccale': 7,
       'Moelle': 8,
       'Oesophage': 9,
       'Thyroide': 10,
       'Mandibule': 11,
       'Chiasma': 12}

list_remove = []
for i in range(100, -1, -1):
    list_remove.append(str(i) + "_")


