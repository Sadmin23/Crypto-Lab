import box


def change_bit_positions(array, bit_stream):
    result = ""
    for row in array:
        for position in row:
            result += bit_stream[position - 1]
    return result


def print_with_spaces_8(result):
    formatted_result = " ".join([result[i : i + 8] for i in range(0, len(result), 8)])
    print(formatted_result)


def print_with_spaces_7(result):
    formatted_result = " ".join([result[i : i + 7] for i in range(0, len(result), 7)])
    print(formatted_result)


def print_with_spaces_6(result):
    formatted_result = " ".join([result[i : i + 6] for i in range(0, len(result), 6)])
    print(formatted_result)


def print_with_spaces_4(result):
    formatted_result = " ".join([result[i : i + 4] for i in range(0, len(result), 4)])
    print(formatted_result)


def hex_to_bits(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)


def bits_to_hex(bit_stream):
    return hex(int(bit_stream, 2))[2:].upper()


def string_to_bits(string):
    return "".join([bin(ord(char))[2:].zfill(8) for char in string])


def string_to_hex(string):
    return bits_to_hex(string_to_bits(string))


print(string_to_hex("Your lips are smoother than vaseline"))

K = "0001001100110100010101110111100110011011101111001101111111110001"
M = "0000000100100011010001010110011110001001101010111100110111101111"

# K = "0E329232EA6D0D73"
# M = "8787878787878787"
# K = hex_to_bits(K)
# M = hex_to_bits(M)

K_plus = change_bit_positions(box.PC_1, K)


def left_shift(bit_stream, shift):
    return bit_stream[shift:] + bit_stream[:shift]


Ci = K_plus[:28]
Di = K_plus[28:]
Ki = []

for i in range(16):
    Ci = left_shift(Ci, box.Left_Shifts[i])
    Di = left_shift(Di, box.Left_Shifts[i])
    CiDi = Ci + Di
    Ki.append(change_bit_positions(box.PC_2, CiDi))
    # print_with_spaces_6(Ki[i])


M_plus = change_bit_positions(box.IP, M)

Li = []
Ri = []

Li.append(M_plus[:32])
Ri.append(M_plus[32:])


def map_s_box(bit_stream):
    result = ""
    for i in range(8):
        row = int(bit_stream[i * 6] + bit_stream[i * 6 + 5], 2)
        col = int(bit_stream[i * 6 + 1 : i * 6 + 5], 2)
        result += bin(box.S_Boxes[i][row][col])[2:].zfill(4)
    return result


def function(Ri, Ki):
    T = change_bit_positions(box.E, Ri)
    T = int(T, 2) ^ int(Ki, 2)
    T = bin(T)[2:].zfill(48)
    T = map_s_box(T)
    return change_bit_positions(box.P, T)


for i in range(16):
    Li.append(Ri[i])
    f = function(Ri[i], Ki[i])
    Ri.append(bin(int(Li[i], 2) ^ int(f, 2))[2:].zfill(32))


R16L16 = Ri[16] + Li[16]
C = change_bit_positions(box.inv_IP, R16L16)
# print(bits_to_hex(C))
