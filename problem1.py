def read_text_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None


def write_text_to_file(file_path, text):
    try:
        with open(file_path, "w") as file:
            file.write(text)
    except Exception as e:
        print(f"Error writing to file '{file_path}': {e}")


def vigenere_cipher(text, key, mode="encode"):
    result = ""
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            key_char = key[i % key_length]
            shift = ord(key_char.lower()) - ord("a")

            if char.isupper():
                result += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            else:
                result += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
        else:
            result += char

    return result if mode == "encode" else vigenere_cipher(result, key, mode="decode")


def vigenere_decipher(text, key):
    text = reverse_format_output(text)
    result = ""
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            key_char = key[i % key_length]
            shift = ord(key_char.lower()) - ord("a")

            if char.isupper():
                result += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            else:
                result += chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
        else:
            result += char

    return result


def format_output(ciphertext):
    words = [ciphertext[i : i + 5] for i in range(0, len(ciphertext), 5)]
    return " ".join(words)


def reverse_format_output(formatted_text):
    return "".join(formatted_text.split())


def main():
    input_file_path = "input.txt"
    key_file_path = "key.txt"
    output_file_path = "output.txt"

    input_text = read_text_from_file(input_file_path)
    if not input_text:
        return

    key = read_text_from_file(key_file_path)
    if not key:
        return

    cleaned_text = "".join(char for char in input_text if char.isalpha())

    ciphertext = vigenere_cipher(cleaned_text, key)

    formatted_output = format_output(ciphertext)

    write_text_to_file(output_file_path, formatted_output)

    decoded_text = vigenere_decipher(formatted_output, key)
    # print("Decoded Message:", decoded_text)


if __name__ == "__main__":
    main()
