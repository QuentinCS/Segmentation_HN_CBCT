import glob
import os

def count_jobs_per_patient():

    for simulation in glob.glob('./Simulations/*'):
        # create a text in the patient folder and save the number of completed jobs 
        # count the number of completed jobs
        for results_dir in glob.glob(f'{simulation}/results.*'):
            if os.path.isfile(f'{results_dir}/primary0000.mha'):
                primary_folder = results_dir
            elif os.path.isfile(f'{results_dir}/secondary0000.mha'):
                secondary_folder = results_dir
        secondary_runfolder = secondary_folder.replace('results','run')
        job_completed = len(glob.glob(f"{secondary_runfolder}/output.*"))

        with open(f"{simulation}/num_completed_jobs.txt", "w") as f:
            f.write(f'{job_completed}')

if __name__ == "__main__":
    #prim_per_proj = int(sys.argv[1])
    #num_jobs = int(sys.argv[2])
    count_jobs_per_patient()

