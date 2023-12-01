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
            if block.shape != (8, 8):
                # If the block is not exactly 8x8, pad it with zeros
                padded_block = np.zeros((8, 8), dtype=block.dtype)
                padded_block[:block.shape[0], :block.shape[1]] = block
                block = padded_block
            blocks.append(block)
    return blocks


def zigzag_indices ():
    indices = [(i, j) for i in range(8) for j in range(8)]
    indices.sort(key=lambda x: (x[0]+x[1], x[1]) if (x[0]+x[1]) % 2 == 0 else (x[1]+x[0], x[0]))
    return indices

def dct_basis(u , v):
    basis_matrix = np.zeros((8, 8))
    for x in range(8):
        for y in range(8):
            basis_matrix[x][y]= np.cos(((2 * x + 1) * u * np.pi)/16) * np.cos(((2 * y + 1) * v * np.pi)/16)
    return basis_matrix


def dct_2d(block):
    dct_matrix = np.zeros((8, 8))
    for u in range(8):
        for v in range(8):
            basis_matrix = dct_basis(u, v)
            dct_matrix[u][v] = np.sum(np.multiply(block, basis_matrix))
    # divide each element by 16 and then divide first row by 2 and first column by 2
    dct_matrix = dct_matrix/16
    dct_matrix[0] = dct_matrix[0]/2
    dct_matrix[:, 0] = dct_matrix[:, 0]/2

    return dct_matrix

def main():
    image_path = 'image.jpeg'
    image = read_image(image_path)
    blocks = image_blocks(image)
    
    #Applying DCT to each block
    for i in range (len(blocks)):
        blocks[i] = dct_2d(blocks[i])

    #Quantization
    Low_Compression_Quantizer = np.array(
    [[1, 1, 1, 1, 1, 2, 2, 4],
      [1, 1, 1, 1, 1, 2, 2, 4],
      [1, 1, 1, 1, 2, 2, 2, 4],
      [1, 1, 1, 1, 2, 2, 4, 8],
      [1, 1, 2, 2, 2, 2, 4, 8],
      [2, 2, 2, 2, 2, 4, 8, 8],
      [2, 2, 2, 4, 4, 8, 8, 16],
      [4, 4, 4, 4, 8, 8, 16, 16]
    ])
    
    High_Compression_Quantizer= np.array([
    [1, 2, 4, 8, 16, 32, 64, 128],
    [2, 4, 4, 8, 16, 32, 64, 128],
    [4, 4, 8, 16, 32, 64, 128, 128],
    [8, 8, 16, 32, 64, 128, 128, 256],
    [16, 16, 32, 64, 128, 128, 256, 256],
    [32, 32, 64, 128, 128, 256, 256, 256],
    [64, 64, 128, 128, 256, 256, 256, 256],
    [128, 128, 128, 256, 256, 256,256,256]
    ])

    # Apply the Quantization step 
    # Divide each each block by the quantization matrix
    # Show to user which quantization matrix he wants to use
    # 1 for low compression and 2 for high compression
    print ("Please enter 1 for low compression and 2 for high compression")
    compression = input()
    if compression == '1':
        for i in range (len(blocks)):
            blocks[i] = np.divide(blocks[i], Low_Compression_Quantizer)
    elif compression == '2':
        for i in range (len(blocks)):
            blocks[i] = np.divide(blocks[i], High_Compression_Quantizer)
    else:
        print ("Wrong input")
        exit()
    
    #using zigzag indices to flatten each matrix into a vector and store all vectors in a list
    zigzag = zigzag_indices()
    vectors = []
    for i in range (len(blocks)):
        vector = []
        for j in range (len(zigzag)):
            vector.append(blocks[i][zigzag[j][0]][zigzag[j][1]])
        vectors.append(vector)


        

    
if __name__ == '__main__':
    main()