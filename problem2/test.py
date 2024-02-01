MAX_KEY_LENGTH = 10


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
    # sorted_factor_by_counts = sorted(factorsByCount, key=lambda x: x[1], reverse=True)

    highest_count = max(factorsByCount, key=lambda x: x[1])[1]

    # Calculate the range within 7.5% of the highest count
    percentage_range = int(0.075 * highest_count)
    lower_limit = highest_count - percentage_range
    upper_limit = highest_count

    # Find the factors within the range
    selected_factors = [factor for factor, count in factorsByCount if lower_limit <= count <= upper_limit]

    # Find the highest factor within the range
    highest_factor_within_range = max(selected_factors)

    return highest_factor_within_range

def Kasiski_Examination():
    seqFactors = {}
    seqSpacings = findSequence("CVJTNAFENMCDMKBXFSTKLHGSOJWHOFUISFYFBEXEINFIMAYSSDYYIJNPWTOKFRHWVWTZFXHLUYUMSGVDURBWBIVXFAFMYFYXPIGBHWIFHHOJBEXAUNFIYLJWDKNHGAOVBHHGVINAULZFOFUQCVFBYNFTYGMMSVGXCFZFOKQATUIFUFERQTEWZFOKMWOJYLNZBKSHOEBPNAYTFKNXLBVUAXCXUYYKYTFRHRCFUYCLUKTVGUFQBESWYSSWLBYFEFZVUWTRLLNGIZGBMSZKBTNTSLNNMDPMYMIUBVMTLOBJHHFWTJNAUFIZMBZLIVHMBSUWLBYFEUYFUFENBRVJVKOLLGTVUZUAOJNVUWTRLMBATZMFSSOJQXLFPKNAULJCIOYVDRYLUJMVMLVMUKBTNAMFPXXJPDYFIJFYUWSGVIUMBWSTUXMSSNYKYDJMCGASOUXBYSMCMEUNFJNAUFUYUMWSFJUKQWSVXXUVUFFBPWBCFYLWFDYGUKDRYLUJMFPXXEFZQXYHGFLACEBJBXQSTWIKNMORNXCJFAIBWWBKCMUKIVQTMNBCCTHLJYIGIMSYCFVMURMAYOBJUFVAUZINMATCYPBANKBXLWJJNXUJTWIKBATCIOYBPPZHLZJJZHLLVEYAIFPLLYIJIZMOUDPLLTHVEVUMBXPIBBMSNSCMCGONBHCKIVLXMGCRMXNZBKQHODESYTVGOUGTHAGRHRMHFREYIJIZGAUNFZIYZWOUYWQZPZMAYJFJIKOVFKBTNOPLFWHGUSYTLGNRHBZSOPMIYSLWIKBANYUOYAPWZXHVFUQAIATYYKYKPMCEYLIRNPCDMEIMFGWVBBMUPLHMLQJWUGSKQVUDZGSYCFBSWVCHZXFEXXXAQROLYXPIUKYHMPNAYFOFHXBSWVCHZXFEXXXAIRPXXGOVHHGGSVNHWSFJUKNZBESHOKIRFEXGUFVKOLVJNAYIVVMMCGOFZACKEVUMBATVHKIDMVXBHLIVWTJAUFFACKHCIKSFPKYQNWOLUMYVXYYKYAOYYPUKXFLMBQOFLACKPWZXHUFJYGZGSTYWZGSNBBWZIVMNZXFIYWXWBKBAYJFTIFYKIZMUIVZDINLFFUVRGSSBUGNGOPQAILIFOZBZFYUWHGIRHWCFIZMWYSUYMAUDMIYVYAWVNAYTFEYYCLPWBBMVZZHZUHMRWXCFUYYVIENFHPYSMKBTMOIZWAIXZFOLBSMCHHNOJKBMBATZXXJSSKNAULBJCLFWXDSUYKUCIOYJGFLMBWHFIWIXSFGXCZBMYMBWTRGXXSHXYKZGSDSLYDGNBXHAUJBTFDQCYTMWNPWHOFUISMIFFVXFSVFRNA")

    for seq in seqSpacings:
        seqFactors[seq] = []
        for spacing in seqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    factorsByCount = getMostCommonFactors(seqFactors)
    print(factorsByCount)

    # allLikelyKeyLengths = []
    # for twoIntTuple in factorsByCount:
    #     allLikelyKeyLengths.append(twoIntTuple[0])
    # return allLikelyKeyLengths

if __name__ == "__main__":
    # print(Kasiski_Examination())
    Kasiski_Examination()
