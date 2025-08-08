from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math

# MAIN 
NUM_PINS = 300
NUM_LINES = 6000
THICKNESS = 1
WIDTH = 300
HEIGHT = 300
SIZE = (WIDTH, HEIGHT)


# GRAB IMAGE & CONVERT TO GRAYSCALE
# img = np.asarray(Image.open('images/imgTest1.png'))
img = Image.open('images/imgTest1.png').convert('L')
img2 = np.asarray(img.resize(SIZE, Image.LANCZOS))
# lum_img = img2[:, :, 0]
imgplot = plt.imshow(img2, cmap="gray")


# SET PINS
def setPins(nailCount, size):
    arrPins = []
    center = (size[0] // 2, size[1] // 2)
    radius = size[0] // 2 - 50
    print(center)
    print(radius)
    for i in range(nailCount):
        angle = (2 * math.pi * i) / nailCount
        x = size[0] // 2 + radius * math.cos(angle)
        y = size[1] // 2 + radius * math.sin(angle)
        arrPins.append((x,y))
    return arrPins

arrPins = setPins(NUM_PINS, SIZE)
print(arrPins)
# GREEDY ALGORITHM


# Show
# plt.colorbar()
# plt.show()