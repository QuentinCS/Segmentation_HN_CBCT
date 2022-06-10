import glob
import os
import shutil

def merge():
    for simulation in glob.glob('./Simulations/*'):
        # go to patient simulation folder, merge the results and then reconstruct
        current=os.getcwd()
        os.chdir(simulation)

        # delete output folder if it already exists
        if os.path.exists('output'):
            shutil.rmtree('output')
        os.makedirs('output', exist_ok=True)

        for folder in glob.glob(f'run.*'):
            # merge the job results
            mergecommand = f'gate_power_merge.sh {folder}'
            os.system(mergecommand)

            # copy the results to output folder
            results_folder = folder.replace('run.','results.')
            for filename in os.listdir(results_folder):
                src = os.path.join(f'{results_folder}',filename)
                dst = os.path.join('output',filename)
                if os.path.isfile(src):
                    shutil.copyfile(src, dst)
            #shutil.copytree(f'{results_folder}','output',dirs_exist_ok=True)

        os.chdir(current)


if __name__ == "__main__":
    merge()

