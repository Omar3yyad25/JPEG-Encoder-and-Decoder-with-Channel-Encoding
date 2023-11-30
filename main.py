import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def read_image(file_path):
    img = Image.open(file_path).convert('L')
    # plt.imshow(img, cmap='gray')
    # plt.axis('off')  
    # plt.show()
    return np.array(img)


def image_blocks(image):
    height, width = image.shape
    blocks = []
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = image[i:i+8, j:j+8]
            blocks.append(block)
    return blocks

def zigzag_indices ():
    indices = [(i, j) for i in range(8) for j in range(8)]
    indices.sort(key=lambda x: (x[0]+x[1], x[1]) if (x[0]+x[1]) % 2 == 0 else (x[1]+x[0], x[0]))
    return indices

image_path = 'image.jpeg'
image = read_image(image_path)
blocks = image_blocks(image)


print (zigzag_indices())
