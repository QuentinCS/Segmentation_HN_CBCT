import glob
import os
import sys
import get_atten_primary
import get_atten_scatter_all
import rescale_pixels
import resize_secondaries

def reconstruct(primaries_per_proj):
    for simulation in glob.glob('./Simulations/*'):
        # go to patient simulation folder and reconstruct
        current=os.getcwd()
        os.chdir(simulation)

        # resize the secondary images
        resize_secondaries.resize_all_local()

        # compute attenuation with scatter and reconstruct
        proj_path_withscatter='./withscatter'
        geometryfile='./data/elektaGeometry.xml'
        get_atten_scatter_all.attenuation_local(primaries_per_proj,proj_path_withscatter)
        reconstruct_steps(proj_path_withscatter)

        # compute attenuation without scatter and reconstruct
        proj_path_withoutscatter='./withoutscatter'
        geometryfile='./data/elektaGeometry.xml'
        get_atten_primary.attenuation_local(proj_path_withoutscatter)
        reconstruct_steps(proj_path_withoutscatter)

        os.chdir(current)


def reconstruct_steps(projections_path, geometryfile):
    reconstructed_img_path= f'{projections_path}/Reconstruction'
    if not os.path.exists(reconstructed_img_path):
        os.makedirs(reconstructed_img_path)

    # reconstruct image 
    fdkcommand = f'rtkfdk -p {projections_path} -r .*.mha --pad 1 -o {reconstructed_img_path}/fdk.mha -g {geometryfile} --dimension 410,264,410'
    os.system(fdkcommand)
    fovcommand = f'rtkfieldofview --geometry {geometryfile} -d -p {projections_path} -r .*.mha --reconstruction {reconstructed_img_path}/fdk.mha  --output {reconstructed_img_path}/fdk.mha --verbose'
    #--hardware=cuda
    os.system(fovcommand)
    # save the mask
    maskcommand = f'rtkfieldofview --geometry {geometryfile} -d -p {projections_path} -r .*.mha --reconstruction {reconstructed_img_path}/fdk.mha  --output {reconstructed_img_path}/mask.mha -m'
    os.system(maskcommand)

    # rotate reconstructed image and mask
    rotatecommand = f'clitkAffineTransform -i {reconstructed_img_path}/fdk.mha -o {reconstructed_img_path}/fdk_rotated.mha -m data/matriceRTK2CBCT.mat --pad=0 --transform_grid'
    os.system(rotatecommand)
    rotatemaskcommand = f'clitkAffineTransform -i {reconstructed_img_path}/mask.mha -o {reconstructed_img_path}/mask.mha -m data/matriceRTK2CBCT.mat --pad=0 --transform_grid'
    os.system(rotatemaskcommand)

    # rescale reconstructed image
    rescale_pixels.rescale(f'{reconstructed_img_path}/fdk_rotated.mha')


if __name__ == "__main__":
    prim_per_proj = int(sys.argv[1])
    reconstruct(prim_per_proj)

