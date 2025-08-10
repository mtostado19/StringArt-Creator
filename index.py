from PIL import Image, ImageOps, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math

# MAIN 
NUM_PINS = 200
NUM_LINES = 2000
THICKNESS = 1
WIDTH = 300
HEIGHT = 300
SIZE = (WIDTH, HEIGHT)


# GRAB IMAGE & CONVERT TO GRAYSCALE
img = Image.open('images/imgTest1.png').convert('L')
img2 = img.resize(SIZE, Image.LANCZOS)
imgArr = np.asarray(img2).astype(np.int16)


# SET PINS
def setPins(nailCount, size):
    arrPins = []
    radius = size[0] // 2 - 10
    # print(radius)
    for i in range(nailCount):
        angle = (2 * math.pi * i) / nailCount
        x = size[0] // 2 + radius * math.cos(angle)
        y = size[1] // 2 + radius * math.sin(angle)
        arrPins.append((int(x),int(y)))
    return arrPins

arrPins = setPins(NUM_PINS, SIZE)
# print(arrPins)

# GREEDY ALGORITHM
def exploreAllPaths(arrPins, originalImg, NUM_LINES):

    currentNail = arrPins[0]
    arrNails = [currentNail]
    solutionBoard = Image.new('L', [WIDTH, HEIGHT], 255)
    draw = ImageDraw.Draw(solutionBoard)
    visited_lines = set()

    for _ in range(NUM_LINES):
        nextNail = None
        highestContrast = -1

        # Find the best solution
        for nail in arrPins:
            if nail == currentNail:
                continue

            if len(arrNails) > 1 and nail == arrNails[-2]:
                continue

            line_key = tuple(sorted([currentNail, nail]))
            if line_key in visited_lines:
                continue


            steps = 100
            totalContrast = 0
            for i in range(steps):
                x = int(math.floor(currentNail[0] + (nail[0] - currentNail[0]) * (i/steps)))
                y = int(math.floor(currentNail[1] + (nail[1] - currentNail[1]) * (i/steps)))

                if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
                    brightness = int(originalImg[y, x])
                    totalContrast += (255 - brightness)

            contrast = totalContrast / steps

            if contrast > highestContrast:
                highestContrast = contrast
                nextNail = nail
            #Get the contrast


        if nextNail == None:
            break

        arrNails.append(nextNail)
        #Draw the next nail
        draw.line([currentNail, nextNail], fill="black", width=THICKNESS)
        visited_lines.add(tuple(sorted([currentNail, nextNail])))
        updateImage(currentNail, nextNail, originalImg, steps)
        currentNail = nextNail

    return arrNails, solutionBoard

def updateImage(nail1, nail2, originalImg, steps):
    for i in range(steps):
        x = int(math.floor(nail1[0] + (nail2[0] - nail1[0]) * (i/steps)))
        y = int(math.floor(nail1[1] + (nail2[1] - nail1[1]) * (i/steps)))
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            originalImg[y, x] = max(0, originalImg[y, x] - 10)
    return originalImg


arrNails, solutionBoard = exploreAllPaths(arrPins, imgArr, NUM_LINES)
print(arrNails)

# Show circumference
for items in arrPins:
    plt.scatter(items[0], items[1], marker="o", s=THICKNESS)

#TEST LINES
# x= [arrPins[0][0], arrPins[50][0]]
# y = [arrPins[0][1], arrPins[50][1]]

# img3 = img2.copy()
# draw = ImageDraw.Draw(img3)
# draw.line([(0, 0), (250,10)], fill="black", width=THICKNESS)
# diff = imgArr - np.array(img3)
# print(np.sum(diff))
# imgArr = np.asarray(img2)

# plt.plot(x,y, color='black')
test = np.asarray(solutionBoard)

imgplot = plt.imshow(solutionBoard, cmap="gray")

plt.colorbar()
plt.show()

# testImg.show()