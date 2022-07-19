import glob
import os
import shutil

def merge():

    # delete existing results folder if it already exists
    for path in glob.glob("results.*"):
        shutil.rmtree(path)

    for folder in glob.glob(f'run.*'):
        # merge the job results
        mergecommand = f'gate_power_merge.sh {folder}'
        os.system(mergecommand)


if __name__ == "__main__":
    merge()

