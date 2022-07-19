#!/usr/bin/env python
import os
import sys
import glob
import itk

def convert_all(dir_name, output_dir):
    # get all the secondary images
    Dimension = 2
    InputPixelType = itk.F
    OutputPixelType = itk.UC

    InputImageType = itk.Image[InputPixelType, Dimension]
    OutputImageType = itk.Image[OutputPixelType, Dimension]

    for inputImage in glob.glob(f'{dir_name}/*.mha'):
        outputImage = inputImage.replace('.mha', '.png')
        outputImage = outputImage.replace('./', f'{output_dir}')

        reader = itk.ImageFileReader[InputImageType].New()
        reader.SetFileName(inputImage)

        rescaler = itk.RescaleIntensityImageFilter[
            InputImageType,
            InputImageType].New()
        rescaler.SetInput(reader.GetOutput())
        rescaler.SetOutputMinimum(0)
        outputPixelTypeMaximum = itk.NumericTraits[OutputPixelType].max()
        rescaler.SetOutputMaximum(outputPixelTypeMaximum)

        castImageFilter = itk.CastImageFilter[InputImageType, OutputImageType].New()
        castImageFilter.SetInput(rescaler.GetOutput())

        writer = itk.ImageFileWriter[OutputImageType].New()
        writer.SetFileName(outputImage)
        writer.SetInput(castImageFilter.GetOutput())

        writer.Update()

    # convert to gif
    # convert_gif_command=f'convert -distort SRT 1.1,0 -resize 256x256 -delay 6 -loop 0 *.png image.gif '

if __name__ == "__main__":
    dir_name = sys.argv[1]
    output_dir = sys.argv[2]
    convert_all(dir_name, output_dir)

