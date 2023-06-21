from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from custom_proxy_check import USDCProxyCheck
from starknet_py.proxy.proxy_check import StarknetEthProxyCheck, ArgentProxyCheck, OpenZeppelinProxyCheck
from starknet_py.proxy.contract_abi_resolver import ProxyConfig

class Approval():
    def __init__(self):
        node_url = "https://starknet-mainnet.g.alchemy.com/v2/U_b8ufSWw8Q1l4gnTaMGlq7wl4PdW14_"
        full_node_client = FullNodeClient(node_url=node_url)
        self.provider=Account(
            address=0x02c0c89bec631039bcfc6f5041825baaae37f3f2606ce0d056c65093dd644b1a,
            signer= StarkCurveSigner,
            client=full_node_client,
            chain=StarknetChainId.MAINNET,
                            )
        self.proxy_config = ProxyConfig(proxy_checks=[USDCProxyCheck() ,ArgentProxyCheck(), StarknetEthProxyCheck(), OpenZeppelinProxyCheck()])
    
    def allowance(self, contract, owner, spender, kind):
        if kind == "nft":
            func = "isApprovedForAll"
        else :
            func = "allowance"
        try:
            contract_call = Contract.from_address_sync(address=contract, provider=self.provider, proxy_config=self.proxy_config)
        except:
            contract_call = Contract.from_address_sync(address=contract, provider=self.provider, proxy_config=False)
        contract_call = contract_call.functions[func].prepare(owner, spender).call_sync()
        allowance = int(contract_call.as_tuple()[0])
        return allowance
    
    def revoke(self, contract, spender, kind):
        if kind == "nft":
            func = "setApprovalForAll"
        else :
            func = "approve"
        try:
            contract_call = Contract.from_address_sync(address=contract, provider=self.provider, proxy_config=self.proxy_config)
        except:
            contract_call = Contract.from_address_sync(address=contract, provider=self.provider, proxy_config=False)
        contract_call = contract_call.functions[func].prepare(spender, 0).call_sync()



if __name__ == "__main__":     
    a=Approval().allowance(0x04d0390b777b424e43839cd1e744799f3de6c176c7e32c1812a41dbd9c19db6a,
                       0x10055337e225d8461b0d5baca28942bf1d6089f1870a6fbf03313875b51db50,
                       0x7a6f98c03379b9513ca84cca1373ff452a7462a3b61598f0af5bb27ad7f76d1,
                       "token")
    print(a)

