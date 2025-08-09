from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math

# MAIN 
NUM_PINS = 150
NUM_LINES = 6000
THICKNESS = 1
WIDTH = 300
HEIGHT = 300
SIZE = (WIDTH, HEIGHT)


# GRAB IMAGE & CONVERT TO GRAYSCALE
img = Image.open('images/imgTest1.png').convert('L')
img2 = np.asarray(img.resize(SIZE, Image.LANCZOS))

# imgplot = plt.imshow(img2, cmap="gray")


# SET PINS
def setPins(nailCount, size):
    arrPins = []
    center = (size[0] // 2, size[1] // 2)
    radius = size[0] // 2 - 10
    # print(center)
    # print(radius)
    for i in range(nailCount):
        angle = (2 * math.pi * i) / nailCount
        x = size[0] // 2 + radius * math.cos(angle)
        y = size[1] // 2 + radius * math.sin(angle)
        arrPins.append((x,y))
    return arrPins

arrPins = setPins(NUM_PINS, SIZE)
print(arrPins)

# GREEDY ALGORITHM
def exploreAllPaths():
    return

exploreAllPaths()

# Show
for items in arrPins:
    plt.scatter(items[0], items[1], marker="o", s=THICKNESS)

#TEST LINES
x= [arrPins[0][0], arrPins[50][0]]
y = [arrPins[0][1], arrPins[50][1]]

plt.plot(x,y, color='black')
imgplot = plt.imshow(img2, cmap="gray")

plt.colorbar()
plt.show()