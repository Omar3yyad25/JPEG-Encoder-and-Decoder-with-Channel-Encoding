def huffman_decode(encoded_data, root):
    decoded_data = []
    current_code = ''

    for bit in encoded_data:
        current_code += bit
        if current_code in root:
            n = current_code
            current_code = ''
            # make it integer to avoid problems in the next step
            decoded_data.append(int(root[n]))
            
    return decoded_data