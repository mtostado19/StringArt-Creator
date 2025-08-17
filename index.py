from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import json
import config
import traceback
from pathlib import Path
from createPins import CreatePins
from exploreSolution import Solution


def main():

    try:
        # GRAB IMAGE & CONVERT TO GRAYSCALE
        img = Image.open('images/test4.png').convert('L')
        img2 = img.resize(config.SIZE, Image.LANCZOS)
        # NORMALIZE ARRAY (0, 1)
        imgArr = np.asarray(img2, dtype=np.float32) / 255

        arrPins = CreatePins().setPins(config.NUM_PINS, config.SIZE)
        # print(arrPins)
        arrNails, instructions = Solution().exploreAllPaths(arrPins, imgArr, config.NUM_LINES)
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
    except Exception as e:
        print("Error, oh well")
        print(e)
        traceback.print_exc()

if __name__ == '__main__':
    main()