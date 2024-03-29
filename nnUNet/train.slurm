#!/bin/bash
#SBATCH --job-name=gpu_mono          # nom du job
#SBATCH --ntasks=1                   # nombre total de taches (= nombre de GPU ici)
#SBATCH --gres=gpu:1                 # nombre de GPU (1/4 des GPU)
#SBATCH --cpus-per-task=10           # nombre de coeurs CPU par tache (1/4 du noeud 4-GPU)
# /!\ Attention, "multithread" fait reference à l'hyperthreading dans la terminologie Slurm
#SBATCH --hint=nomultithread         # hyperthreading desactive
#SBATCH --time=10:00:00              # temps maximum d'execution demande (HH:MM:SS)
#SBATCH --output=gpu_mono_TaskXXX_f0_%j.out      # nom du fichier de sortie
#SBATCH --error=gpu_mono_TaskXXX_f0_%j.out       # nom du fichier d'erreur (ici commun avec la sortie)

#Run this job with
# sbatch runTest.slurm
START_TIME=$(date +%s)
echo "---------------------------------------------------"
echo "Train Task XXX with plan nnUNetPlansV2_noMirroring"
echo "Disabling mirror data augmentation"
echo "3d_fullres, fold 0"
echo "---------------------------------------------------"
echo

module purge

# See available module with: module avail
#module load pytorch-gpu/py3/1.7.1 #it's difficult to use nnunet with this module
module load gcc/8.3.1 cuda/10.2 nccl/2.7.8-1-cuda cudnn/8.0.4.30-cuda-10.2 intel-mkl/2020.1 magma/2.5.3-cuda openmpi/4.0.2-cuda #python/3.8.2

# Activate venv with this installation and python 3.8.2
#pip install torch torchvision torchaudio
cd /gpfswork/rech/ddr/uyx67dp
source nnunet/bin/activate


#/gpfsscratch/rech/ddr/uyx67dp
export nnUNet_raw_data_base="/gpfsscratch/rech/ddr/uyx67dp/nnUNet/nnUNet_raw_data_base"
export nnUNet_preprocessed="/gpfsscratch/rech/ddr/uyx67dp/nnUNet/nnUNet_preprocessed"
export RESULTS_FOLDER="/gpfsscratch/rech/ddr/uyx67dp/nnUNet/nnUNet_trained_models"

# Execute your code 
nnUNet_plan_and_preprocess -t XXX --verify_dataset_integrity
nnUNet_train 3d_fullres nnUNetTrainerV2_noMirroring XXX 0 --npz


echo
END_TIME=$(date +%s)
echo "Total running time : $(($END_TIME - $START_TIME)) s "

