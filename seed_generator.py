from secrets import token_bytes
from hashlib import sha256, pbkdf2_hmac
import unicodedata
from bitstring import BitArray
from blspy import AugSchemeMPL, G1Element, PrivateKey
from chia.util.bech32m import encode_puzzle_hash
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import puzzle_hash_for_pk
from os import path

base_path = [12381, 8444, 2]

with open("english.txt", "r") as f:
    words = f.readlines()
    words = [word.strip() for word in words]

def generate_bytes() -> bytes:
    """
    Generates 32 bytes of entropy.
    """
    return token_bytes(32)

def bytes_from_hash(phrase: str) -> bytes:
    phrase_bytes = phrase.encode("utf-8")
    phrase_hash = sha256(phrase_bytes).digest()
    assert len(phrase_hash) == 32
    return phrase_hash

def double_entropy_bytes(entropy_bytes: bytes) -> bytes:
    """
    Hash input bytes with random bytes
    """
    random_bytes = generate_bytes()
    double_bytes = sha256(entropy_bytes + random_bytes).digest()
    assert len(double_bytes) == 32
    return double_bytes

def bytes_from_file(file_path: str) -> bytes:
    """
    Reads a file and returns its contents as bytes.
    """
    # check if file exists
    if not path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    with open(file_path, "rb") as f:
        file_hash = sha256(f.read()).digest()
        assert len(file_hash) == 32
        return file_hash

def bytes_to_mnemonic(mnemonic_bytes: bytes) -> str:
    if len(mnemonic_bytes) not in [16, 20, 24, 28, 32]:
        raise ValueError(
            f"Data length should be one of the following: [16, 20, 24, 28, 32], but it is {len(mnemonic_bytes)}."
        )
    word_list = words
    CS = len(mnemonic_bytes) // 4

    checksum = BitArray(bytes(sha256(mnemonic_bytes).digest()))[:CS]

    bitarray = BitArray(mnemonic_bytes) + checksum
    mnemonics = []
    assert len(bitarray) % 11 == 0

    for i in range(0, len(bitarray) // 11):
        start = i * 11
        end = start + 11
        bits = bitarray[start:end]
        m_word_position = bits.uint
        m_word = word_list[m_word_position]
        mnemonics.append(m_word)

    return " ".join(mnemonics)

def mnemonic_to_seed(mnemonic: str) -> bytes:
    """
    Uses BIP39 standard to derive a seed from entropy bytes.
    """
    salt_str: str = "mnemonic"
    salt = unicodedata.normalize("NFKD", salt_str).encode("utf-8")
    mnemonic_normalized = unicodedata.normalize("NFKD", mnemonic).encode("utf-8")
    seed = pbkdf2_hmac("sha512", mnemonic_normalized, salt, 2048)

    assert len(seed) == 64
    return seed

def get_wallet_pk_from_sk(sk: PrivateKey) -> PrivateKey:
    """
    Returns a public key from a private key.
    """
    for i in base_path:
        int_sk = AugSchemeMPL.derive_child_sk_unhardened(sk, i)
    return int_sk

def get_observer_address(sk: PrivateKey, path: list[int]) -> str:
    """
    Returns a Chia address from a private key.
    """
    full_path = base_path + path
    for index in full_path:
        sk = AugSchemeMPL.derive_child_sk_unhardened(sk, index)
    
    puzzle_hash = puzzle_hash_for_pk(sk.get_g1())
    address = encode_puzzle_hash(puzzle_hash, "xch")
    return address

def derive_public_key(sk_int: PrivateKey, path: list[int]) -> G1Element:
    """
    Derives a public key from a list of paths.
    """
    pubkey = sk_int
    for index in path:
        pubkey: G1Element = AugSchemeMPL.derive_child_sk_unhardened(pubkey, index)
    return pubkey.get_g1()

def print_public_keys(seed_b: bytes):
    seed = AugSchemeMPL.key_gen(seed_b)
    print("Public keys:")
    print("")
    print(f"Master Public key [m]: {seed.get_g1()}")
    print(f"Wallet Public key [m/12381/8444/2]: {derive_public_key(seed, base_path)}")
    print("First 10 wallet addresses:")
    for i in range(0, 10):
        print(f"Address [{i}]: {get_observer_address(seed, [i])}")

def main():
    print("#############################################")
    print("Mnemonic Seed Generator")
    print("")
    print("1) Generate a random mnemonic phrase")
    print("2) Generate a mnemonic phrase from a phrase")
    print("3) Generate a mnemonic phrase from a file hash")
    print("4) Generate a random mnemonic with entropy phrase")
    choice = input("Enter selection (1-4, q to quit): ")
    if not any(choice == c for c in ["1", "2", "3", "4", "q"]):
        print("Invalid choice.")
        main()
    if choice == "1":
        print("______________________________________________")
        mnemonic = bytes_to_mnemonic(generate_bytes())
        print(f"Generated mnemonic phrase:")
        print(mnemonic)
        seed = mnemonic_to_seed(mnemonic)
        print_public_keys(seed)
        choice = input("Run again? (y/n): ")
        if choice == "y":
            main()
        else:
            exit()
    elif choice == "2":
        print("______________________________________________")
        phrase = input("Enter phrase: ")
        mnemonic = bytes_to_mnemonic(bytes_from_hash(phrase))
        print(f"Generated mnemonic phrase:")
        print(mnemonic)
        seed = mnemonic_to_seed(mnemonic)
        print_public_keys(seed)
        choice = input("Run again? (y/n): ")
        if choice == "y":
            main()
        else:
            exit()
    elif choice == "3":
        print("______________________________________________")
        file_path = input("Enter path to file: ")
        try:
            mnemonic = bytes_to_mnemonic(bytes_from_file(file_path))
        except FileNotFoundError:
            print("File not found.")
            print("")
            main()
        print(f"Generated mnemonic phrase:")
        print(mnemonic)
        seed = mnemonic_to_seed(mnemonic)
        print_public_keys(seed)
        choice = input("Run again? (y/n): ")
        if choice == "y":
            main()
        else:
            exit()
    elif choice == "4":
        print("______________________________________________")
        phrase = input("Enter phrase: ")
        mnemonic = bytes_to_mnemonic(double_entropy_bytes(bytes_from_hash(phrase)))
        print(f"Generated mnemonic phrase:")
        print(mnemonic)
        seed = mnemonic_to_seed(mnemonic)
        print_public_keys(seed)
        choice = input("Run again? (y/n): ")
        if choice == "y":
            main()
        else:
            exit()
    elif choice == "q":
        exit()

if __name__ == "__main__":
    main()