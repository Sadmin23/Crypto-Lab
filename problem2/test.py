MAX_KEY_LENGTH = 16


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


def kasiski_examination():
    seqFactors = {}
    seqSpacings = findSequence("VHVSSPQUCEMRVBVBBBVHVSURQGIBDUGRNICJQUCERVUAXSSR")

    for seq in seqSpacings:
        seqFactors[seq] = []
        for spacing in seqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    print(seqFactors)


if __name__ == "__main__":
    kasiski_examination()
