from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path
from createPins import CreatePins
import config

file_path = Path("instructions.json")
if file_path.is_file():
    with open(file_path, "r") as f:
        data = json.load(f)
    pins = CreatePins().setPins(config.NUM_PINS, config.SIZE)
    board = Image.new('L', [config.WIDTH, config.HEIGHT], 255)
    coords = []
    for element in data["arr"]:
        coords.append(pins[element])
    npCoords = np.array(coords)
    x, y = npCoords[:,0], npCoords[:,1]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(board, cmap="gray", vmin=0, vmax=255)
    ax.plot(x,y, color="black", linewidth="0.4")
    plt.savefig("finalImage.png")
    plt.show()
else:
    print("File not found")