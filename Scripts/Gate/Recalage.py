import itk
from itk import *

parameter_object = itk.ParameterObject.New()
parameter_object.AddParameterFile('parameters.txt')

cbct_fixed = itk.imread("../../cbct_images/1.2.840.113854.261407832220960147202645796066740913654.1/cbct.0.nii", itk.F)
cbct_moving = itk.imread("reconstruct/fdk_rotated.mha", itk.F)

result_image, result_transform_parameters_mask = itk.elastix_registration_method(cbct_fixed, #fixed
          cbct_moving, #moving
          parameter_object=parameter_object,
          output_directory='output/',
          log_to_console=True)

itk.imwrite(result_image, "result_registration.mhd")
print(result_transform_parameters_mask)

