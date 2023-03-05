# wallet-tools
Python tools for examining wallet transactions and balances from a full node

## Installation
Linux/WSL (2 install options available):
Option 1: Install chia-blockchain from source [following directions here](https://github.com/Chia-Network/chia-blockchain/wiki/INSTALL#install-from-source) then run these files from within the chia-blockchain venv.

Option 2: 
1. `git clone https://github.com/scrutinously/wallet-tools.git`
2. `cd wallet-tools`
3. `python -m venv ./venv` (or whatever your python binary is called, like `python3' on ubuntu)
4. `source ./venv/bin/activate`
5. `pip install -r requirements.txt`

Windows:
Preferably, just follow the above instructions in WSL.

## Usage
### non_observer.py
For non-observer wallet checking, you will need a full node running with the keys for the wallet you want to check.

Run the script with `python non_observer.py` and follow the prompt. The script will derive the specified number of non-observer addresses, then theck for coin-records on all of those addresses and determine the highest derivation index that the wallet achieved before observer addresses became the default. A list of all addresses that had coin records will be output into a file called `non_observer.txt` in the current working directory, and a csv file of each address that still has a balance called `non_observer.csv` will also be output.

### seed_generator.py
This script was created with the initial idea of being a tool to generate cold wallet mnemonics without installing the mnemonic into any keyring, writing it to any file, or putting it in any clipboard buffer. It will generate a random mnemonic phrase from the BIP39 wordlist. This script also allows you to seed it with your own words/phrase for a deterministic method for re-creating your mnemonic. **WARNING** *Because your mnemonic is reproducable, it will then only be as strong as the phrase you use to create it, rather than having 24 words of entropy for security, ensure that your chosen phrase is complex enough to not be guessed/brute-forced.* You also have the option to use the hash of a file as the seed for the mnemonic, which will be reproducable as long as the file is not changed. This is useful for generating a mnemonic from a file that is stored in a secure location, which you can than recover the mnemonic from if you lose the 24 words. This method will only be secure if the file is not changed, not obvious as to its purpose, and only you know that it can be used to recover your mnemonic.

This script will output the mnemonic to the terminal, which you can then write down (it is inadvisable to store the mnemonic in a file). The script will also output the Master Public Key, and the Wallet Observer Public Key (derived at HD path m/12381/8444/2), and the first 10 observer wallet addresses. It is safe to copy these public keys and addresses to a file for usage on another system. You can then use the public keys to derive any other public keys/addresses you may need.