def find_best_shift(ciphertext):
    frequencies = {
        'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31,
        'N': 6.95, 'S': 6.28, 'H': 5.92, 'R': 6.02, 'D': 4.32,
        'L': 3.98, 'C': 2.78, 'U': 2.75, 'M': 2.40, 'W': 2.36,
        'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.49,
        'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
        'Z': 0.07
    }

    def calculate_score(text):
        score = 0
        for letter in text:
            if letter.upper() in frequencies:
                score += frequencies[letter.upper()]
        return score

    best_score = 0
    best_text = ''

    for shift in range(1, 26):
        shifted_text = ''
        for letter in ciphertext:
            if letter.isalpha():
                if letter.islower():
                    shifted_text += chr((ord(letter) - ord('a') + shift) % 26 + ord('a'))
                else:
                    shifted_text += chr((ord(letter) - ord('A') + shift) % 26 + ord('A'))
            else:
                shifted_text += letter

        score = calculate_score(shifted_text)
        if score > best_score:
            best_score = score
            best_text = shifted_text

    return best_text

message = "ADSSFFNSJKWLGWAXWJNWAGLQNMFAFWWZETBXTFKQSFWGSTDUOWFLSFFJGAWASFLVJMAJJGWSDSSNFSWVWWKJEHESMJWKNLMMOAAAWJABZLFJDVXSGKGZDGAHJNWZJVOGGSSAAVAKLDGUQKGSXAXHFSXAGGSZKGLIGKADLAKFWVAKQKUGGZXWJKVFSGLZGFSDATLVHFESOXSOASLWKJWXZWSGDADWFFV"
message = message.lower()
print(find_best_shift(message))