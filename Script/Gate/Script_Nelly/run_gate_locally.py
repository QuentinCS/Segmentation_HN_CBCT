import glob
import os
import sys
import shutil
import rotateCT_Gate
import count_projections
import numpy as np

#primaries_per_proj=1000
def run_simulation_old(primaries_per_proj):
    open("errorlog.txt", "w").close()
    allpatients = glob.glob('./patient_database/*')
    for patient in allpatients:
        patientfolders = glob.glob(f'{patient}/input/*')
        for folder in patientfolders:
            foldername=os.path.basename(folder)
            # create sim files for patients and copy CT and cbct geometry   
            simulation_folder= f'./Simulations/{foldername}'

            try:
                if os.path.exists(simulation_folder):
                    shutil.rmtree(simulation_folder)
                shutil.copytree('reference_simulation', simulation_folder)

                # get and rotate the CT before simulation
                shutil.copy(f'{folder}/CT.nii', f'{simulation_folder}/data')
                rotateCT_Gate.applyTransfo(f'{simulation_folder}/data/CT.nii', f'{simulation_folder}/data/CT_rotated.mha',f'{folder}/cbct.0.mat')
                resizecommand=f'clitkAffineTransform -i {simulation_folder}/data/CT_rotated.mha -o {simulation_folder}/data/CT_rotated_smaller.mha --spacing=3,3,3 --transform_grid  --adaptive --pad=-1024'
                os.system(resizecommand)

                geometry_command=f'rtkelektasynergygeometry --xml {folder}/cbct.0_0.xml -o {simulation_folder}/data/elektaGeometry.xml'
                os.system(geometry_command)
                # delete half the projection angles
                count_projections.del_projs(f'{simulation_folder}/data/elektaGeometry.xml', f'{simulation_folder}/data/elektaGeometry_halfprojections.xml')

                shutil.copy(f'{folder}/cbct.0.nii', f'{simulation_folder}/data')

                # copy ROI images
                ROIdirName=f'{simulation_folder}/data/ROI'
                if not os.path.exists(ROIdirName):
                    os.mkdir(ROIdirName)
                for ROI in glob.glob(f'{folder}/?_*.nii')+glob.glob(f'{folder}/??_*.nii'):
                    shutil.copy(ROI, ROIdirName)

            except Exception as e:
                f = open('errorlog.txt', 'a')
                f.write(f'Error for patient {foldername}: {e}')
                f.close()            
    
            else:
                # go to patient simulation folder and run the simulations jobs
                current=os.getcwd()
                os.chdir(simulation_folder)

                try:

                    # change number of primaries in the macros according to projections
                    count_projections.update_mac(primaries_per_proj,1)

                    # run the simulations
                    gatecommand_primary = 'Gate mac/primary-patient.mac'
                    os.system(gatecommand_primary)
                    gatecommand_scatter = f'Gate mac/scatter-patient.mac'
                    os.system(gatecommand_scatter)

                except Exception as e:
                    f = open('errorlog.txt', 'a')
                    f.write(f'Error for patient {foldername}: {e}')
                    f.close()   

                os.chdir(current)


def run_simulation(primaries_per_proj):
    for simulation_folder in glob.glob('./Simulations/*'):
        # go to patient simulation folder and run the simulations jobs
        main_path=os.getcwd()
        os.chdir(simulation_folder)

        # change number of primaries in the macros according to projections
        count_projections.update_mac(primaries_per_proj,1)

        # run the simulations
        #gatecommand_primary = 'Gate mac/primary-patient.mac'
        gatecommand_primary = 'Gate mac/primary-patient.mac'
        os.system(gatecommand_primary)
        gatecommand_scatter = f'Gate mac/scatter-patient.mac'
        os.system(gatecommand_scatter)

        os.chdir(main_path)

if __name__ == "__main__":
    prim_per_proj = int(sys.argv[1])
    run_simulation(prim_per_proj)
