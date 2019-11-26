import numpy as np
from PIL import Image
import os

ppmPic = './myppm.ppm'
image_input = Image.open('./penguin.png')
image_input.save(ppmPic)

input_ppm = Image.open(ppmPic)

print(input_ppm)