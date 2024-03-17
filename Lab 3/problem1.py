# Given cipher texts
C1 = [0xE9, 0x3A, 0xE9, 0xC5, 0xFC, 0x73, 0x55, 0xD5]
C2 = [0xF4, 0x3A, 0xFE, 0xC7, 0xE1, 0x68, 0x4A, 0xDF]

length = len(C1)
# C1 xor C2
M = []
for i in range(length):
    M.append(C1[i] ^ C2[i])

# decrypt
with open("dict.txt", "r") as dictionary:
    words = dictionary.read().split()
    words = set([word for word in words if len(word) == length])
    for word1 in words:
        M1 = [ord(c) for c in word1]
        M2 = []
        for i in range(length):
            M2.append(M1[i] ^ M[i])
        word2 = "".join([chr(c) for c in M2])
        if word2 in words:
            print(word1, word2)
