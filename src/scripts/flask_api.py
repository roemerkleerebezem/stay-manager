import flask
from flask import Flask
from flask import request
from flask_cors import CORS

from tinydb import TinyDB, Query

db = TinyDB("./database/mdm-stay-manager-db.json")

import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def updateSettingProfiles(settings, action):
    # Writes, deletes or updates setting profiles to the setting-profiles.json file
    import json

    with open('setting-profiles.json') as json_file:
        profiles = json.load(json_file)

    updated = False

    if action == 'delete-setting':
        profiles = [profile for profile in profiles if profile['name'] != settings['name']]
    elif action == 'save-setting':
        to_replace = [profile for profile in profiles if (profile['name'] == settings['name'])]
        profiles = [settings if (profile['name'] == settings['name']) else profile for profile in profiles]
        if len(to_replace) > 0:
            updated = True
            for profile in [profile for profile in profiles if (profile['name'] == settings['name'])]:
                profile['default'] = to_replace[0]['default']


    for profile in profiles:
        if profile['name'] == settings['name']:
            if action == 'modify-setting':
                profile['default'] = True
                updated = True
        else :
            if (action == 'modify-setting'):
                profile['default'] = False

    if (action == 'save-setting') & (updated == False):
        settings['default'] = False
        profiles.append(settings)

    with open('setting-profiles.json', 'w') as json_file:
      json.dump(profiles, json_file)

    print([profile['invoiceData']['mainTableFooter'] for profile in profiles])

    return 0

