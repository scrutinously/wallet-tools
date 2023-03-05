from blspy import AugSchemeMPL, PrivateKey, G1Element
from chia.util.bech32m import encode_puzzle_hash, decode_puzzle_hash
from chia.types.blockchain_format.program import Program
from chia.consensus.coinbase import create_puzzlehash_for_pk
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import puzzle_hash_for_pk
from chia.cmds.keys_funcs import resolve_derivation_master_key
from typing import Optional, Union
from pathlib import Path
import os

base_path = [12381, 8444, 2]

def get_sk(fp: Optional[Union[int,str]] = None) -> PrivateKey:
    """
    Returns a private key from a file or a fingerprint.
    """
    master_sk = resolve_derivation_master_key(fp)
    return master_sk

def get_wallet_pk_from_sk(sk: PrivateKey, path: list[int]) -> PrivateKey:
    """
    Returns a public key from a private key.
    """
    for i in base_path:
        int_sk = AugSchemeMPL.derive_child_sk_unhardened(sk, i)
    return int_sk

def derive_public_key(sk_int: PrivateKey, path: list[int]) -> G1Element:
    """
    Derives a public key from a list of paths.
    """
    pubkey = sk_int
    for index in path:
        pubkey: G1Element = AugSchemeMPL.derive_child_sk_unhardened(pubkey, index)
    return pubkey.get_g1()

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

def get_non_observer_address(sk: PrivateKey, path: list[int]) -> str:
    """
    Returns a Chia address from a private key.
    """
    full_path = base_path + path
    for index in full_path:
        sk = AugSchemeMPL.derive_child_sk(sk, index)
    
    puzzle_hash = puzzle_hash_for_pk(sk.get_g1())
    address = encode_puzzle_hash(puzzle_hash, "xch")
    return address

def get_address(sk: PrivateKey, index: int) -> str:
    """
    Returns a Chia address from a public key.
    """
    puzzle_hash = puzzle_hash_for_pk(derive_public_key(sk, [index]))

    #ph = std_tx.curry([Program])

    address = encode_puzzle_hash(puzzle_hash, "xch")
    return address