#!myflask/bin/python3
from flask import Flask

from flask import jsonify
from flask import abort
from flask import request


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

#db:
# master list
invoices = [
    {'amount': 12, 'who': 1, 'extra': "extra information", 'iid':2},
    {'amount': 24, 'who': 2, 'iid': 123},
    {'amount': 32, 'who': "07719", 'iid': 125},
]
"""
Consistency checks:
each one must have am iid, amount, some who. Other fields are optional.
"""

#price? order?


"""
In-memory acumulated states. (deliberate redundancy, similar to cache.)
"""
uinvoices = [
    {'amount': 12, 'ucid': 10},
    {'amount': 32, 'ucid': 20},
]



#users map
clients = [
     #cid, unique_id,  who,  who_id,  person=uniqe_id=ucid: any client_identifier
    {'cid': 1, 'unique_cid': 10},
    {'cid': "07719", 'unique_cid': 10},
    {'cid': 2, 'unique_cid': 20},
]
"""
Consistency checks:
"""




def represents_int(int_like):
    # is_int_like
    try:
        int(int_like)
        return True
    except ValueError:
        return False

def represents_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


def is_int(int_like):
    if represents_int(int_like) and int(int_like) == int_like:
        return True
    return False

def is_amount(number_like):
    # TODO: check aomount has 2 decimal points only.
    if represents_float(number_like) and intfloat(number_like) == number_like:
        return True
    return False

def invoice_consistency(iv):
    """ returns (bool,reason"""
    amount = iv['amount']
    if amount is None:
        return False, "no `Amount` key"

    #if is_intlike(amount):
    #    return False, "`Amount` must be int"

    who = iv['who']
    if who is None:
        return False, "no `Who` key"

    if not 'iid' in iv:
        return False, "no `iid` key"
    iid = iv['iid']
    if iid is None:
        return False, "no `iid` key"

    if not is_amount(amount):
        return False, "`amount` needs to be float/numerical"

    if amount <= 0:
        return False, "`amount` needs to be a positive number"

    return True, ""

def total_consistency():
    """ Returns (bool, reason) """
    last_iv = None
    for iv in invoices:
        conssnt, reasonnot = invoice_consistency(iv)
        if not conssnt:
            return False, "inconsisnency:"+reasonnot

        if last_iv is not None:
            if not last_iv['iid'] < iv['iid']:
                return False, "strictly increaing primary key"

        last_iv = iv
    # TODO: check unique iid (or strictly increasing)
    return True, ""
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

@app.route('/acc/api/v1.0/invoices', methods=['GET'])
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


@app.route('/acc/api/v1.0/invoices/<int:invoice_iid>', methods=['GET'])
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
'/acc/api/v1.0/invoices/'
->
'/acc/api/v1.0/invoices'
"""
@app.route('/acc/api/v1.0/invoices', methods=['POST'])
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
