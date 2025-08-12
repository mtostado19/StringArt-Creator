from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import math
import config

class Solution():

    allBresenhamLines = {}
    def bresenham_line(self, nail1, nail2):

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
    
    def computeAllBresenhamLines(self, arrPins):
        for pin1 in arrPins:
            for pin2 in arrPins:
                if pin1 != pin2:
                    pixels = self.bresenham_line(pin1, pin2)
                    self.allBresenhamLines[pin1, pin2] = pixels
    
    def calculateScore(self, nail1, nail2, workingImg):

        pixels = self.allBresenhamLines[nail1, nail2]

        if not pixels:
            return 0.0

        totalContrast = 0
        for x, y in pixels:
            pixelIndex = workingImg[y, x]
            darkness = 1.0 - pixelIndex
            totalContrast += darkness

        return totalContrast / len(pixels)
    
    def updateImage(self, nail1, nail2, workingImg):
        pixels = self.allBresenhamLines[nail1, nail2]
        bright = 0.5
        for x, y in pixels:
            pixelIndex = workingImg[y,x]
            newVal = min(1.0, pixelIndex + bright)
            workingImg[y,x] = newVal
        return workingImg
    
    # GREEDY ALGORITHM
    def exploreAllPaths(self, arrPins, originalImg, NUM_LINES):

        self.computeAllBresenhamLines(arrPins)

        currentNail = arrPins[0]
        arrNails = [currentNail]
        solutionBoard = Image.new('L', [config.WIDTH, config.HEIGHT], 255)
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

                contrast = self.calculateScore(currentNail, nail, workingImg)

                if contrast > highestContrast:
                    highestContrast = contrast
                    nextNail = nail
                    bestPin = i

            if nextNail == None:
                break

            arrNails.append(nextNail)
            arrFinalInstructions.append(bestPin)
            #Draw the next nail
            draw.line([currentNail, nextNail], fill=0, width=config.THICKNESS)

            self.updateImage(currentNail, nextNail, workingImg)

            img_disp.set_data(solutionBoard)
            ax.set_xlabel("Lines: " + str(numLines + 1))
            plt.draw()
            plt.pause(0.001)
            currentNail = nextNail

        plt.ioff()
        return arrNails, arrFinalInstructions