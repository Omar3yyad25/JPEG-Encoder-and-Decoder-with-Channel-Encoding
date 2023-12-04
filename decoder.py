from encoder import zigzag_indices, Low_Compression_Quantizer, High_Compression_Quantizer, dct_basis
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def run_length_decoding(vector):
    decoded_vector = []
    j = 0
    while j < len(vector):
        if vector[j] == 0:
            for k in range(vector[j+1]):
                decoded_vector.append(0)
            j += 2 
        else:
            decoded_vector.append(vector[j])
            j += 1  
        
    return decoded_vector

def convert_1d_to_2d(vectors):
    zigzag = zigzag_indices()
    vectors_2d = []
    for i in range (len(vectors)):
        block = np.zeros((8, 8))
        for j in range (len(zigzag)):
            block[zigzag[j][0]][zigzag[j][1]] = vectors[i][j]
        vectors_2d.append(block)
    return vectors_2d

def Dequantization(blocks, QF):
    if QF == '1':
        for i in range (len(blocks)):
            blocks[i] = Low_Compression_Quantizer * blocks[i]
    elif QF == '2':
        for i in range (len(blocks)):
            blocks[i] = High_Compression_Quantizer * blocks[i]
    
    return blocks

def inverse_dct_2d(dequantized_block):
    idct_matrix = np.zeros((8, 8)) 
    for i in range (8):
        for j in range (8):
            basis_matrix = dct_basis(i,j)
            idct_matrix[i][j] = np.sum(np.multiply(dequantized_block, basis_matrix))

    return idct_matrix

def calculate_padding(image):
    height, width = image.shape
    padding_width = 0 if width % 8 == 0 else 8 - (width % 8)
    return padding_width

def reconstruct_image(decoded_blocks, image, padding):
    reconstructed_image = np.zeros((image.shape[0]+padding, image.shape[1]+padding))
    index = 0
    for i in range (0, image.shape[0], 8):
        for j in range (0, image.shape[1], 8):
            reconstructed_image[i:i+8, j:j+8] = decoded_blocks[index]
            index += 1
    squeezed_image = np.squeeze(reconstructed_image)

    # Saving the reconstructed image
    print("Image reconstructed successfully")
    plt.imshow(squeezed_image, cmap='gray')
    plt.show()

       