def mergeDecryptedChunks(decrypted_chunks):
    """
    Merges the decrypted chunks according to the specified pattern.
    """
    merged_text = ""

    # Determine the maximum length among the decrypted chunks
    max_length = max(len(chunk) for chunk in decrypted_chunks)

    for i in range(max_length):
        for chunk in decrypted_chunks:
            # Add the current letter from each decrypted chunk to the merged text
            if i < len(chunk):
                merged_text += chunk[i]

    return merged_text

# Example usage:
decrypted_chunks = ["ABC", "DEF", "GHIJKL"]
merged_text = mergeDecryptedChunks(decrypted_chunks)
print(merged_text)