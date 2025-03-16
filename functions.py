import hashlib

def count_repeated_pattern_from_start(hash: str) -> int:
    sign: str = hash[0]
    for i in range(1, len(hash)):
        if hash[i] != sign:
            return i


def get_sha256_hash(word: str) -> str:
    return hashlib.sha256(word.encode()).hexdigest()


def convert_hex_to_binary(hex: str) -> str:
    hash_in_binary = format(int(hex, 16), '0>42b')
    return f"{"0" * (256-len(hash_in_binary))}{hash_in_binary}"