from multiprocessing import Pool
from approve_check import Contract_addr
from db import Database
import time

def process_data(data):
    ct = Contract_addr(data["contract"])
    allowance = ct.approval_allowance(owner=int(data["tx_from"], 16), spender=int(data["spender"], 16))
    name = ct.name()
    kind = Database().contract_get_kind(data["contract"])
    return {"name":name, "contract":data["contract"], "spender":data["spender"], "tx_from":data["tx_from"], "kind":kind, "allowance":allowance}


if __name__ == '__main__':
    st = time.time()
    db = Database().approve_get_data("0x10006a2516f6a3eae392c14bd355287a99c16a2d3f1e5d6beaeada7a360106e")
    pool = Pool(15)
    results = pool.map(process_data, db)
    print(results)
    et = time.time()
    print('Execution time:', et - st , 'seconds')
    print(len(results))

