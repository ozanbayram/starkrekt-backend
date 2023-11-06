from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from starknet_py.net.client_models import Call
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_errors import ClientError
from db import Database
import logging

logging.basicConfig(level=logging.INFO, filename='logs/approve_check.log', format='%(asctime)s - %(levelname)s - %(message)s')

class Contract_addr():
    def __init__(self, contract):
        node_url = "http://localhost:6060"
        full_node_client = FullNodeClient(node_url=node_url)
        self.provider=Account(
            address=0x02c0c89bec631039bcfc6f5041825baaae37f3f2606ce0d056c65093dd644b1a,
            signer= StarkCurveSigner,
            client=full_node_client,
            chain=StarknetChainId.MAINNET,)
        self.contract = contract

        Database().contract_init(contract) #for cache

    def approval_allowance(self, owner, spender):
        logging.debug("approval_allowance func çalışıyor" )
        kind = Database().contract_get_kind(self.contract)
        if kind:
            if kind == "nft":
                func = "isApprovedForAll"
            elif kind == "token":
                func = "allowance"
            approval_call = Call(
                            to_addr=self.contract,
                            selector=get_selector_from_name(func),
                            calldata=[owner,spender]
                                        )
            try:
                allowance = self.provider.client.call_contract_sync(call=approval_call, block_number="latest")[0]
            except Exception as e:
                logging.exception(f"Exception occurred CT:{self.contract}, SP:{spender}, Owner:{owner}")
        else:
            try:
                approval_call = Call(
                            to_addr=self.contract,
                            selector=get_selector_from_name("allowance"),
                            calldata=[owner,spender]
                            )
                allowance = self.provider.client.call_contract_sync(call=approval_call, block_number="latest")[0]
                Database().contract_update_kind(self.contract, "token")
            except ClientError:
                approval_call = Call(
                            to_addr=self.contract,
                            selector=get_selector_from_name("isApprovedForAll"),
                            calldata=[owner,spender]
                                      )
                allowance = self.provider.client.call_contract_sync(call=approval_call, block_number="latest")[0]
                Database().contract_update_kind(self.contract, "nft")
            except Exception as err:
                logging.exception(f"Unexpected error. {self.contract} ")
                return "unknown"

        return allowance

    def name(self):
        logging.debug("name func çalışıyor" )
        name = Database().contract_get_name(self.contract)
        if name:
            return name
        else:
            name_call = Call(
                            to_addr=self.contract,
                            selector=get_selector_from_name("name"),
                            calldata=[]
                                      )
            try:
                name = self.provider.client.call_contract_sync(call=name_call, block_number="latest")
                name = bytearray.fromhex(hex(name[0])[2:]).decode()
                Database().contract_update_name(self.contract, name)
            except:
                logging.exception(f"Unexpected error. {self.contract} ")
                return "unknown"

        return name

if __name__ == "__main__":     
    a=Contract_addr("0x10006a2516f6a3eae392c14bd355287a99c16a2d3f1e5d6beaeada7a360106e")
    
    q=a.approval_allowance(
                       int("2029465295112035131755114657150204409949577836511997973657918255827659592446"),
                       int("3461208862407773342635871960084685728498932599526891269545319004528055383761"))
    print(q)