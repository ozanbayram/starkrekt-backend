from multiprocessing import Pool
from approve_check import Contract_addr
from db import Database
import time



def process_data(data):
    ct = Contract_addr(data["contract"])
    #print(data["contract"], data["tx_from"], data["spender"])
    allowance = ct.approval_allowance(owner=int(data["tx_from"], 16), spender=int(data["spender"], 16))
    name = ct.name()
    kind = Database().contract_get_kind(data["contract"])
    return {"name":name, "contract":data["contract"], "spender":data["spender"], "kind":kind, "allowance":allowance}


if __name__ == '__main__':
    st = time.time()
    db = Database().approve_get_data(0x037C27B80c6C672A93d8631bEC2499dbE012d2120c6A59B9aAe8Ce0E9E79f4a3)
    pool = Pool(15)
    results = pool.map(process_data, db)
    print(results)
    et = time.time()
    print('Execution time:', et - st , 'seconds')

