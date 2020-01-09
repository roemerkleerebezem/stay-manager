import flask
from flask import Flask
from flask import request
from flask_cors import CORS

from tinydb import TinyDB, Query

db = TinyDB("./mdm-stay-manager-db.json")

import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# Handle and update invoice data
def handleInvoiceData(request_json):
    synced = False

    if request_json == {}:
        return 'No payload', 400
    else:
        data = request_json["data"]
        action = request_json["action"]

        if (action == "save") & (data["booking"]["uuid"] != None):
            try:
                db.upsert(data, Query().booking.uuid == data['booking']['uuid'])
                synced = True
            except:
                synced = False
        elif data["booking"]['uuid'] == None:
            data["booking"]['uuid'] = str(uuid.uuid4())
        else:
            bookingUuid = data["booking"]['uuid']
            storedBooking = db.search(Query().booking.uuid == bookingUuid)
            if len(storedBooking) == 1:
                if storedBooking[0] != data:
                    synced = False
                else:
                    synced = True
            else:
                # Needs to be created
                synced = False

    response = {
        "synced": synced,
        "data": data
    }

    return response


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api', methods=['POST'])
def send_data():
    request_json = request.get_json()
    response_json = handleInvoiceData(request_json)

    response = flask.jsonify(response_json)

    return response



if __name__ == '__main__':
    app.run(host="0.0.0.0")
