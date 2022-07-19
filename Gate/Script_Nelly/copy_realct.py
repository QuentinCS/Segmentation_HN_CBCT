
#!/usr/bin/env python
import shutil
import sys
import glob
import os

def copy_realCT():
    trainingimages_folder = '/home/nabbani/nnunet/CLB_test/cbct_images_db/cbct_images_training_v2'
    test_folder = '/home/nabbani/nnunet/CLB_test/cbct_images_db/cbct_images_test_v2'

    elastix_param_file = '/home/nabbani/nnunet/CLB_test/Parameters_Rigid.txt'
    elastix_folder = '/home/nabbani/nnunet/CLB_test/registered_pseudos'

    for patients in glob.glob('*/cbct_images/*'):
        print(patients)
        foldername = os.path.basename(patients)
        copy_directory = f'{trainingimages_folder}/{foldername}'
        if not os.path.exists(copy_directory):
            print("folder " + foldername + " not found in training folder")
            copy_directory = f'{test_folder}/{os.path.basename(patients)}'
            if not os.path.exists(copy_directory):
                print("folder " + foldername + " not found in test folder")
                break

        

        # copy real CT 
        filename = f'{patients}/CT.nii'
        if os.path.exists(filename):
            shutil.copy(filename,copy_directory)

        realct = f'{copy_directory}/CT.nii'
        realcbct = f'{patients}/cbct.0.nii'
        #simucbct = f'{copy_directory}/withscatter_beforematching.mha'
        #registeredct_simu = f'{copy_directory}/CT_registeredwithsimu.mha'
        registeredct_real = f'{copy_directory}/CT_registeredwithsreal.mha'
        # register real CT with simu cbct in the destination directory
        #elastix_command = f'elastix -f {simucbct} -m {realct} -p {elastix_param_file} -out {elastix_folder}'
        #os.system(elastix_command)

        #registered_ct_path = f'{elastix_folder}/result.0.mhd'

        #convert_command= f'gt_image_convert {registered_ct_path} -o {registeredct_simu}'
        #os.system(convert_command)


        if not os.path.exists(registeredct_real):
            # register real CT with real cbct
            elastix_command = f'elastix -f {realcbct} -m {realct} -p {elastix_param_file} -out {elastix_folder}'
            os.system(elastix_command)

            registered_ct_path = f'{elastix_folder}/result.0.mhd'

            convert_command= f'gt_image_convert {registered_ct_path} -o {registeredct_real}'
            os.system(convert_command)


if __name__ == "__main__":
    copy_realCT()

