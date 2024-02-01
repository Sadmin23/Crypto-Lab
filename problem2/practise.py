import re

NONLETTERS_PATTERN = re.compile('[^A-Z]')

MAX_KEY_LENGTH = 16

def read_text_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def findRepeatSequencesSpacings(message):
    # Goes through the message and finds any 3 to 5 letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).

    # Use a regular expression to remove non-letters from the message.
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # Compile a list of seqLen-letter sequences found in the message.
    seqSpacings = {}  # keys are sequences, values are list of int spacings
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            # Determine what the sequence is, and store it in seq
            seq = message[seqStart:seqStart + seqLen]

            # Look for this sequence in the rest of the message
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # Found a repeated sequence.
                    if seq not in seqSpacings:
                        seqSpacings[seq] = []  # initialize blank list

                    # Append the spacing distance between the repeated
                    # sequence and the original sequence.
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings

def getUsefulFactors(num):

    if num < 2:
        return []  # Numbers less than 2 have no useful factors

    factors = set()  # The set of factors found

    # When finding factors, you only need to check integers up to MAX_KEY_LENGTH.
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.add(i)
            factors.add(num // i)

    factors.discard(1)  # Remove 1 from the set of factors, if present

    return list(factors)

def getMostCommonFactors(seqFactors):
    # Initialize a dictionary to store factor counts.
    factorCounts = {}

    # Iterate through sequences and their associated factor lists.
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            # Update factor counts in the dictionary.
            if factor <= MAX_KEY_LENGTH:
                factorCounts[factor] = factorCounts.get(factor, 0) + 1

    # Create a list of tuples containing factors and their counts.
    factorsByCount = [(factor, count) for factor, count in factorCounts.items()]

    # Sort the list by the factor count in descending order.
    factorsByCount.sort(key=lambda x: x[1], reverse=True)

    return factorsByCount


# Example usage:
input_file_path = "cipher.txt"
key_file_path = "key.txt"
output_file_path = "output.txt"
message = read_text_from_file(input_file_path)
#message = "CVJTNAFENMCDMKBXFSTKLHGSOJWHOFUISFYFBEXEINFIMAYSSDYYIJNPWTOKFRHWVWTZFXHLUYUMSGVDURBWBIVXFAFMYFYXPIGBHWIFHHOJBEXAUNFIYLJWDKNHGAOVBHHGVINAULZFOFUQCVFBYNFTYGMMSVGXCFZFOKQATUIFUFERQTEWZFOKMWOJYLNZBKSHOEBPNAYTFKNXLBVUAXCXUYYKYTFRHRCFUYCLUKTVGUFQBESWYSSWLBYFEFZVUWTRLLNGIZGBMSZKBTNTSLNNMDPMYMIUBVMTLOBJHHFWTJNAUFIZMBZLIVHMBSUWLBYFEUYFUFENBRVJVKOLLGTVUZUAOJNVUWTRLMBATZMFSSOJQXLFPKNAULJCIOYVDRYLUJMVMLVMUKBTNAMFPXXJPDYFIJFYUWSGVIUMBWSTUXMSSNYKYDJMCGASOUXBYSMCMEUNFJNAUFUYUMWSFJUKQWSVXXUVUFFBPWBCFYLWFDYGUKDRYLUJMFPXXEFZQXYHGFLACEBJBXQSTWIKNMORNXCJFAIBWWBKCMUKIVQTMNBCCTHLJYIGIMSYCFVMURMAYOBJUFVAUZINMATCYPBANKBXLWJJNXUJTWIKBATCIOYBPPZHLZJJZHLLVEYAIFPLLYIJIZMOUDPLLTHVEVUMBXPIBBMSNSCMCGONBHCKIVLXMGCRMXNZBKQHODESYTVGOUGTHAGRHRMHFREYIJIZGAUNFZIYZWOUYWQZPZMAYJFJIKOVFKBTNOPLFWHGUSYTLGNRHBZSOPMIYSLWIKBANYUOYAPWZXHVFUQAIATYYKYKPMCEYLIRNPCDMEIMFGWVBBMUPLHMLQJWUGSKQVUDZGSYCFBSWVCHZXFEXXXAQROLYXPIUKYHMPNAYFOFHXBSWVCHZXFEXXXAIRPXXGOVHHGGSVNHWSFJUKNZBESHOKIRFEXGUFVKOLVJNAYIVVMMCGOFZACKEVUMBATVHKIDMVXBHLIVWTJAUFFACKHCIKSFPKYQNWOLUMYVXYYKYAOYYPUKXFLMBQOFLACKPWZXHUFJYGZGSTYWZGSNBBWZIVMNZXFIYWXWBKBAYJFTIFYKIZMUIVZDINLFFUVRGSSBUGNGOPQAILIFOZBZFYUWHGIRHWCFIZMWYSUYMAUDMIYVYAWVNAYTFEYYCLPWBBMVZZHZUHMRWXCFUYYVIENFHPYSMKBTMOIZWAIXZFOLBSMCHHNOJKBMBATZXXJSSKNAULBJCLFWXDSUYKUCIOYJGFLMBWHFIWIXSFGXCZBMYMBWTRGXXSHXYKZGSDSLYDGNBXHAUJBTFDQCYTMWNPWHOFUISMIFFVXFSVFRNA"
result = findRepeatSequencesSpacings(message)

# Print the result
for seq, spacings in result.items():
    print(f"Sequence: {seq}, Spacings: {spacings}")