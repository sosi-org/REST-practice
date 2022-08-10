#!python
# !./temp/p3-for-me/bin/python

from flask import Flask

from flask import jsonify
from flask import abort
from flask import request

import client_notifier

API_ENDPOINT_URL = "/acc/api/v1.0"



#import flask
#print("flask.__version__", flask.__version__) # 1.0.2

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

#@app.route('/favicon.ico')
#def favicon():
#    return favicon

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found (Sosi)'}), 404)


###################################################################
#  LOGIC
###################################################################

#import data
from data_example import *

print(invoices)
# import data_class:
from data_operations import *

"""
Private. For test purposes only
"""
"""
@app.route('/todo/api/v1.0/consistency_state', methods=['GET'])
def consistency():
    for iv in invoices:
        if not invoice_consistency(iv):
            return jsonify(iv)
    return jsonify(?)
"""

@app.route(API_ENDPOINT_URL+'/invoices', methods=['GET'])
def invoices_listall():
    """
    Dumps all `invoices`
    """

    #invoices=[]
    #if len(invoices) == 0:
    #    # incorrect usage
    #    abort(404)  # The requested URL was not found on the server.
    #    FIXME

    return jsonify({'invoices': invoices})


@app.route(API_ENDPOINT_URL+'/invoices/<int:invoice_iid>', methods=['GET'])
def invoices_retrieve(invoice_iid):
    """
    """

    if not total_consistency():
        abort(400)

    for iv in invoices:
        #print("iv['iid']: ", iv['iid'])
        if iv['iid'] == invoice_iid:
            return jsonify(iv)
    abort(404)  # does not give more info
    # The requested URL was not found on the server.



##########
import datetime
###########

"""
The URL was defined with a trailing slash so Flask will automatically redirect to the URL with the trailing slash if it was accessed without one.  Make sure to directly send your POST-request to this URL since we can\'t make browsers or HTTP clients redirect with form data reliably or without user interaction.\n\nNote: this exception is only raised in debug mode'<
API_ENDPOINT_URL + '/invoices/'
->
API_ENDPOINT_URL + '/invoices'
"""
@app.route(API_ENDPOINT_URL+'/invoices', methods=['POST'])
def new_invoice():
    ###################
    # `request` first used. Terrible design.
    ###################
    if not request.json:
        abort(400)

    if not 'amount' in request.json or not 'who' in request.json:
        abort(400)

    # increment primary key
    #new_iid = len(invoices)+1-1
    new_iid = invoices[-1]['iid'] + 1

    new_who = request.json['who']
    new_amount = request.json['amount']

    #if new_who is None:  # never happens

    new_invoice = {
        ######################
        # request.json['field'],
        ########################
        'iid': new_iid,
        'who': new_who,
        'amount': new_amount,

        #more info here
        'timestamp': datetime.datetime.now(),
        #TODO: client info (useful for identificaion and binding to uid) from http request
    }

    i,reason = invoice_consistency(new_invoice)
    if not i:
        # TODO: inconsistency exception? No.not a good idea. inconsitencies are more common than that.
        #TODO: show the reason
        #abort(400)  # invalid
        #################
        #  Nice: returns error with reason.
        #################
        return jsonify({'reason': reason}), 400

    # Actual integration
    # in memory
    invoices.append(new_invoice)

    #Then: (next in chain)
    # Todo: make a pipeline. Maybe using RxJS?
    #client_notifier # is the output side of this pipeline
    #client_notifier.notify_newdata(extract_notify(new_invoice))
    client_notifier.notify_newdata_arrival(single_invoice_notify(new_invoice))
    #client_notifier.notify_newintegration()  # notifies the update of the integration. Second fanout branch.

    #branch out:
    # send another copy to quque, which in turn sends two to database, etc.

    """
    1. In memory accumulation
    2. Integration service.
    3. Notifier to client (fast route)
    4. Database accumulation. (1. PostGres 2.Mongo 3.GIS 4. etc) x cluster factor x interleave.
    5. Queue (for other uses?)
    6. Log!


    7. UDP?
    8. 0MQ
    9. Boradcast to vicinity (subscribe?)
    10. RxJS chain. Observer pattern.
    """

    #############
    # Not directly returned.
    # REST is messy. (A bit open-design: the protocol and conventions are kept. Such as the endpoint having the same name. Returning wrapped. etc.)
    #############
    #return {'invoice': new_invoice}, 201  # AHA
    #       forgot jsonify
    return jsonify({'invoice': new_invoice}), 201  # AHA

# logic separate from app.py
#class ClientNotifier
    #client_notifier.notify_newdata_arrival

def single_invoice_notify(new_invoice):
    # extract_notify()
    return new_invoice

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0')  # why?
