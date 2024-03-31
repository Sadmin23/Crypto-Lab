import Table


def map_bits(array, bit_stream):
    result = ""
    for row in array:
        for position in row:
            result += bit_stream[position - 1]
    return result


def hex_to_bits(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)


def bits_to_hex(bit_stream):
    return hex(int(bit_stream, 2))[2:].upper()


def string_to_bits(string):
    bit_string = "".join([bin(ord(char))[2:].zfill(8) for char in string])
    remainder = len(bit_string) % 64
    if remainder != 0:
        padding = "0" * (64 - remainder)
        bit_string += padding
    return bit_string


def string_to_hex(string):
    return bits_to_hex(string_to_bits(string))


def binary_to_string(binary_data):
    return "".join(
        chr(int(binary_data[i : i + 8], 2)) for i in range(0, len(binary_data), 8)
    ).rstrip("\x00")


Ki = []
Li = []
Ri = []


def left_shift(bit_stream, shift):
    return bit_stream[shift:] + bit_stream[:shift]


def precompute_key(K):
    K_plus = map_bits(Table.PC_1, K)

    Ci = K_plus[:28]
    Di = K_plus[28:]

    for i in range(16):
        Ci = left_shift(Ci, Table.Left_Shifts[i])
        Di = left_shift(Di, Table.Left_Shifts[i])
        CiDi = Ci + Di
        Ki.append(map_bits(Table.PC_2, CiDi))


def map_s_box(bit_stream):
    result = ""
    for i in range(8):
        row = int(bit_stream[i * 6] + bit_stream[i * 6 + 5], 2)
        col = int(bit_stream[i * 6 + 1 : i * 6 + 5], 2)
        result += bin(Table.S_Boxes[i][row][col])[2:].zfill(4)
    return result


def Mangler_function(Ri, Ki):
    T = map_bits(Table.E, Ri)
    T = int(T, 2) ^ int(Ki, 2)
    T = bin(T)[2:].zfill(48)
    T = map_s_box(T)
    return map_bits(Table.P, T)


def DES_encrypt(M, K):
    M_plus = map_bits(Table.IP, M)
    Li.append(M_plus[:32])
    Ri.append(M_plus[32:])
    precompute_key(K)
    for i in range(16):
        Li.append(Ri[i])
        f = Mangler_function(Ri[i], Ki[i])
        Ri.append(bin(int(Li[i], 2) ^ int(f, 2))[2:].zfill(32))
    R16L16 = Ri[16] + Li[16]
    C = map_bits(Table.inv_IP, R16L16)
    Li.clear()
    Ri.clear()
    return C


def DES_decrypt(C, K):
    C_plus = map_bits(Table.IP, C)
    Li.append(C_plus[:32])
    Ri.append(C_plus[32:])
    precompute_key(K)
    for i in range(16):
        Li.append(Ri[i])
        f = Mangler_function(Ri[i], Ki[15 - i])
        Ri.append(bin(int(Li[i], 2) ^ int(f, 2))[2:].zfill(32))
    R16L16 = Ri[16] + Li[16]
    M = map_bits(Table.inv_IP, R16L16)
    Li.clear()
    Ri.clear()
    return M


def split_into_blocks(bit_string, block_size):
    return [
        bit_string[i : i + block_size] for i in range(0, len(bit_string), block_size)
    ]


def ECB(blocks, key, mode="encrypt"):
    processed_blocks = []
    for block in blocks:
        if mode == "encrypt":
            processed_block = DES_encrypt(block, key)
        elif mode == "decrypt":
            processed_block = DES_decrypt(block, key)
        processed_blocks.append(processed_block)
    return processed_blocks


def concatenate_blocks(blocks):
    return "".join(blocks)


def Encrypt(message, key):
    bit_string = string_to_bits(message)
    blocks = split_into_blocks(bit_string, 64)
    encrypted_blocks = ECB(blocks, key, mode="encrypt")
    encrypted_string = concatenate_blocks(encrypted_blocks)
    return bits_to_hex(encrypted_string)


def Decrypt(ciphertext, key):
    bit_string = hex_to_bits(ciphertext)
    blocks = split_into_blocks(bit_string, 64)
    decrypted_blocks = ECB(blocks, key, mode="decrypt")
    decrypted_string = concatenate_blocks(decrypted_blocks)
    return decrypted_string


if __name__ == "__main__":
    Message = open("message.txt", "r").read()
    Key = open("key.txt", "r").read()
    Key = string_to_bits(Key)
    Ciphertext = Encrypt(Message, Key)
    print("Original Message:", Message)
    print("Encrypted Ciphertext:", Ciphertext)
    with open("encrypted.txt", "w") as encrypted_file:
        encrypted_file.write(Ciphertext)

    Decrypted_message = Decrypt(Ciphertext, Key)

    Decrypted_message = binary_to_string(Decrypted_message)
    print("Decrypted Message:", Decrypted_message)

    with open("decrypted.txt", "w") as decrypted_file:
        decrypted_file.write(Decrypted_message)
