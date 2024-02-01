from collections import Counter
import re

def find_repeated_patterns(ciphertext, min_length=3):
    # Find repeated patterns in the ciphertext
    patterns = re.findall(r'(?=(\w{%d,}))' % min_length, ciphertext)
    return patterns

def find_distances(patterns):
    # Find distances between occurrences of each pattern
    distances = []
    for pattern in patterns:
        indices = [i.start() for i in re.finditer(pattern, ciphertext)]
        distances.extend([indices[j+1] - indices[j] for j in range(len(indices)-1)])
    return distances

def find_possible_key_lengths(distances):
    # Find possible key lengths based on greatest common divisor (GCD) of distances
    common_factors = Counter(distances).most_common()
    possible_key_lengths = [factor for factor, count in common_factors if count > 1]
    return possible_key_lengths

def predict_key_length(ciphertext):
    patterns = find_repeated_patterns(ciphertext)
    distances = find_distances(patterns)
    possible_key_lengths = find_possible_key_lengths(distances)
    return possible_key_lengths

def predict_message(ciphertext, key_length):
    # Attempt to predict the original message using the guessed key length
    predicted_message = ''
    for i in range(key_length):
        slice_i = ciphertext[i::key_length]
        most_common_char = Counter(slice_i).most_common(1)[0][0]
        predicted_message += most_common_char

    return predicted_message

# Example usage:
ciphertext_file_path = 'output.txt'
with open(ciphertext_file_path, 'r') as file:
    ciphertext = file.read()

# (a) Predicted key length
possible_key_lengths = predict_key_length(ciphertext)
print("Predicted Key Lengths:", possible_key_lengths)

# (b) Predicted message based on the algorithm
for key_length in possible_key_lengths:
    predicted_message = predict_message(ciphertext, key_length)
    print(f"Predicted Message (Key Length {key_length}): {predicted_message}")

# (c) You can execute the program for each ciphertext generated in Problem 1
# (d) Mark explanations as needed