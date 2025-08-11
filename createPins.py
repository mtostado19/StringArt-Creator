import math

class CreatePins():
    # SET PINS
    def setPins(self, nailCount, size):
        arrPins = []
        radius = size[0] // 2 - 10
        for i in range(nailCount):
            angle = (2 * math.pi * i) / nailCount
            x = size[0] // 2 + radius * math.cos(angle)
            y = size[1] // 2 + radius * math.sin(angle)
            arrPins.append((int(x),int(y)))
        return arrPins