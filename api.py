from flask import Flask, request, jsonify
from db import Database

app = Flask(__name__)

@app.route("/aproval/tx")
def show_approval():
    address = request.args.get("address")
    tx = Database().get_data(int(address, 16))
    print(tx)
    return jsonify(tx)

app.run(debug=True)