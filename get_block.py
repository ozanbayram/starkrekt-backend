from starknet_py.net.networks import MAINNET, TESTNET
from dbdocker import Database
from starknet_py.net.full_node_client import FullNodeClient
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

approval_input1 = 0x02d4c8ea4c8fb9f571d1f6f9b7692fff8e5ceaf73b1df98e7da8c1109b39ae9a
approval_input2 = 0x0219209e083275171774dab1df80982e9df2096516f06319c5c6d71ae0a8480c

node_url = "http://localhost:6060"
mainnet_client = FullNodeClient(node_url=node_url)
db=Database()

def get_block(ilk, son):
    for block_no in range(ilk, son+1):
        logging.info(f"{block_no} is fetching...")
        block = mainnet_client.get_block_sync(block_number=block_no)
        txs = block.transactions
        #tx = mainnet_client.get_transaction_sync("0x067610f0d8c4e67d370e3781bd419bfb8d86081591ac84191d93748ad8fef017")
        for tx in txs:
            if "calldata" in dir(tx):
                if int(approval_input1) in tx.calldata or int(approval_input2) in tx.calldata:
                    if int(approval_input1) in tx.calldata:
                        approval_input = approval_input1
                    else:
                        approval_input = approval_input2

                    call_array_len = tx.calldata[0]

                    #calldata_len_index = (call_array_len*4)+1 #for cairo 0
                    #calldata_len = tx.calldata[calldata_len_index]
                    #full_data_len = calldata_len_index + calldata_len + 1
                    try:
                        checking_cairo_1_or_0 = tx.calldata[tx.calldata.index(int(approval_input))+2]
                        if checking_cairo_1_or_0 > 1000: #is cairo 1
                            contract = hex(tx.calldata[tx.calldata.index(int(approval_input))-1])
                            #tx_hash = hex(tx.hash)
                            tx_from = hex(tx.sender_address)
                            spender = hex(tx.calldata[tx.calldata.index(int(approval_input))+2])

                        else: #is cairo 0
                            data = tx.calldata[(call_array_len*4)+2:]
                            spender_index = tx.calldata[tx.calldata.index(int(approval_input))+1]
                            spender = hex(data[spender_index])
                            contract = hex(tx.calldata[tx.calldata.index(int(approval_input))-1])
                            #tx_hash = hex(tx.hash)
                            tx_from = hex(tx.sender_address)
                        db.approve_insert_data(tx_from=tx_from, contract=contract, spender=spender)
                        logging.info(f"{contract}, {spender}, {tx_from}")
                    except:
                        logging.exception(f"{contract}, {spender}, {tx_from}")

if __name__ == "__main__":     
    #db=Database()
    get_block(300000,380000)