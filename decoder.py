from encoder import zigzag_indices, Low_Compression_Quantizer, High_Compression_Quantizer
import numpy as np

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




       