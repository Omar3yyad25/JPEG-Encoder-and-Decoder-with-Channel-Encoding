import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct
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

def built_in_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def dct_2d(block):
    dct_block = np.zeros((8, 8))
    for u in range(8):
        for v in range(8):
            sum = 0
            for x in range(8):
                for y in range(8):
                    if x == 0 and y == 0:
                        sum += block[x][y] * np.cos(((2 * x + 1) * u * np.pi) / 64) * np.cos(((2 * y + 1) * v * np.pi) / 64)
                    elif x == 0 or y == 0:
                        sum += block[x][y] * np.cos(((2 * x + 1) * u * np.pi) / 32) * np.cos(((2 * y + 1) * v * np.pi) / 32)
                    else:
                        sum += block[x][y] * np.cos(((2 * x + 1) * u * np.pi) / 16) * np.cos(((2 * y + 1) * v * np.pi) / 16)
            dct_block[u][v] = sum
    return dct_block

image_path = 'image.jpeg'
image = read_image(image_path)
blocks = image_blocks(image)

blocks[200] = built_in_dct(blocks[700])

plt.imshow(blocks[700], cmap='gray')
plt.axis('off')  
plt.show()