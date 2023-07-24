from starknet_py.net.networks import MAINNET, TESTNET
from db import Database
from starknet_py.net.full_node_client import FullNodeClient
import logging

logging.basicConfig(level=logging.INFO, filename='logs/get_block.log', format='%(asctime)s - %(levelname)s - %(message)s')

nft_approval = 0x02d4c8ea4c8fb9f571d1f6f9b7692fff8e5ceaf73b1df98e7da8c1109b39ae9a
token_approval = 0x0219209e083275171774dab1df80982e9df2096516f06319c5c6d71ae0a8480c

node_url = "http://localhost:6060"
mainnet_client = FullNodeClient(node_url=node_url)
#mainnet_client = GatewayClient("mainnet")

def get_block(ilk, son):
    for block_no in range(ilk, son+1):
        logging.info(f"{block_no} is fetching...")
        block = mainnet_client.get_block_sync(block_number=block_no)
        txs = block.transactions
        for tx in txs:
            if "calldata" in dir(tx):
                if int(nft_approval) in tx.calldata or int(token_approval) in tx.calldata:
                    if int(nft_approval) in tx.calldata:
                        kind = "nft"
                        approval_type = nft_approval
                    else:
                        kind = "token"
                        approval_type = token_approval
                    call_array_len = tx.calldata[0]
                    data = tx.calldata[(call_array_len*4)+2:]
                    spender_index = tx.calldata[tx.calldata.index(int(approval_type))+1]
                    spender = hex(data[spender_index])
                    contract = hex(tx.calldata[tx.calldata.index(int(approval_type))-1])
                    tx_hash = hex(tx.hash)
                    tx_from = hex(tx.sender_address)
                    db.approve_insert_data(block_no=block_no, tx_hash=tx_hash, tx_from=tx_from, contract=contract, spender=spender, kind=kind)
                    logging.info(f"{tx_hash}, {block_no}, {contract}, {kind}, {spender}, {tx_from}")

if __name__ == "__main__":     
    db=Database()
    get_block(86000,86050)

