import flask
from flask import Flask
from flask import request
from flask_cors import CORS

from tinydb import TinyDB, Query

db = TinyDB("./database/mdm-stay-manager-db.json")

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
                if action == "retrieve":
                    data = storedBooking[0]
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

def calculateValue(booking):
    total_guests = 0
    taxable_guests = 0

    nights = len(booking['stay']['stayNightArray'])

    for night in booking['stay']['stayNightArray']:
        if night['guests'] == None :
            night['guests'] = 0
        if night['externalGuests'] == None :
            night['externalGuests'] = 0
        total_guests = total_guests + night['guests'] + night['externalGuests']
        taxable_guests = taxable_guests + night['guests']

    stay_brut = nights*booking['prices']['villaNight'] + total_guests*booking['prices']['stayNight'] + booking['stay']['pets']*booking['prices']['petNight']
    if str(nights) in booking['discountPerNight']:
        discount = booking['discountPerNight'][str(nights)]
    else:
        discount = booking['discountPerNight'][(max(booking['discountPerNight']))]
    stay_net = stay_brut*(1-discount)

    meal_subtotal = 0
    for meal in booking['meals']:
        meal_subtotal = meal_subtotal + meal['adults']*meal['adultPrice'] + meal['children']*meal['childPrice']
        for cost in meal['costs']:
            try :
                cost_total_price = float(cost['totalPrice'])
                meal_subtotal = meal_subtotal - cost_total_price
            except:
                pass

    costs_total = 0
    paid_total = 0

    for cost in booking['booking']['costs']:
        try :
            total_price =  float(cost["totalPrice"])
            if cost['type'] == 'cost':
                costs_total += total_price
            #     payment = reduction
            elif cost['type'] == 'payment':
                costs_total -= total_price
            elif cost['type'] in ['payment-bank', 'payment-cash']:
                paid_total += total_price

        except:
            pass

    booking_value = stay_net + meal_subtotal + costs_total

    return {'paid_total':paid_total,
            'booking_value':booking_value}

@app.route('/api', methods=['GET'])
def get_bookings():
    db_data = db.all()

    bookingList = []
    for booking in db_data:
        temp_booking = {
            'status':booking['booking']['status'],
            'source':booking['booking']['source'],
            'uuid':booking['booking']['uuid'],
            'invoiceNumber':booking['booking']['invoiceNumber'],
            'arrivalDatetime':booking['stay']['arrivalDatetime'],
            'nights':len(booking['stay']['stayNightArray']),
            'departureDatetime':booking['stay']['departureDatetime'],
            'baseGuests':booking['stay']['baseGuests'],
            'meals':len(booking['meals']),
            'name':booking['contact']['name'],
            'rating': booking['contact']['rating'],
            'bookingValue':calculateValue(booking)['booking_value'],
            'paid':calculateValue(booking)['paid_total']
        }
        bookingList.append(temp_booking)

    bookingList.sort(key=lambda x: x['arrivalDatetime'])

    response = flask.jsonify(bookingList)

    return response


@app.route('/api', methods=['POST'])
def send_data():
    request_json = request.get_json()
    response_json = handleInvoiceData(request_json)

    response = flask.jsonify(response_json)

    return response



if __name__ == '__main__':
    app.run(host="127.0.0.1")
