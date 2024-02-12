MAX_KEY_LENGTH = 16


def read_text_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None


def findSequence(message):
    size = len(message)
    repeatedSubstringDistance = {}
    for substringLen in range(3, 6):
        for i in range(size - substringLen):
            substring = message[i : i + substringLen]

            for j in range(i + substringLen, size - substringLen):
                if message[j : j + substringLen] == substring:
                    if substring not in repeatedSubstringDistance:
                        repeatedSubstringDistance[substring] = []

                    repeatedSubstringDistance[substring].append(j - i)
    return repeatedSubstringDistance


def getAllFactors(num):
    if num < 2:
        return []
    factors = set()
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.add(i)
            factors.add(num // i)
    factors.discard(1)
    return list(factors)


def getKeyLength(factorList):
    factor_count = {}
    for i in factorList:
        factors = factorList[i]
        for factor in factors:
            if factor <= MAX_KEY_LENGTH:
                factor_count[factor] = factor_count.get(factor, 0) + 1

    #sort factor_count by count
    factor_count = dict(sorted(factor_count.items(), key=lambda x: x[1], reverse=True))

    print("Factor Counts:", factor_count)

    keyLength = [(factor, count) for factor, count in factor_count.items()]

    upper_count = max(keyLength, key=lambda x: x[1])[1]

    standardDeviation = int(0.075 * upper_count)
    lower_limit = upper_count - standardDeviation
    upper_limit = upper_count

    filteredFactors = [
        factor for factor, count in keyLength if lower_limit <= count <= upper_limit
    ]

    print("Filtered Factors:", filteredFactors)

    mostProbableKeyLength = max(filteredFactors)

    return mostProbableKeyLength


def seperateString(message, key_length):
    seperated_string = []
    for i in range(key_length):
        seperated_string.append(message[i::key_length])
    return seperated_string


def find_best_shift(ciphertext):
    frequencies = {
        "E": 12.02,
        "T": 9.10,
        "A": 8.12,
        "O": 7.68,
        "I": 7.31,
        "N": 6.95,
        "S": 6.28,
        "H": 5.92,
        "R": 6.02,
        "D": 4.32,
        "L": 3.98,
        "C": 2.78,
        "U": 2.75,
        "M": 2.40,
        "W": 2.36,
        "F": 2.23,
        "G": 2.02,
        "Y": 1.97,
        "P": 1.93,
        "B": 1.49,
        "V": 0.98,
        "K": 0.77,
        "J": 0.15,
        "X": 0.15,
        "Q": 0.10,
        "Z": 0.07,
    }

    def calculate_score(text):
        score = 0
        for letter in text:
            if letter.upper() in frequencies:
                score += frequencies[letter.upper()]
        return score

    best_score = 0
    best_text = ""

    for shift in range(1, 27):
        shifted_text = ""
        for letter in ciphertext:
            if letter.isalpha():
                if letter.islower():
                    shifted_text += chr(
                        (ord(letter) - ord("a") + shift) % 26 + ord("a")
                    )
                else:
                    shifted_text += chr(
                        (ord(letter) - ord("A") + shift) % 26 + ord("A")
                    )
            else:
                shifted_text += letter

        score = calculate_score(shifted_text)
        if score > best_score:
            best_score = score
            best_text = shifted_text

    return best_text


def calculate_key(split_strings, decrypted_chunks, key_length):
    key = ""

    print("Predicted Key Length:", key_length)

    for i in range(key_length):
        shift_value = (ord(split_strings[i][0]) - ord(decrypted_chunks[i][0])) % 26
        key += chr((shift_value + ord("a")))

    return key


def mergeDecryptedChunks(decrypted_chunks):
    merged_text = ""

    max_length = max(len(chunk) for chunk in decrypted_chunks)

    for i in range(max_length):
        for chunk in decrypted_chunks:
            if i < len(chunk):
                merged_text += chunk[i]

    return merged_text


def reverse_format_output(formatted_text):
    return "".join(formatted_text.split())


def Kasiski_Examination():

    input_file_path = "output.txt"
    cipher = read_text_from_file(input_file_path)
    cipher = reverse_format_output(cipher)
    factorList = {}
    repeatedSubstringDistance = findSequence(cipher)

    for seq in repeatedSubstringDistance:
        factorList[seq] = []
        for spacing in repeatedSubstringDistance[seq]:
            factorList[seq].extend(getAllFactors(spacing))

    keyLength = getKeyLength(factorList)
    splitStrings = seperateString(cipher, keyLength)
    decrypted_chunks = [find_best_shift(splitString) for splitString in splitStrings]
    key = calculate_key(splitStrings, decrypted_chunks, keyLength)
    print("Calculated Key:", key)
    merged_text = mergeDecryptedChunks(decrypted_chunks)
    print("Decrypted Text:", merged_text)


if __name__ == "__main__":
    Kasiski_Examination()
