def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def write_text_to_file(file_path, text):
    try:
        with open(file_path, 'w') as file:
            file.write(text)
    except Exception as e:
        print(f"Error writing to file '{file_path}': {e}")

def vigenere_cipher(text, key):
    result = ''
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            key_char = key[i % key_length]
            shift = ord(key_char.lower()) - ord('a')

            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char

    return result

def main():
    input_file_path = 'input.txt'
    key_file_path = 'key.txt'
    output_file_path = 'output.txt'

    # Read input text from 'input.txt'
    input_text = read_text_from_file(input_file_path)
    if not input_text:
        return

    # Read the encryption key from 'key.txt'
    key = read_text_from_file(key_file_path)
    if not key:
        return

    # Clean the input text
    cleaned_text = ''.join(char for char in input_text if char.isalpha())

    # Encode the message using the key
    ciphertext = vigenere_cipher(cleaned_text, key)

    # Write the modified ciphertext into 'output.txt'
    write_text_to_file(output_file_path, ciphertext)

if __name__ == "__main__":
    main()