from xml.dom import minidom
import fileinput
import sys
import shutil
import os

def create_files(prim_per_proj,number_jobs):
    current_path=os.getcwd()

    # create and edit 4 files: simulation.job, merge.job, and reconstruct.job, the template for the files is in the job_files_template folder
    file_name = 'simulation.job'
    shutil.copy(f'job_files_template/{file_name}', './')
    for line in fileinput.input(f'./{file_name}', inplace=True):
        if 'cd ~/sps/' in line:
            print(f'cd {current_path}')
        elif 'python ~/sps/' in line:
            print(f'python {current_path}/py/job_gate.py {prim_per_proj} {number_jobs}')
        else:
            print(line, end='')

    file_name = 'merge_all.job'
    shutil.copy(f'job_files_template/{file_name}', './')
    for line in fileinput.input(f'./{file_name}', inplace=True):
        if 'cd ~/sps/' in line:
            print(f'cd {current_path}')
        elif 'python ~/sps/' in line:
            print(f'python {current_path}/py/merge_jobs_all.py')
        else:
            print(line, end='')

    file_name = 'reconstruct_all.job'
    shutil.copy(f'job_files_template/{file_name}', './')
    for line in fileinput.input(f'./{file_name}', inplace=True):
        if 'cd ~/sps/' in line:
            print(f'cd {current_path}')
        elif 'python ~/sps/' in line:
            print(f'python {current_path}/py/reconstruct_job_all.py {prim_per_proj} {number_jobs}')
        else:
            print(line, end='')

if __name__ == "__main__":
    prim_per_proj = int(sys.argv[1])
    number_jobs = int(sys.argv[2])
    create_files(prim_per_proj,number_jobs)
