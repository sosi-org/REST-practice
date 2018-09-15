#!myflask/bin/python3
from flask import Flask

from flask import jsonify
from flask import abort
from flask import request

API_ENDPOINT_URL = "/acc/api/v1.0"

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
        #TODO: show the reason
        #abort(400)  # invalid
        #################
        #  Nice: returns error with reason.
        #################
        return jsonify({'reason': reason}), 400

    invoices.append(new_invoice)

    #############
    # Not directly returned.
    # REST is messy. (A bit open-design: the protocol and conventions are kept. Such as the endpoint having the same name. Returning wrapped. etc.)
    #############
    #return {'invoice': new_invoice}, 201  # AHA
    #       forgot jsonify
    return jsonify({'invoice': new_invoice}), 201  # AHA



if __name__ == '__main__':
    app.run(debug=True)
