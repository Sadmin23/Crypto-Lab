def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None


file_path = 'input.txt'
text = read_text_from_file(file_path)
if text:
    print(text)
