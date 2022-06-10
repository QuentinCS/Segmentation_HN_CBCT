import glob
import os
import sys
import get_atten_primary
import get_atten_scatter
import shutil
import fileinput

def reconstruct(primaries_per_proj,num_jobs):
    # folder to copy the results to
    images_folder = 'cbct_images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    for simulation in glob.glob('./Simulations/*'):
        # go to patient simulation folder and reconstruct
        main_path=os.getcwd()
        os.chdir(simulation)

        # create job file for each patient and submit
        file_name = 'reconstruct_onepatient.job'
        shutil.copy(f'{main_path}/job_files_template/{file_name}', './')
        for line in fileinput.input(f'./{file_name}', inplace=True):
            if 'cd ~/sps/' in line:
                print(f'cd {os.getcwd()}')
            elif 'python ~/sps/' in line:
                print(f'python {main_path}/py/reconstruct_job_onepatient.py {primaries_per_proj} {num_jobs}')
            else:
                print(line, end='')

        reconstructcommand = f'qsub reconstruct_onepatient.job'
        os.system(reconstructcommand)

        os.chdir(main_path)

if __name__ == "__main__":
    prim_per_proj = int(sys.argv[1])
    num_jobs = int(sys.argv[2])
    reconstruct(prim_per_proj,num_jobs)

