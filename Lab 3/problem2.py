import json


def encode(m, p, prev_c):
    return m ^ (p + prev_c) % 256


def encrypt(word, P, prev_c=0):
    W = [ord(c) for c in word]
    C = []
    for i in range(len(P)):
        Ci = encode(W[i], P[i], prev_c)
        C.append(Ci)
        prev_c = Ci
    return C


def decrypt(C, P, prev_c=0):
    W = []
    for i in range(len(P)):
        Wi = encode(C[i], P[i], prev_c)
        prev_c = C[i]
        W.append(Wi)
    word = "".join([chr(c) for c in W])
    return word


def task1():
    PAD = [12, 15, 1, 123, 55, 33, 90, 190, 72, 29]
    c = encrypt("HelloWorld", PAD)
    print("cipher: ", c)
    word = decrypt(c, PAD)
    print("message: ", word)


ciphertexts = []
msg_count = 10
msg_len = 60
pads = []
words = []
w_interval = 15


def recursively_expand_pad(cur_pad, cur_index, words, end_index):
    if cur_index == end_index:
        texts = [(decrypt(ciph[:end_index], cur_pad)) for ciph in ciphertexts]
        text_to_score = "\n".join(texts).lower()
        score = sum(len(word) ** 2 for word in words if word in text_to_score)
        return (score, texts, cur_pad)
    else:
        best_score = 0
        best_texts = None
        best_pad = None
        for p in pads[cur_index]:
            score, texts, pad = recursively_expand_pad(
                cur_pad + [p], cur_index + 1, words, end_index
            )
            if best_score < score:
                best_score = score
                best_texts = texts
                best_pad = pad
        return (best_score, best_texts, best_pad)


def task2():
    global words, ciphertexts, pads, msg_count, msg_len

    valid_chars = (
        list(range(65, 91)) + list(range(97, 123)) + [32, 44, 46, 63, 33, 45, 40, 41]
    )

    with open("dict.txt", "r") as dictionary:
        words = dictionary.read().lower().split()

    with open("ciphertext.txt", "r") as ciphertextfile:
        for i in range(10):
            ciphertexts.append(json.loads(ciphertextfile.readline()))

    for j in range(msg_len):
        possible_pad = []
        for i in range(256):
            valid = 1
            for k in range(msg_count):
                prev_c = ciphertexts[k][j - 1] if j > 0 else 0
                m = encode(ciphertexts[k][j], i, prev_c)
                if not (valid_chars.__contains__(m)):
                    valid = 0
                    break
            if valid == 1:
                possible_pad.append(i)
        pads.append(possible_pad)
    pad_lens = list(len(p) for p in pads)
    print("possible pad counts: ", pad_lens)
    print("\n")

    ranges = [(0, 4), (4, 15), (15, 23), (23, 35), (35, 43), (43, 60)]

    final_pads = []
    final_texts = []

    for start, end in ranges:
        best_score, best_texts, best_pad = recursively_expand_pad([], 0, words, end)
        print(f"Best Texts for next {end - start} pads:", best_texts)
        print("\n")

        for i in range(end - start):
            pads[start + i] = [best_pad[start + i]]

        if end == 60:
            final_pads = best_pad
            final_texts = "\n".join(best_texts)
        

    print("Hacked Pad:", final_pads)
    print("\nHacked Messages:\n", final_texts)


if __name__ == "__main__":
    task2()
