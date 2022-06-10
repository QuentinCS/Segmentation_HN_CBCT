#!/usr/bin/env python
import itk
import sys

def rescale(filename):
    # read the image
    attenuation = itk.imread(filename)
    attenuation = itk.MultiplyImageFilter(attenuation,65536)
    itk.imwrite(attenuation, filename.replace(".mha", "_rescaled.mha"))

if __name__ == "__main__":
    filename = sys.argv[1]
    rescale(filename)

