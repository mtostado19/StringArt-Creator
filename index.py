from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import math
import json
from pathlib import Path

# MAIN 
NUM_PINS = 300
NUM_LINES = 50
THICKNESS = 1
WIDTH = 800
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)


# GRAB IMAGE & CONVERT TO GRAYSCALE
img = Image.open('images/test4.png').convert('L')
img2 = img.resize(SIZE, Image.LANCZOS)
# NORMALIZE ARRAY (0, 1)
imgArr = np.asarray(img2, dtype=np.float32) / 255

# SET PINS
def setPins(nailCount, size):
    arrPins = []
    radius = size[0] // 2 - 10
    for i in range(nailCount):
        angle = (2 * math.pi * i) / nailCount
        x = size[0] // 2 + radius * math.cos(angle)
        y = size[1] // 2 + radius * math.sin(angle)
        arrPins.append((int(x),int(y)))
    return arrPins

arrPins = setPins(NUM_PINS, SIZE)
# print(arrPins)

def bresenham_line(nail1, nail2):

    x1, y1 = nail1
    x2, y2 = nail2
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    slope = dy > dx

    if slope:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    error = dx // 2
    y = y1
    ystep = 1 if y1 < y2 else -1

    pixels = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if slope else (x, y)
        pixels.append(coord)
        error -= dy
        if error < 0:
            y += ystep
            error += dx

    return pixels

def calculateScore(nail1, nail2, workingImg):

    pixels = bresenham_line(nail1, nail2)

    if not pixels:
        return 0.0

    totalContrast = 0
    for x, y in pixels:
        pixelIndex = workingImg[y, x]
        darkness = 1.0 - pixelIndex
        totalContrast += darkness

    return totalContrast / len(pixels)

def updateImage(nail1, nail2, workingImg):
    pixels = bresenham_line(nail1, nail2)
    bright = 0.5
    for x, y in pixels:
        pixelIndex = workingImg[y,x]
        newVal = min(1.0, pixelIndex + bright)
        workingImg[y,x] = newVal
    return workingImg

# GREEDY ALGORITHM
def exploreAllPaths(arrPins, originalImg, NUM_LINES):

    currentNail = arrPins[0]
    arrNails = [currentNail]
    solutionBoard = Image.new('L', [WIDTH, HEIGHT], 255)
    draw = ImageDraw.Draw(solutionBoard)
    workingImg = originalImg.copy()

    # Simulation
    plt.ion()
    fig, ax = plt.subplots()
    img_disp = ax.imshow(solutionBoard, cmap="gray", vmin=0, vmax=255)
    plt.draw()

    # Arr of instructions using pin index
    arrFinalInstructions = []
    bestPin = None

    for numLines in range(NUM_LINES):

        nextNail = None
        highestContrast = -1

        # Find the best solution
        for i, nail in enumerate(arrPins):
            if nail == currentNail:
                continue

            contrast = calculateScore(currentNail, nail, workingImg)

            if contrast > highestContrast:
                highestContrast = contrast
                nextNail = nail
                bestPin = i

        if nextNail == None:
            break

        arrNails.append(nextNail)
        arrFinalInstructions.append(bestPin)
        #Draw the next nail
        draw.line([currentNail, nextNail], fill=0, width=THICKNESS)

        updateImage(currentNail, nextNail, workingImg)

        img_disp.set_data(solutionBoard)
        ax.set_xlabel("Lines: " + str(numLines + 1))
        plt.draw()
        plt.pause(0.001)
        currentNail = nextNail

    plt.ioff()
    return arrNails, solutionBoard, workingImg, arrFinalInstructions

arrNails, solutionBoard, workingImg, instructions = exploreAllPaths(arrPins, imgArr, NUM_LINES)

# print(instructions)
file_path = Path("instructions.json")
# text = { "name": "Amy"}

if file_path.is_file():
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({ "arr": instructions }, f)
else:
    print("File not found")

plt.ioff()
plt.show()