from approve_check import Approval
from db import Database
from multiprocessing import Pool

db = Database().get_data(0x037C27B80c6C672A93d8631bEC2499dbE012d2120c6A59B9aAe8Ce0E9E79f4a3)

appr = Approval()

for data in db:
    #print(data)
    try:
        q=appr.allowance(contract=data["contract"], owner=int(data["tx_from"], 16), spender=int(data["spender"], 16), kind=data["type"])
        print(data["contract"], data["tx_from"], data["spender"],data["type"],q)
    except:
        print(data["contract"], data["tx_from"], data["spender"],data["type"])

