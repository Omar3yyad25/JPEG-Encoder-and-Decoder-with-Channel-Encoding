def run_length_decoding(vectors):
    decoded_vectors = []
    for i in range(len(vectors)):
        decoded_vector = []
        j = 0
        while j < len(vectors[i]):
            if vectors[i][j] == 0:
                for k in range(vectors[i][j+1]):
                    decoded_vector.append(0)
                j += 2 
            else:
                decoded_vector.append(vectors[i][j])
                j += 1  
        decoded_vectors.append(decoded_vector)
    return decoded_vectors