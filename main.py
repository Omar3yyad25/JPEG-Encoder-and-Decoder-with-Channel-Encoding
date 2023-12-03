from encoder import *
from decoder import *
from huffmanc import *
from huffmandecoder import huffman_decode
from huffencoder import huffman_encode
from itertools import chain

def main():
    image_path = 'image.jpeg'
    image = read_image(image_path)
    blocks = image_blocks(image)
    number_of_blocks = len(blocks)
    
    #Applying DCT to each block
    for i in range (len(blocks)):
        blocks[i] = dct_2d(blocks[i])

    #Quantization
    compression = input("Please enter 1 for low compression and 2 for high compression")
    blocks = Quantization(blocks, compression)
    
    #using zigzag indices to flatten each matrix into a vector and store all vectors in a list
    vectors = convert_2d_to_1d(blocks)
    print ("Vectors: ", vectors[1000])
    #Run length encoding
    encoded_vectors = run_length_encoding(vectors)
    #Huffman encoding
    f = Huffman(list(chain.from_iterable(encoded_vectors)))
    encoded_data = huffman_encode(list(chain.from_iterable(encoded_vectors)) , f.table)

    #Huffman decoding
    decoded_result = huffman_decode(encoded_data, f.table)
    #Run length decoding
    decoded_vector = run_length_decoding(decoded_result)

    #divide the decoded vector into 64 elements vectors
    decoded_vectors = []
    index = 0
    for i in range (number_of_blocks):
        decoded_vector_64 = []
        for j in range (64):
            decoded_vector_64.append(decoded_vector[index])
            index += 1
        decoded_vectors.append(decoded_vector_64)

    #convert each vector into a 8x8 matrix
    decoded_blocks = convert_1d_to_2d(decoded_vectors)

    #Dequantization
    decoded_blocks = Dequantization(decoded_blocks, compression)
    print ("Decoded blocks: ", decoded_blocks[1000])

if __name__ == '__main__':
    main()