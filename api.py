from flask import Flask, request, jsonify
from db import Database
from multiprocessing import Pool
from db import Database
from main import rm_duplicate, process_data
from flask_cors import CORS
import logging
import time

app = Flask(__name__)
CORS(app)

@app.route("/approval/tx")
def show_approval():
    address = request.args.get("address")
    tx = Database().approve_get_data(int(address, 16))
    print(tx)
    return jsonify(tx)

@app.route("/approval/allowance")
def show_allowance():
    st = time.time()
    address = request.args.get("address")
    dbs = Database().approve_get_data(int(address, 16))
    db = rm_duplicate(dbs)
    pool = Pool(15)
    results = pool.map(process_data, db)
    et = time.time()
    logging.info(f'Execution time: {et - st} seconds  | ADRESS: {address} TX_NO:{len(results)}')
    return (results)