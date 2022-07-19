from batchgenerators.utilities.file_and_folder_operations import *
import numpy as np
from nnunet.paths import preprocessing_output_dir
task_name = 'Task722_Submandibular_PatchSize64'
plans_fname = join(preprocessing_output_dir, task_name, 'nnUNetPlansv2.1_plans_3D.pkl')
plans = load_pickle(plans_fname)
plans['plans_per_stage'][0]['batch_size'] = 2
plans['plans_per_stage'][0]['patch_size'] = np.array((64, 64, 64))
plans['plans_per_stage'][0]['max_num_epochs'] = 200
#plans['plans_per_stage'][0]['num_pool_per_axis'] = [6, 6]
#plans['plans_per_stage'][0]['pool_op_kernel_sizes'] = [[2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2]]
#plans['plans_per_stage'][0]['conv_kernel_sizes'] = [[3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3]]
save_pickle(plans, join(preprocessing_output_dir, task_name, 'nnUNetPlans_P64_plans_3D.pkl'))
