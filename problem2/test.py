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
    seqSpacings = {}
    for seqlen in range(3, 6):
        for i in range(size - seqlen):
            substring = message[i : i + seqlen]

            for j in range(i + seqlen, size - seqlen):
                if message[j : j + seqlen] == substring:
                    if substring not in seqSpacings:
                        seqSpacings[substring] = []

                    seqSpacings[substring].append(j - i)
    return seqSpacings


def getUsefulFactors(num):
    if num < 2:
        return []
    factors = set()
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.add(i)
            factors.add(num // i)
    factors.discard(1)
    return list(factors)


def getMostCommonFactors(seqFactors):
    factorCounts = {}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor <= MAX_KEY_LENGTH:
                factorCounts[factor] = factorCounts.get(factor, 0) + 1

    factorsByCount = [(factor, count) for factor, count in factorCounts.items()]
    sorted_factor_by_counts = sorted(factorsByCount, key=lambda x: x[1], reverse=True)
    # print(sorted_factor_by_counts)

    highest_count = max(factorsByCount, key=lambda x: x[1])[1]

    # Calculate the range within 7.5% of the highest count
    percentage_range = int(0.075 * highest_count)
    lower_limit = highest_count - percentage_range
    upper_limit = highest_count

    # Find the factors within the range
    selected_factors = [
        factor
        for factor, count in factorsByCount
        if lower_limit <= count <= upper_limit
    ]

    # Find the highest factor within the range
    highest_factor_within_range = max(selected_factors)

    return highest_factor_within_range


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


def mergeDecryptedChunks(decrypted_chunks):
    merged_text = ""

    # Determine the maximum length among the decrypted chunks
    max_length = max(len(chunk) for chunk in decrypted_chunks)

    for i in range(max_length):
        for chunk in decrypted_chunks:
            # Add the current letter from each decrypted chunk to the merged text
            if i < len(chunk):
                merged_text += chunk[i]

    return merged_text


def reverse_format_output(formatted_text):
    return "".join(formatted_text.split())


def Kasiski_Examination():

    input_file_path = "output.txt"
    cipher = read_text_from_file(input_file_path)
    cipher = reverse_format_output(cipher)
    # cipher = "CVJTNAFENMCDMKBXFSTKLHGSOJWHOFUISFYFBEXEINFIMAYSSDYYIJNPWTOKFRHWVWTZFXHLUYUMSGVDURBWBIVXFAFMYFYXPIGBHWIFHHOJBEXAUNFIYLJWDKNHGAOVBHHGVINAULZFOFUQCVFBYNFTYGMMSVGXCFZFOKQATUIFUFERQTEWZFOKMWOJYLNZBKSHOEBPNAYTFKNXLBVUAXCXUYYKYTFRHRCFUYCLUKTVGUFQBESWYSSWLBYFEFZVUWTRLLNGIZGBMSZKBTNTSLNNMDPMYMIUBVMTLOBJHHFWTJNAUFIZMBZLIVHMBSUWLBYFEUYFUFENBRVJVKOLLGTVUZUAOJNVUWTRLMBATZMFSSOJQXLFPKNAULJCIOYVDRYLUJMVMLVMUKBTNAMFPXXJPDYFIJFYUWSGVIUMBWSTUXMSSNYKYDJMCGASOUXBYSMCMEUNFJNAUFUYUMWSFJUKQWSVXXUVUFFBPWBCFYLWFDYGUKDRYLUJMFPXXEFZQXYHGFLACEBJBXQSTWIKNMORNXCJFAIBWWBKCMUKIVQTMNBCCTHLJYIGIMSYCFVMURMAYOBJUFVAUZINMATCYPBANKBXLWJJNXUJTWIKBATCIOYBPPZHLZJJZHLLVEYAIFPLLYIJIZMOUDPLLTHVEVUMBXPIBBMSNSCMCGONBHCKIVLXMGCRMXNZBKQHODESYTVGOUGTHAGRHRMHFREYIJIZGAUNFZIYZWOUYWQZPZMAYJFJIKOVFKBTNOPLFWHGUSYTLGNRHBZSOPMIYSLWIKBANYUOYAPWZXHVFUQAIATYYKYKPMCEYLIRNPCDMEIMFGWVBBMUPLHMLQJWUGSKQVUDZGSYCFBSWVCHZXFEXXXAQROLYXPIUKYHMPNAYFOFHXBSWVCHZXFEXXXAIRPXXGOVHHGGSVNHWSFJUKNZBESHOKIRFEXGUFVKOLVJNAYIVVMMCGOFZACKEVUMBATVHKIDMVXBHLIVWTJAUFFACKHCIKSFPKYQNWOLUMYVXYYKYAOYYPUKXFLMBQOFLACKPWZXHUFJYGZGSTYWZGSNBBWZIVMNZXFIYWXWBKBAYJFTIFYKIZMUIVZDINLFFUVRGSSBUGNGOPQAILIFOZBZFYUWHGIRHWCFIZMWYSUYMAUDMIYVYAWVNAYTFEYYCLPWBBMVZZHZUHMRWXCFUYYVIENFHPYSMKBTMOIZWAIXZFOLBSMCHHNOJKBMBATZXXJSSKNAULBJCLFWXDSUYKUCIOYJGFLMBWHFIWIXSFGXCZBMYMBWTRGXXSHXYKZGSDSLYDGNBXHAUJBTFDQCYTMWNPWHOFUISMIFFVXFSVFRNA"
    # cipher = cipher.lower()
    seqFactors = {}
    seqSpacings = findSequence(cipher)

    for seq in seqSpacings:
        seqFactors[seq] = []
        for spacing in seqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    factorsByCount = getMostCommonFactors(seqFactors)
    # print(factorsByCount)
    splitStrings = seperateString(cipher, factorsByCount)
    # print(splitStrings)
    decrypted_chunks = [find_best_shift(splitString) for splitString in splitStrings]
    # print(decrypted_chunks)

    merged_text = mergeDecryptedChunks(decrypted_chunks)

    return merged_text


if __name__ == "__main__":
    print(Kasiski_Examination())
    # Kasiski_Examination()
