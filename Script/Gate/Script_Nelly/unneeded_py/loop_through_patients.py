import glob
import os
import shutil
import steps_per_patient

primaries_per_proj=10
allpatients = glob.glob('./patient_database/*')
for patient in allpatients:
    patientfolders = glob.glob(f'{patient}/input/*')
    for folder in patientfolders:
        foldername=os.path.basename(folder)
        # create sim files for patients and copy CT and cbct geometry   
        simulation_folder= f'./Simulations/{foldername}'
        shutil.rmtree(simulation_folder)
        shutil.copytree('reference_simulation', simulation_folder)
        convert_command=f'clitkImageConvert --vv {folder}/CT.nii {simulation_folder}/data/CT.mha'
        os.system(convert_command)
        geometry_command=f'rtkelektasynergygeometry --xml {folder}/cbct.0_0.xml -o {simulation_folder}/data/elektaGeometry.xml'
        os.system(geometry_command)
        shutil.copy(f'{folder}/cbct.0.nii', f'{simulation_folder}/data')
        # copy ROI images
        ROIdirName=f'{simulation_folder}/data/ROI'
        if not os.path.exists(ROIdirName):
            os.mkdir(ROIdirName)
        for ROI in glob.glob(f'{folder}/?_*.nii')+glob.glob(f'{folder}/??_*.nii'):
            shutil.copy(ROI, ROIdirName)
        # go to patient simulation folder and run the simulations and reconstruction
        current=os.getcwd()
        os.chdir(simulation_folder)
        steps_per_patient.steps(primaries_per_proj)
        os.chdir(current)
