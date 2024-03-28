def change_bit_positions(array, bit_stream):
    result = ""
    for row in array:
        for position in row:
            result += bit_stream[position - 1]
    return result


# Example usage:
PC_1 = [
    [57, 49, 41, 33, 25, 17, 9],
    [1, 58, 50, 42, 34, 26, 18],
    [10, 2, 59, 51, 43, 35, 27],
    [19, 11, 3, 60, 52, 44, 36],
    [63, 55, 47, 39, 31, 23, 15],
    [7, 62, 54, 46, 38, 30, 22],
    [14, 6, 61, 53, 45, 37, 29],
    [21, 13, 5, 28, 20, 12, 4],
]


def print_with_spaces_8(result):
    formatted_result = " ".join([result[i : i + 8] for i in range(0, len(result), 8)])
    print("Result with spaces:", formatted_result)


def print_with_spaces_7(result):
    formatted_result = " ".join([result[i : i + 7] for i in range(0, len(result), 7)])
    print("Result with spaces:", formatted_result)


def print_with_spaces_6(result):
    formatted_result = " ".join([result[i : i + 6] for i in range(0, len(result), 6)])
    print(formatted_result)


K = "0001001100110100010101110111100110011011101111001101111111110001"
# print_with_spaces_8(bit_stream)
K_plus = change_bit_positions(PC_1, K)
# print_with_spaces_7(result)

# M = "0000000100100011010001010110011110001001101010111100110111101111"
PC_2 = [
    [14, 17, 11, 24, 1, 5],
    [3, 28, 15, 6, 21, 10],
    [23, 19, 12, 4, 26, 8],
    [16, 7, 27, 20, 13, 2],
    [41, 52, 31, 37, 47, 55],
    [30, 40, 51, 45, 33, 48],
    [44, 49, 39, 56, 34, 53],
    [46, 42, 50, 36, 29, 32],
]

Left_Shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def left_shift(bit_stream, shift):
    return bit_stream[shift:] + bit_stream[:shift]


Ci = K_plus[:28]
Di = K_plus[28:]
Ki = []

for i in range(16):
    Ci = left_shift(Ci, Left_Shifts[i])
    Di = left_shift(Di, Left_Shifts[i])
    CiDi = Ci + Di
    Ki.append(change_bit_positions(PC_2, CiDi))
    print_with_spaces_6(Ki[i])
    # print_with_spaces_7(Ci)
    # print_with_spaces_7(Di)
