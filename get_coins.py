from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.types.coin_record import CoinRecord
from chia.util.config import load_config
from chia.util.ints import uint16
from pathlib import Path
from os import getenv, path, mkdir, listdir, walk, rmdir
from chia.util.bech32m import decode_puzzle_hash, encode_puzzle_hash
import json
import asyncio

hostname = "localhost"
chia_root: Path = Path(path.expanduser(getenv("CHIA_ROOT", "~/.chia/mainnet"))).resolve()

class rpc:
    def __init__(self):
        self.node_rpc_client = None

    async def open_rpc_clients(self):
        config = load_config(chia_root, "config.yaml")
        try:
            node_rpc_port = config["full_node"]["rpc_port"]
            self.node_rpc_client = await FullNodeRpcClient.create(
                hostname, uint16(node_rpc_port), chia_root, config
                ) 
        except Exception as e:
            print(e)
            print("Error opening rpc clients")

    async def close_rpc_clients(self):
        if self.node_rpc_client:
            self.node_rpc_client.close()
            await self.node_rpc_client.await_closed()

    async def get_current_height(self):
        try:
            blockchain_state = await self.node_rpc_client.get_blockchain_state()
            height = blockchain_state["peak"].height
            return height
        except Exception as e:
            print(e)
            print("Error getting current height")

    async def get_address_tx(self, address: str, start_block: int, end_block: int):
        ph = decode_puzzle_hash(address)
        try:
            coins = await self.node_rpc_client.get_coin_records_by_puzzle_hash(ph, True, start_block, end_block)
            return coins
        except Exception as e:
            print(e)
            print("Error getting address tx")

    async def get_all_address_tx(self, addresses: list[str], start_block: int = 0, end_block: int = 3129030):
        all_ph = []
        for address in addresses:
            ph = decode_puzzle_hash(address)
            all_ph.append(ph)

        try:
            coins = await self.node_rpc_client.get_coin_records_by_puzzle_hashes(all_ph, True, start_block, end_block)
            return coins
        except Exception as e:
            print(e)
            print("Error getting address tx")
            self.close_rpc_clients()


async def main():
    rpc_client = rpc()
    await rpc_client.open_rpc_clients()
    height = await rpc_client.get_current_height()
    await rpc_client.close_rpc_clients()
    print(height)

if __name__ == "__main__":
    asyncio.run(main())