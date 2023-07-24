from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.account.account import Account
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from starknet_py.net.models import StarknetChainId
import time
from get_block import get_block
from starknet_py.net.client_errors import ClientError
import logging

node_url = "http://localhost:6060"
full_node_client = FullNodeClient(node_url=node_url)
block = full_node_client.get_block_sync(block_number="latest")
current_block = block.block_number

while True:
    time.sleep(2)
    try:
        block = full_node_client.get_block_sync(block_number="latest")
    except:
        logging.exception("Exception occurred")    
    new_query = block.block_number
    if new_query > current_block:
        current_block = new_query
        print("current_block", current_block)
        while True:
            time.sleep(3)
            try:
                get_block(current_block,current_block)
                break
            except ClientError:
                pass
            except:
                logging.exception("Exception occurred")