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

        test1 = []
        test2 = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if slope else (x, y)
            test1.append(coord[0])
            test2.append(coord[1])
            error -= dy
            if error < 0:
                y += ystep
                error += dx

        return np.array(test1), np.array(test2)
    
    def computeAllBresenhamLines(self, arrPins):
        for pin1 in arrPins:
            for pin2 in arrPins:
                if pin1 != pin2:
                    x, y = self.bresenham_line(pin1, pin2)
                    self.allBresenhamLines[pin1, pin2] = x, y
    
    def calculateScore(self, nail1, nail2, workingImg):

        x, y = self.allBresenhamLines[nail1, nail2]
        pixelsIndex = workingImg[y,x]
        darkness = 1.0 - pixelsIndex

        return darkness.mean()
    
    def updateImage(self, nail1, nail2, workingImg):
        x, y = self.allBresenhamLines[nail1, nail2]
        bright = 0.3
        workingImg[y,x] = np.minimum(1.0, workingImg[y,x] + bright)
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
        fig, ax = plt.subplots(figsize=(10,10))
        img_disp = ax.imshow(solutionBoard, cmap="gray", vmin=0, vmax=255)
        plt.draw()

        # Arr of instructions using pin index
        arrFinalInstructions = []

        for numLines in range(NUM_LINES):

            nextNail, bestPin = None, None
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
            draw.line([currentNail, nextNail], fill=50, width=config.THICKNESS)

            self.updateImage(currentNail, nextNail, workingImg)

            if numLines % 100 == 0 or numLines == NUM_LINES - 1:
                img_disp.set_data(solutionBoard)
                ax.set_xlabel("Lines: " + str(numLines + 1))
                plt.draw()
                plt.pause(0.001)
            currentNail = nextNail

        plt.ioff()
        return arrNails, arrFinalInstructions