# Returns the data needed to populate the invoice
def getInvoiceObject(data, invoice):
    import dateutil.parser
    import math

    # current date and time
    now = datetime.now()
    now_timestamp = int(datetime.timestamp(now))

    settings = data['settings']

    meta = invoice['meta']

    print = {
        'catering':not invoice['meta']['cateringNoPrint'],
        'stay': not invoice['meta']['stayNoPrint'],
    }

    if meta['uuid'] == None:
        meta['uuid'] = str(uuid.uuid4())

    if meta['creationDate'] == None:
        meta['creationDate'] = now_timestamp

    meta['lastModificationDate'] = now_timestamp

    # LOADING THE DATA FROM THE STORE
    contact = {key: value for (key, value) in data['contact'].items() if key in ['name', 'phone', 'email']}

    allTransactions = data['booking']['costs']

    internalCosts = data['booking']['internalCosts']

    booking = {
        key: value for (key, value) in data['booking'].items()
        if key in ['status', 'invoiceNumber', 'deposits']
    }

    stay = {
        key: value for (key, value) in data['stay'].items()
        if key in ['arrivalDate', 'arrivalTime', 'departureDate', 'departureTime', 'stayNightArray', ]
    }

    meals = data['meals']

    meta.update({
        'minArrivalTime': settings['minArrivalTime'],
        'maxDepartureTime': settings['maxDepartureTime'],
        'creationCity': settings['invoiceData']['creationCity'],
        'mainTableFooter': settings['invoiceData']['mainTableFooter'],
        'mainPageFooter': settings['invoiceData']['mainPageFooter'],
    })

    meta['host'] = settings['invoiceData']['host']
    meta['property'] = settings['invoiceData']['property']

    meta['invoiceIndex'] = f"{datetime.fromtimestamp(meta['creationDate']).year}-{str(datetime.fromtimestamp(meta['creationDate']).month).zfill(2)}-{str(meta['invoiceNumber']).zfill(3)}"

    stayNightArray = stay['stayNightArray']

    # CALCULATING THE INVOICE
    ## VILLA
    villaNights = {
        'external': {
            'units': sum([night['external']['villa'] for night in stayNightArray]),
            'price': 0,
            'total': 0,
            'value': sum([night['external']['villa'] for night in stayNightArray]) * settings['prices']['villa']
        },
        'internal': {
            'units': sum([night['internal']['villa'] for night in stayNightArray]),
            'price': settings['prices']['villa'],
            'total': sum([night['internal']['villa'] for night in stayNightArray]) * settings['prices']['villa']
        },
    }

    ## PETS
    petNights = {
        'units': sum([night['internal']['pets'] for night in stayNightArray]),
        'price': settings['prices']['pet'],
        'total': sum([night['internal']['pets'] for night in stayNightArray]) * settings['prices']['pet']
    }

    ## GUESTS
    guestNights = [
        {
            'internal': {
                'date': night['date'],
                'units': night['internal']['adults'] + night['internal']['kids'],
                'price': settings['prices']['guest'],
                'total': (night['internal']['adults'] + night['internal']['kids']) * settings['prices']['guest']
            },
            'external': {
                'date': night['date'],
                'units': night['external']['adults'] + night['external']['kids'],
                'price': 0,
                'total': 0,
                'value': (night['external']['adults'] + night['external']['kids']) * settings['prices']['guest']
            }
        } for night in stayNightArray
    ]

    ## SUBTOTAL AND BOOKING VALUE BEFORE DISCOUNT
    stayTotalBeforeDiscount = villaNights['internal']['total'] \
                              + sum([night['internal']['total'] for night in guestNights]) \
                              + petNights['total']

    stayValueBeforeDiscount = villaNights['internal']['total'] \
                              + villaNights['external']['value'] \
                              + sum([night['internal']['total'] for night in guestNights]) \
                              + sum([night['external']['value'] for night in guestNights]) \
                              + petNights['total']

    ## DISCOUNT
    discountPercentage = settings['discountPerNight'][str(len(stayNightArray))] if str(str(len(stayNightArray))) in settings['discountPerNight'] else max(settings['discountPerNight'].values())

    stayDiscount = {
        'nights': len(stayNightArray),
        'percentage': discountPercentage,
        'total': discountPercentage * stayTotalBeforeDiscount
    }

    ## EXTRA HOURS after discount, before stay tax
    arrivalDate = datetime.fromtimestamp(stay['arrivalDate'])
    departureDate = datetime.fromtimestamp(stay['departureDate'])
    arrivalTime = datetime.fromtimestamp(stay['arrivalTime'])
    departureTime = datetime.fromtimestamp(stay['departureTime'])
    minArrivalTime = settings['minArrivalTime']
    maxDepartureTime = settings['maxDepartureTime']

    ### Hours are rounded up : 15 minutes = 1 extra hour
    extraArrivalHours = max(0, (minArrivalTime['hour'] + minArrivalTime['minute'] / 60) - (
            arrivalTime.hour + arrivalTime.minute / 60))
    extraDepartureHours = max(0, (departureTime.hour + departureTime.minute / 60) - (
            maxDepartureTime['hour'] + maxDepartureTime['minute'] / 60))

    extraHours = math.ceil(extraArrivalHours + extraDepartureHours)

    stayExtraHours = {
        'units': extraHours,
        'price': settings['prices']['extraHour'],
        'total': extraHours * settings['prices']['extraHour']
    }

    ## STAY SUBTOTAL BEFORE TAX

    stayTotalBeforeTax = stayTotalBeforeDiscount \
                         - stayDiscount['total'] \
                         + stayExtraHours['total']

    stayValueBeforeTax = stayValueBeforeDiscount \
                         - stayDiscount['total'] \
                         + stayExtraHours['total']

    ## TAXE DE SEJOUR as night percentage
    guests = {
        'total': sum([night['internal']['units'] for night in guestNights]),
        'min': min([(night['internal']['units'] + night['external']['units']) for night in guestNights]),
        'max': max([(night['internal']['units'] + night['external']['units']) for night in guestNights])
    }

    if guests['total'] > 0:
        stayTax = {
            'percentage': settings['prices']['taxeSejour'],
            'units': sum([night['internal']['adults'] for night in stayNightArray]),
            'price': round(settings['prices']['taxeSejour'] * stayTotalBeforeTax / guests['total'], 2),
            'total': round(settings['prices']['taxeSejour'] * sum([night['internal']['adults'] for night in stayNightArray]) * (
                    stayTotalBeforeTax / guests['total']), 2)
        }
    else:
        stayTax = {
            'percentage': settings['prices']['taxeSejour'],
            'units': 0,
            'price': 0,
            'total': 0,
        }

    ## STAY TOTAL AND VALUE

    stayTotal = stayTotalBeforeTax + stayTax['total']
    stayValue = stayValueBeforeTax

    ## RESULT STAY
    stayInvoiceData = {
        'arrivalDate': arrivalDate,
        'departureDate': departureDate,
        'arrivalTime': arrivalTime,
        'departureTime': departureTime,
        'villa': villaNights,
        'guests': guestNights,
        'pets': petNights,
        'extraHours':stayExtraHours,
        'totalBeforeDiscount': stayTotalBeforeDiscount,
        'discount': stayDiscount,
        'totalBeforeTax': stayTotalBeforeTax,
        'guestAmount': guests,
        'tax': stayTax if print['stay'] else 0,
        'total': stayTotal if print['stay'] else 0,
        'value': stayValue if print['stay'] else 0,
    }

    ## MEALS
    mealsInvoice = [
        {
            'date': meal['date'] if 'date' in meal else data['booking']['date'],
            'type': meal['type'],
            'adults': {
                'units': meal['adults'],
                'price': meal['adultPrice'],
                'total': meal['adults'] * meal['adultPrice']
            },
            'children': {
                'units': meal['children'],
                'price': meal['childPrice'],
                'total': meal['children'] * meal['childPrice']
            },
        } for meal in meals
    ]

    mealsTotal = sum(
        [
            meal['adults']['total'] + meal['children']['total']
            for meal in mealsInvoice
        ]
    )

    ### MEAL VALUE
    totalMealCosts = sum([
        sum([cost['totalPrice'] for cost in meal['costs']])
        for meal in meals
    ])
    mealsValue = mealsTotal - totalMealCosts

    ## RESULTS MEAL
    mealsInvoiceData = {
        'meals': mealsInvoice if print['catering'] else [],
        'total': mealsTotal if print['catering'] else 0,
        'value': mealsValue if print['catering'] else 0,
    }

    ## MAIN PAGE
    costs = [
        transaction for
        transaction
        in allTransactions
        if transaction['type'] in ['cost']
    ]
    discounts = [
        transaction for
        transaction
        in allTransactions
        if transaction['type'] in ['payment']
    ]
    transactions = [
        transaction for
        transaction
        in allTransactions
        if transaction['type'] in ['payment-bank', 'payment-cash']
    ]

    mainTotal = stayInvoiceData['total'] + mealsInvoiceData['total'] + sum(
        [cost['totalPrice'] for cost in costs]) - sum([discount['totalPrice'] for discount in discounts])
    mainValue = stayInvoiceData['value'] + mealsInvoiceData['value'] + sum(
        [cost['totalPrice'] for cost in costs]) - sum([discount['totalPrice'] for discount in discounts]) - sum([cost['totalPrice'] for cost in internalCosts])

    mainToPay = mainTotal - sum([transaction['totalPrice'] for transaction in transactions])
    mainValueToPay = mainValue - sum([transaction['totalPrice'] for transaction in transactions])

    ## RESULTS MAIN PAGE
    mainInvoiceData = {
        'status': booking['status'],
        'contact': contact,
        'total': mainTotal,
        'costs':costs,
        'transactions':transactions,
        'discounts':discounts,
        'toPay': mainToPay,
        'value': mainValue,
        'valueToPay': mainValueToPay,
        'deposits': booking['deposits'],
    }

    invoiceData = {
        'meta': meta,
        'stay': stayInvoiceData,
        'meals': mealsInvoiceData,
        'main': mainInvoiceData,
    }

    return invoiceData

