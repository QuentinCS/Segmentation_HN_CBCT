 # Script to check if the esophagus is homogenenous in shape in the training dataset and in the predictions
import gatetools as gt
import time
import sys
import itk
import os
import glob

start_time = time.time()


i = 0
a = False
name = 'sCBCT_HN_%.3i.nii.gz'%(i)
train = 'Task704_Esophagus/labelsTr/sCBCT_HN_%.3i.nii.gz'%(i)


while i < 92:
   if os.path.exists(train):
        if a == False:
            image_itk = itk.imread(train)
            image = itk.array_view_from_image(image_itk)
            eso = image.copy()
            eso.fill(0)
            mask = image==2
            eso[mask] = 1
            a = True
 
        else:
            image_itk2 = itk.imread(train)
            image_rescale = gt.applyTransformation(input=image_itk2, like=image_itk, force_resample=True, interpolation_mode='NN')
            image_2 = itk.array_view_from_image(image_rescale)
            eso_2 = image_2.copy()
            eso_2.fill(0)
            mask_2 = image_2==2
            eso_2[mask_2] = 1
            eso += eso_2

   i += 1
   train = 'Task704_Esophagus/labelsTr/sCBCT_HN_%.3i.nii.gz'%(i)



pred = glob.glob('/export/home/qchaine/nnUnet/nnUNet/nnUNet_trained_models/nnUNet/ensembles/Task704_Esophagus/Predictions/*.gz')

for prediction in pred:
    if prediction == pred[0]:
        image_pred_itk = itk.imread(prediction)
        image_pred = itk.array_view_from_image(image_pred_itk)
        eso_pred = image_pred.copy()
        eso_pred.fill(0)
        mask_pred = image_pred==2
        eso_pred[mask_pred] = 1
 
    else:
        image_pred_itk2 = itk.imread(prediction)
        image_pred_rescale = gt.applyTransformation(input=image_pred_itk2, like=image_pred_itk, force_resample=True, interpolation_mode='NN')
        image_pred_2 = itk.array_view_from_image(image_pred_rescale)
        eso_pred_2 = image_pred_2.copy()
        eso_pred_2.fill(0)
        mask_pred_2 = image_pred_2==2
        eso_pred_2[mask_pred_2] = 1
        eso_pred += eso_pred_2   



save = itk.image_from_array(eso)
save.CopyInformation(image_itk) # Important to save the image with correct spacing, size!!
itk.imwrite(save, 'Esophagus_sum.nii')


save_pred = itk.image_from_array(eso_pred)
save_pred.CopyInformation(image_pred_itk) # Important to save the image with correct spacing, size!!
itk.imwrite(save_pred, 'Esophagus_pred_sum.nii')

duree = time.time() - start_time
print ('\nTotal running time : %5.3g s' % duree)

