import itk
import sys
import os
#import pathlib

def rotate(filename,output_filename):

    CT_img = itk.imread(filename)
    #newfilename=filename.replace(pathlib.Path(filename).suffix,'_rotated' + pathlib.Path(filename).suffix)
    size=itk.size(CT_img)
    spacing=CT_img.GetSpacing()
    origin=CT_img.GetOrigin()

    newsize=str(size[0]) + "," + str(size[2]) + "," + str(size[1])
    newspacing=str(spacing[0]) + "," + str(spacing[2]) + "," + str(spacing[1])
    neworigin_z = -(size[1] * spacing[1] + origin[1])
    neworigin=str(origin[0]) + "," + str(origin[2]) + "," + str(neworigin_z)

    command = f"clitkAffineTransform -i {filename} -o {output_filename} -m data/CT_rotmatrix -v --size={newsize} --spacing={newspacing}  --origin={neworigin} "
    os.system(command)


if __name__ == "__main__":
    filename = sys.argv[1]
    output_filename = sys.argv[2]
    rotate(filename,output_filename)
