from blspy import AugSchemeMPL, PrivateKey, G1Element
from chia.util.bech32m import encode_puzzle_hash
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import puzzle_hash_for_pk

base_path = [12381, 8444, 2]

def derive_public_key(publicKey: G1Element, path: list[int]) -> G1Element:
    """
    Derives a public key from a list of paths.
    """
    pubkey = publicKey
    for index in path:
        pubkey: G1Element = AugSchemeMPL.derive_child_pk_unhardened(pubkey, index)
    return pubkey

def get_addresses_from_master_pk(master_pk: str, derivations: int) -> list[str]:
    """
    Returns a list of addresses from a master public key.
    """
    master_pk_b = bytes.fromhex(master_pk)
    master_pk_g1 = G1Element.from_bytes(master_pk_b)
    wallet_pk = derive_public_key(master_pk_g1, base_path)
    addresses = []
    for i in range(0, derivations):
        addresses.append(get_address(wallet_pk, i))
    return addresses

def get_addresses_from_wallet_pk(wallet_pk: str, derivations: int) -> list[str]:
    """
    Returns a list of addresses from a wallet public key.
    """
    wallet_pk_b = bytes.fromhex(wallet_pk)
    wallet_pk_g1 = G1Element.from_bytes(wallet_pk_b)
    addresses = []
    for i in range(0, derivations):
        addresses.append(get_address(wallet_pk_g1, i))
    return addresses

def get_address(pubkey: G1Element, index: int) -> str:
    """
    Returns a Chia address from a public key.
    """
    puzzle_hash = puzzle_hash_for_pk(derive_public_key(pubkey, [index]))

    #ph = std_tx.curry([Program])

    address = encode_puzzle_hash(puzzle_hash, "xch")
    return address

def get_all_addresses(pubkey: G1Element, derivations: int) -> list[str]:
    """
    Returns a Chia address from a public key.
    """
    pubkey_b = bytes.fromhex(pubkey)
    pubkey_g1 = G1Element.from_bytes(pubkey_b)

    addresses = []
    for i in range(0, derivations):
        addresses.append(get_address(pubkey_g1, i))
    return addresses