import glob
import os
import shutil
import fileinput

def merge():
    for simulation in glob.glob('Simulations/*'):

        # go to patient simulation folder, merge the results and then reconstruct
        main_path=os.getcwd()
        os.chdir(simulation)

        # create job file for each patient and submit

        file_name = 'merge_onepatient.job'
        shutil.copy(f'{main_path}/job_files_template/{file_name}', './')
        for line in fileinput.input(f'./{file_name}', inplace=True):
            if 'cd ~/sps/' in line:
                print(f'cd {os.getcwd()}')
            elif 'python ~/sps/' in line:
                print(f'python {main_path}/py/merge_jobs_onepatient.py')
            else:
                print(line, end='')

        mergecommand = f'qsub merge_onepatient.job'
        os.system(mergecommand)

        # count the number of completed jobs
        for results_dir in glob.glob(f'run.*'):
            output_dir = glob.glob(f'{results_dir}/output.*')
            #if os.path.isfile(f'{output_dir[0]}/primary0000.mha'):
            #    primary_folder = results_dir
            if os.path.isfile(f'{output_dir[0]}/secondary0000.mha'):
                secondary_folder = results_dir
        #secondary_runfolder = secondary_folder.replace('results','run')
        job_completed = len(glob.glob(f"{secondary_folder}/output.*"))

        with open(f"num_completed_jobs.txt", "w") as f:
            f.write(f'{job_completed}')

        os.chdir(main_path)


if __name__ == "__main__":
    merge()

