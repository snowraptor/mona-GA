#!/usr/bin/python2

from sys import argv
import cairo
from numpy import *
import time

with open(argv[1], 'r') as png1:
    surf1 = cairo.ImageSurface.create_from_png(png1)

with open(argv[2], 'r') as png2:
    surf2 = cairo.ImageSurface.create_from_png(png2)

data1 = surf1.get_data()
data2 = surf2.get_data()

pixels1 = map(ord, data1)
pixels2 = map(ord, data2)

delta = array(pixels2) - pixels1
rms = sqrt(average(delta * delta))

print(delta)
print(surf1.get_format(), cairo.FORMAT_ARGB32, cairo.FORMAT_RGB24)

print(rms)



