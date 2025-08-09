from PIL import Image, ImageOps, ImageDraw
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
img2 = img.resize(SIZE, Image.LANCZOS)

imgArr = np.asarray(img2)

# imgplot = plt.imshow(img2, cmap="gray")


# SET PINS
def setPins(nailCount, size):
    arrPins = []
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
# print(arrPins)

# GREEDY ALGORITHM
def exploreAllPaths(arrPins, originalImg, NUM_PINS, NUM_LINES):
    currentPin = (arrPins[0][0], arrPins[0][1])
    currentBest = -9999
    for i in range(200):
        for x, y in arrPins:
            if currentPin == (x, y):
                continue

            # Determine best next pin
            tempImg = originalImg.copy()
            draw = ImageDraw.Draw(tempImg)
            draw.line([(currentPin[0], currentPin[1]), (x, y)], fill='black', width=THICKNESS)
            result = np.asarray(originalImg) - np.array(tempImg)
            result = np.sum(result)
            if result > currentBest:
                currentBest = result
                nextPin = (x, y)
        print("current", currentPin)
        print("next", nextPin)
        draw = ImageDraw.Draw(originalImg)
        draw.line([(currentPin[0], currentPin[1]), (x, y)], fill='black', width=THICKNESS)
        currentPin = nextPin
    return

exploreAllPaths(arrPins, img2, NUM_PINS, NUM_LINES)

# Show
for items in arrPins:
    plt.scatter(items[0], items[1], marker="o", s=THICKNESS)

#TEST LINES
x= [arrPins[0][0], arrPins[50][0]]
y = [arrPins[0][1], arrPins[50][1]]

img3 = img2.copy()
draw = ImageDraw.Draw(img3)
draw.line([(0, 0), (250,10)], fill="black", width=THICKNESS)
diff = imgArr - np.array(img3)
print(np.sum(diff))
imgArr = np.asarray(img2)

# plt.plot(x,y, color='black')
imgplot = plt.imshow(imgArr, cmap="gray")

plt.colorbar()
plt.show()