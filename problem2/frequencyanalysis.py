def calculateLetterFrequency(text):
    letter_frequency = {}

    for char in text:
        if char.isalpha():  # Consider only alphabetic characters
            char = char.upper()  # Convert to uppercase for case-insensitivity
            letter_frequency[char] = letter_frequency.get(char, 0) + 1

    return letter_frequency


message = "taaeenhinhsaTafeStnufehleabvwrrreipwnarnrathenrclrmrortaeeddwsdhootthmathifidtrsiedadceuesarnnaneetretisedltaazeeplriphdotrittwrrmtoncsblfaeptopauiyhnSbhhNceahyaehepwolpecarezniaretrsllrnnnrulrsootblhhaeglltwhiraTlevyhvhlnsehgyzrnssaddrspchearedsaaoeewwdatattzoehsaemtrsdelarehkehrodwhbsioetosee"
print(calculateLetterFrequency(message))
