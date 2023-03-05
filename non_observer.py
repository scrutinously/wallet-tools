from get_coins import rpc, CoinRecord
from sk_derivation import get_non_observer_address, get_sk, encode_puzzle_hash
import asyncio
import csv

node = rpc()

def get_all_addresses(number: int = 100):
    addresses = []
    sk = get_sk()
    for i in range(number):
        addresses.append(get_non_observer_address(sk, [i]))
    return addresses

async def main():
    number = int(input("How many addresses do you want to check? (100 is recommended): "))
    addresses = get_all_addresses(number)
    used_addresses = []
    await node.open_rpc_clients()
    height = await node.get_current_height()
    coins = await node.get_all_address_tx(addresses, 0, height)
    await node.close_rpc_clients()
    index = 0
    balance = 0
    address_balance = {}
    coin: CoinRecord
    for coin in coins:
        ph = coin.coin.puzzle_hash
        address = encode_puzzle_hash(ph, 'xch')
        if address not in used_addresses:
            used_addresses.append(address)
            new_index = addresses.index(address)
            if new_index > index:
                index = new_index
        if not coin.spent:
            balance += coin.coin.amount
            try:
                address_balance[address] += coin.coin.amount
            except KeyError:
                address_balance[address] = coin.coin.amount

    with open('non_observer.txt', 'w') as f:
        for address in used_addresses:
            f.write(f"{address}\n")

    with open('non_observer.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Address', 'Balance'])
        for address in address_balance:
            writer.writerow([address, address_balance[address]])

    print("Addresses with balance:")
    for address in address_balance:
        print(f"{address}: {address_balance[address]}")
    print(f"Total balance: {balance}")
    print(f"Total addresses: {len(used_addresses)}")
    for address in used_addresses:
        print(address)
    print(f"Last address index: {index}")
    
if __name__ == "__main__":
    asyncio.run(main())