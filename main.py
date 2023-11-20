from multiprocessing import Pool
from approve_check import Contract_addr
from db import Database
import time

def process_data(data):
    ct = Contract_addr(data["contract"])
    allowance = ct.approval_allowance(owner=int(data["tx_from"], 16), spender=int(data["spender"], 16))
    name = ct.name()
    kind = Database().contract_get_kind(data["contract"])
    if kind == "token":
        decimals = ct.decimals() 
    else:
        decimals = None
    return {"name":name, "contract":data["contract"], "spender":data["spender"], "tx_from":data["tx_from"], "kind":kind, "allowance":allowance, "contract_decimals":decimals}


if __name__ == '__main__':
    st = time.time()
    db = Database().approve_get_data(0x1000cf4b1279438f373aaf9ef9b1a619cc560dcbf3370409cabd8dee74f6077)
    pool = Pool(15)
    results = pool.map(process_data, db)
    print(results)
    et = time.time()
    print('Execution time:', et - st , 'seconds')
    print(len(results))

