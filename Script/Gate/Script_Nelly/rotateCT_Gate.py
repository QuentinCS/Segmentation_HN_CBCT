import numpy as np
import subprocess
import sys
import os

def invertTransfoMat(transfoMat):
    """Invert an affine transformation matrix.
    """
    transfoMatInv = np.zeros_like(transfoMat)
    A = transfoMat[:3, :3] # the rotation part in the affine matrix
    b = transfoMat[:3,3]  # the translation part in the affine matrix
    transfoMatInv[:3,:3] = A.T # A is a rotation matrix so its transpose is its inverse
    transfoMatInv[:3,3] = -A.T.dot(b)
    transfoMatInv[3,3] = 1.
    return transfoMatInv


def applyTransfo(CTPath,OutputPath,transfoPath):
    transfoCT = np.array([[0,1.,0,0], [1.,0,0,0], [0,0,1.,0], [0,0,0,1.]])
    invTransfoCT = invertTransfoMat(transfoCT)
    transfoCBCT = np.loadtxt(transfoPath)
    transfoCBCT[:-1, -1] *= 10 #convert from cm to mm
    transfoMatCT2RTK = transfoCBCT.dot(invTransfoCT)
    OutputDir = os.path.dirname(OutputPath)
    np.savetxt(f"{OutputDir}/matriceCT2RTK.mat", transfoMatCT2RTK)
    # save the inverse matrix to apply on the reconstructed image
    invTransfoCBCT = invertTransfoMat(transfoMatCT2RTK)
    np.savetxt(f"{OutputDir}/matriceRTK2CBCT.mat", invTransfoCBCT)
    bashCommand = f"clitkAffineTransform -i {CTPath} -o {OutputPath} -m {OutputDir}/matriceCT2RTK.mat --pad=-1024 --transform_grid"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()



if __name__ == "__main__":
    CTPath = sys.argv[1]
    OutputPath = sys.argv[2]
    transfoPath = sys.argv[3]
    #transfoCBCT = np.array([[0,0,1.,-2.13], [0,1.,0,12.13], [-1.,0,0,-8.8], [0,0,0,1.]])
    applyTransfo(CTPath,OutputPath,transfoPath)
