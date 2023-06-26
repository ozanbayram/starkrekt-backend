from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from starknet_py.net.client_models import Call
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_errors import ClientError
from db import Database


class Contract_addr():
    def __init__(self, contract):
        node_url = "https://starknet-mainnet.g.alchemy.com/v2/ojezKjwSAjeWO896rIjeNti1CzNzSwnG"
        full_node_client = FullNodeClient(node_url=node_url)
        self.provider=Account(
            address=0x02c0c89bec631039bcfc6f5041825baaae37f3f2606ce0d056c65093dd644b1a,
            signer= StarkCurveSigner,
            client=full_node_client,
            chain=StarknetChainId.MAINNET,)
        self.contract = contract

        Database().contract_init(contract) #for cache

    def approval_allowance(self, owner, spender):
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
            allowance = self.provider.client.call_contract_sync(approval_call)[0]
        else:
            try:
                approval_call = Call(
                            to_addr=self.contract,
                            selector=get_selector_from_name("allowance"),
                            calldata=[owner,spender]
                            )
                Database().contract_update_kind(self.contract, "token")
                allowance = self.provider.client.call_contract_sync(approval_call)[0]
            except ClientError:
                approval_call = Call(
                            to_addr=self.contract,
                            selector=get_selector_from_name("isApprovedForAll"),
                            calldata=[owner,spender]
                                      )
                Database().contract_update_kind(self.contract, "nft")
                allowance = self.provider.client.call_contract_sync(approval_call)[0]
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}", self.contract)
                return "unknown"

        return allowance

    def name(self):
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
                name = self.provider.client.call_contract_sync(name_call)
                name = bytearray.fromhex(hex(name[0])[2:]).decode()
                Database().contract_update_name(self.contract, name)
            except:
                return "unknown"

        return name

if __name__ == "__main__":     
    a=Contract_addr("0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3")
    
    q=a.approval_allowance(
                       int("0x37c27b80c6c672a93d8631bec2499dbe012d2120c6a59b9aae8ce0e9e79f4a3", 16),
                       int("0x41682b0bcd5db29046130db68a7f6650433acabc0792db559dac247305df783",16))
    print(q)