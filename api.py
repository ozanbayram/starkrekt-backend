from flask import Flask, request
from db import Database

app = Flask(__name__)

@app.route("/aproval/tx")
def show_approval():
    address = request.args.get("address")
    tx = Database().get_data(int(address, 16))
    print(tx)
    return tx
