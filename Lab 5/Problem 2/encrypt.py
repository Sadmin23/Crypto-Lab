from PIL import Image
import DES

image = Image.open("TUX.ppm")
image_data = image.tobytes()

block_size = 8
if len(image_data) % block_size != 0:
    image_data += b" " * (block_size - len(image_data) % block_size)

image_data = DES.bytes_to_bits(image_data)

Key = open("key.txt", "r").read()
Key = DES.string_to_bits(Key)
Ciphertext = DES.Encrypt(image_data, Key)

encrypted_image = Image.frombytes(image.mode, image.size, Ciphertext)
encrypted_image.save("TUX_encrypted.ppm")
