import hashlib

def count_repeated_pattern_from_start(hash: str) -> int:
    """
    Counts how many times the first character is repeated consecutively from the start of a binary hash string.

    Args:
        hash (str): A binary string representation of the hash.

    Returns:
        int: The count of repeated characters starting from the beginning. Returns 0 if the input string is empty.
    """

    if hash == "":
        return 0

    sign: str = hash[0]
    for i in range(1, len(hash)):
        if hash[i] != sign:
            return i
        
    return len(hash)


def get_sha256_hash(word: str) -> str:
    """
    Convert a string into a SHA-256 hash.

    Args:
        word (str): A input string to be hashed.

    Returns:
        str: The resulting SHA-256 hash as a hexadecimal string.
    """

    return hashlib.sha256(word.encode()).hexdigest()


def convert_hex_to_binary(hex: str) -> str:
    """
    Convert a hexadecimal string into its 256-bit binary representation.

    Args:
        hex (str): A hexadecimal string.

    Returns:
        str: A 256-character binary string.
    """

    hash_in_binary: str = format(int(hex, 16), '0>42b')
    padding = "0" * (256-len(hash_in_binary))
    return f"{padding}{hash_in_binary}"