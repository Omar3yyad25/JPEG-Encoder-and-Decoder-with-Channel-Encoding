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
    compression = input("Please enter 1 for low compression and 2 for high compression")
    if compression == '1':
        for i in range (len(blocks)):
            blocks[i] = np.round(blocks[i]/ Low_Compression_Quantizer)
    elif compression == '2':
        for i in range (len(blocks)):
            blocks[i] = np.round(blocks[i]/ High_Compression_Quantizer)
    else:
        print ("Wrong input")
        exit()
    
    #using zigzag indices to flatten each matrix into a vector and store all vectors in a list
    vectors = convert_2d_to_1d(blocks)
    #Run length encoding
    encoded_vectors = run_length_encoding(vectors)
    f = Huffman(list(chain.from_iterable(encoded_vectors)))

    encoded_data = huffman_encode(list(chain.from_iterable(encoded_vectors)) , f.table)
    decoded_result = huffman_decode(encoded_data, f.table)
    print(decoded_result)

                
if __name__ == '__main__':
    main()