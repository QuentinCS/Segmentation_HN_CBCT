import sys
import shutil
import os
import rotateCT_Gate
import glob
import count_projections

if __name__ == "__main__":
    folder_name = sys.argv[1]
    prim_per_proj = int(sys.argv[2])
    number_jobs = int(sys.argv[3])

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    os.makedirs(folder_name)

    # go to folder
    os.chdir(folder_name)

    # copy the py folder and job_files_template
    #os.makedirs('py')
    shutil.copytree('../py', 'py')

    #os.makedirs('job_files_template')
    shutil.copytree('../job_files_template', 'job_files_template')

    open("errorlog.txt", "w").close()

    # create folder to copy the reconstructed cbct images
    images_folder = 'cbct_images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Loop through the patients and copy the needed images for the simulations
    allpatients = glob.glob('../patient_database/*')
    for patient in allpatients:
        patientfolders = glob.glob(f'{patient}/input/*')
        for folder in patientfolders:
            print(folder)
            foldername=os.path.basename(folder)
            # create sim files for patients and copy CT and cbct geometry   
            simulation_folder= f'./Simulations/{foldername}'
            output_folder= f'./{images_folder}/{foldername}'

            try:
                if os.path.exists(simulation_folder):
                    shutil.rmtree(simulation_folder)
                shutil.copytree('../reference_simulation', simulation_folder)

                if os.path.exists(output_folder):
                    shutil.rmtree(output_folder)
                os.makedirs(output_folder)

                # get and rotate the CT before simulation
                shutil.copy(f'{folder}/CT.nii', f'{simulation_folder}/data')
                shutil.copy(f'{folder}/CT.nii', output_folder)
                rotateCT_Gate.applyTransfo(f'{simulation_folder}/data/CT.nii', f'{simulation_folder}/data/CT_rotated.mha',f'{folder}/cbct.0.mat')
                resizecommand=f'clitkAffineTransform -i {simulation_folder}/data/CT_rotated.mha -o {simulation_folder}/data/CT_rotated_smaller.mha --spacing=3,3,3 --transform_grid  --adaptive --pad=-1024'
                os.system(resizecommand)

                geometry_command=f'rtkelektasynergygeometry --xml {folder}/cbct.0_0.xml -o {simulation_folder}/data/elektaGeometry.xml'
                os.system(geometry_command)
                # delete half the projection angles
                #count_projections.del_projs(f'{simulation_folder}/data/elektaGeometry.xml', f'{simulation_folder}/data/elektaGeometry_lessprojections.xml',4)
            
                #shutil.copy(f'{folder}/cbct.0.nii', f'{simulation_folder}/data')
                #ROIdirName=f'{simulation_folder}/data/ROI'
                #if not os.path.exists(ROIdirName):
                #    os.mkdir(ROIdirName)

                # copy cbct and ROI images to the output images folder
                shutil.copy(f'{folder}/cbct.0.nii', output_folder)

                ROIdirName_output=f'{output_folder}/ROI'
                if not os.path.exists(ROIdirName_output):
                    os.mkdir(ROIdirName_output)
                for ROI in glob.glob(f'{folder}/?_*.nii')+glob.glob(f'{folder}/??_*.nii'):
                    #shutil.copy(ROI, ROIdirName)
                    shutil.copy(ROI, ROIdirName_output)
 
            except Exception as e:
                f = open('errorlog.txt', 'a')
                f.write(f'Error for patient {foldername}: {e}')
                f.close()      
            count_projections.update_mac_V2(prim_per_proj, number_jobs, simulation_folder)
            break      
