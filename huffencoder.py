def huffman_encode(tobeencoded_data, root):
        f2 = {y: x for x, y in root.items()}
        encoded_data = ''
        current_code = ''

        for symbol in tobeencoded_data:
            current_code = f2[str(symbol)]
            encoded_data += current_code
                
        return encoded_data