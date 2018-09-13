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


"""
API design:
/acc/api/v1.0/invoices
/acc/api/v1.0/invoices/2  # person
/acc/api/v1.0/invoice/<int:invoice_id>
/acc/api/v1.0/clients  # unique ones
/acc/api/v1.0/uclient/<who>
/acc/api/v1.0/mean
/acc/api/v1.0/sum   #also returns count  (can repeat. n invoie replaces)
/acc/api/v1.0/median
/acc/api/v1.0/latest/<ucid>  # latest invoice by that person

/acc/api/v1.0/sum_unique  (one for each person only: his latest)

For now:
/acc/api/v1.0/invoices
/acc/api/v1.0/invoice/<int:invoice_id>
/acc/api/v1.0/sum

? /acc/api/v1.0/clients  # unique

Error codes:
400  Bad request
404  Error:             unable to process the request sent by the client due to invalid syntax


return 404 in case of resource does not exist(means the url path is wrong)
return 400 only if the rest call is made with some invalid data (non-existaent users)
return ?? when a syntax error

empty: return 404.


"""


def invoice_consistency(iv):
    amount = iv['amount']
    if amount is None:
        return False
    if int(amount) != amount:
        return False

    who = iv['who']
    if who is None:
        return False

    iid = iv['iid']
    if iid is None:
        return False
    if int(amount) != amount:
        return False
    if amount <=0 :
        return False

    return True

def total_consistency():
    for iv in invoices:
        if not invoice_consistency(iv):
            return False
    return True
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
        print("iv['iid']: ", iv['iid'])
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
    if not request.json or not 'iid' in request.json or not 'amount' in request.json or not 'who' in request.json:
        abort(400)
    new_invoice = {
        ######################
        # request.json['field'],
        ########################
        'iid': request.json['iid'],
        'who': request.json['who'],
        'amount': request.json['amount'],

        #more info here
        'timestamp': datetime.datetime.now(),
    }

    if not invoice_consistency(new_invoice):
        abort(400)  # invalid

    invoices.append(new_invoice)

    #############
    # Not directly returned.
    # REST is messy. (A bit open-design: the protocol and conventions are kept. Such as the endpoint having the same name. Returning wrapped. etc.)
    #############
    #return {'invoice': new_invoice}, 201  # AHA
    #       forgot jsonify
    return jsonify({'invoice': new_invoice}), 201  # AHA

"""
201 is:
HTTP defines 201 as the code for "Created".
"""




if __name__ == '__main__':
    app.run(debug=True)

