from BitVector import *

PASSPHRASE = "Hopes and dreams of a million years"
BLOCKSIZE = 16
HINT = "Douglas Adams"


def decrypt(text, key):
    numbytes = BLOCKSIZE // 8

    bv_iv = BitVector(bitlist=[0] * BLOCKSIZE)
    for i in range(0, len(PASSPHRASE) // numbytes):
        textstr = PASSPHRASE[i * numbytes : (i + 1) * numbytes]
        bv_iv ^= BitVector(textstring=textstr)

    encrypted_bv = BitVector(hexstring=text)

    key_bv = BitVector(intVal=key, size=BLOCKSIZE)

    msg_decrypted_bv = BitVector(size=0)

    previous_decrypted_block = bv_iv
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):
        bv = encrypted_bv[i * BLOCKSIZE : (i + 1) * BLOCKSIZE]
        temp = bv.deep_copy()
        bv ^= previous_decrypted_block
        previous_decrypted_block = temp
        bv ^= key_bv
        msg_decrypted_bv += bv

    outputtext = msg_decrypted_bv.get_text_from_bitvector()
    return outputtext


def brute_force_attack(ciphered_text):

    for key in range(29500, 2**BLOCKSIZE - 1):
        outputtext = decrypt(ciphered_text, key)
        if outputtext.find(HINT) != -1:
            return outputtext, key


if __name__ == "__main__":
    with open("ciphered_text.txt", "r") as inputfile, open(
        "deciphered_text.txt", "w"
    ) as outputfile, open("key.txt", "w") as keyfile:
        ciphered_text = inputfile.read()
        deciphered_text, key = brute_force_attack(ciphered_text)
        keyfile.write(str(key))
        outputfile.write(deciphered_text[:-1])
        print(key)
        print(deciphered_text)
