import Table
from PIL import Image


def permutation(array, bit_stream):
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


def bytes_to_bits(byte_stream):
    return "".join([bin(byte)[2:].zfill(8) for byte in byte_stream])


def bits_to_bytes(bit_stream):
    return bytes([int(bit_stream[i : i + 8], 2) for i in range(0, len(bit_stream), 8)])


Ki = []
Li = []
Ri = []


def left_shift(bit_stream, shift):
    return bit_stream[shift:] + bit_stream[:shift]


def precompute_key(K):
    K_plus = permutation(Table.PC_1, K)

    Ci = K_plus[:28]
    Di = K_plus[28:]

    for i in range(16):
        Ci = left_shift(Ci, Table.Left_Shifts[i])
        Di = left_shift(Di, Table.Left_Shifts[i])
        CiDi = Ci + Di
        Ki.append(permutation(Table.PC_2, CiDi))


def map_s_box(bit_stream):
    result = ""
    for i in range(8):
        row = int(bit_stream[i * 6] + bit_stream[i * 6 + 5], 2)
        col = int(bit_stream[i * 6 + 1 : i * 6 + 5], 2)
        result += bin(Table.S_Boxes[i][row][col])[2:].zfill(4)
    return result


def function(Ri, Ki):
    T = permutation(Table.E, Ri)
    T = int(T, 2) ^ int(Ki, 2)
    T = bin(T)[2:].zfill(48)
    T = map_s_box(T)
    return permutation(Table.P, T)


def DES(M, K):
    M_plus = permutation(Table.IP, M)
    Li.append(M_plus[:32])
    Ri.append(M_plus[32:])
    precompute_key(K)
    for i in range(16):
        Li.append(Ri[i])
        f = function(Ri[i], Ki[i])
        Ri.append(bin(int(Li[i], 2) ^ int(f, 2))[2:].zfill(32))
    R16L16 = Ri[16] + Li[16]
    C = permutation(Table.inv_IP, R16L16)
    Li.clear()
    Ri.clear()
    return C


def split_into_blocks(bit_string, block_size):
    return [
        bit_string[i : i + block_size] for i in range(0, len(bit_string), block_size)
    ]


def ECB(blocks, key):
    encrypted_blocks = []
    for block in blocks:
        encrypted_block = DES(block, key)
        encrypted_blocks.append(encrypted_block)
    return encrypted_blocks


def concatenate_blocks(blocks):
    return "".join(blocks)


def Encrypt(message, key):
    blocks = split_into_blocks(message, 64)
    encrypted_blocks = ECB(blocks, key)
    encrypted_string = concatenate_blocks(encrypted_blocks)
    return bits_to_bytes(encrypted_string)


if __name__ == "__main__":
    image = Image.open("image.ppm")
    image_data = image.tobytes()

    block_size = 8
    if len(image_data) % block_size != 0:
        image_data += b" " * (block_size - len(image_data) % block_size)

    image_data = bytes_to_bits(image_data)
    Key = open("key.txt", "r").read()
    Key = string_to_bits(Key)
    encrypted_image_data = Encrypt(image_data, Key)

    encrypted_image = Image.frombytes(image.mode, image.size, encrypted_image_data)
    encrypted_image.save("image_enc.ppm")
