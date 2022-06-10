import os
import sys
import rotateCT
import count_projections
import get_atten_scatter_primary
import get_atten_scatter_all
import rescale_pixels
import resize_secondaries

def steps(prim_per_proj):
    # rotate CT before simulation (get the CT size, spacing and origin position, and calculate the new origin in the z direction because the orientation flips)
    rotateCT.rotate('data/CT.mha')

    # change number of primaries in the macros according to projections
    count_projections.update_mac(prim_per_proj)

    # run the simulations
    gatecommand_primary = 'Gate mac/primary-patient.mac'
    os.system(gatecommand_primary)
    gatecommand_scatter = 'Gate mac/scatter-patient.mac'
    os.system(gatecommand_scatter)
    

    # resize the secondary images
    resize_secondaries.resize_all()

    # compute attenuation with scatter and reconstruct
    proj_path_withscatter='./withscatter'
    get_atten_scatter_all.attenuation(prim_per_proj,proj_path_withscatter)
    reconstruct_steps(proj_path_withscatter)

    # compute attenuation without scatter and reconstruct
    proj_path_withoutscatter='./withoutscatter'
    get_atten_scatter_primary.attenuation(prim_per_proj,proj_path_withoutscatter)
    reconstruct_steps(proj_path_withoutscatter)

def reconstruct_steps(projections_path):
    reconstructed_img_path= f'{projections_path}/reconstructed'
    if not os.path.exists(reconstructed_img_path):
        os.makedirs(reconstructed_img_path)

    # reconstruct image 
    fdkcommand = f'rtkfdk -p {projections_path} -r .*.mha --pad 1 -o {reconstructed_img_path}/fdk.mha -g data/elektaGeometry.xml --dimension=512'
    os.system(fdkcommand)
    fovcommand = f'rtkfieldofview --geometry data/elektaGeometry.xml -d -p {projections_path} -r .*.mha --reconstruction {reconstructed_img_path}/fdk.mha  --output {reconstructed_img_path}/fdk.mha --verbose'
    #--hardware=cuda
    os.system(fovcommand)

    # rotate reconstructed image
    rotatecommand = f'clitkAffineTransform -i {reconstructed_img_path}/fdk.mha -o {reconstructed_img_path}/fdk.mha -m data/rot_matrix -v'
    os.system(rotatecommand)

    # rescale reconstructed image
    rescale_pixels.rescale(f'{reconstructed_img_path}/fdk.mha')

if __name__ == "__main__":
    prim_per_proj = int(sys.argv[1])
    steps(prim_per_proj)