# Handle and update invoice data
def handleInvoiceData(request_json):
    synced = False

    if request_json == {}:
        return 'No payload', 400
    else:
        data = request_json["data"]
        action = request_json["action"]

        if action in ['save-setting', 'delete-setting', 'modify-setting']:
            updateSettingProfiles(data, action)

        elif (action == 'get-invoice'):
            invoiceData = getInvoiceObject(data, request_json['invoice'])
            response = invoiceData
            return response

        elif (action == "save") & (data["booking"]["uuid"] != None):
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


@app.route('/api', methods=['GET'])


def get_bookings():
    db_data = db.all()

    bookingList = []

    for booking in db_data:
        tempInvoice = {
            'meta': {
                'uuid': None,
                'lastModificationDate': None,
                'creationDate': None,
                'cateringNoPrint': False,
                'stayNoPrint': False,
                'contractNoPrint': False,
                'invoiceNumber': booking['booking']['invoiceNumber'],
            },
        }
        invoice = getInvoiceObject(booking, tempInvoice)



        temp_booking = {
            'status':invoice['main']['status'],
            'source':booking['booking']['source'],
            'uuid':booking['booking']['uuid'],
            'invoiceNumber':invoice['meta']['invoiceNumber'],
            'arrivalDate':datetime.timestamp(invoice['stay']['arrivalDate']),
            'arrivalTime':datetime.timestamp(invoice['stay']['arrivalTime']),
            'departureDate':datetime.timestamp(invoice['stay']['departureDate']),
            'departureTime':datetime.timestamp(invoice['stay']['departureTime']),
            'nights':len(invoice['stay']['guests']),
            'minGuests': invoice['stay']['guestAmount']['min'],
            'maxGuests': invoice['stay']['guestAmount']['max'],
            'tax': invoice['stay']['tax']['total'],
            'taxNights': invoice['stay']['tax']['units'],
            'meals':len(invoice['meals']['meals']),
            'name':invoice['main']['contact']['name'],
            'rating': booking['contact']['rating'],
            'value':invoice['main']['value'],
            'total':invoice['main']['total'],
            'paid':invoice['main']['total'] - invoice['main']['toPay']
        }
        bookingList.append(temp_booking)

    bookingList.sort(key=lambda x: x['arrivalDate'])

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
