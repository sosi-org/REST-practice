
from data_example import *
#Shares the main modile's space. Instead of `global invoices`

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
    if represents_float(number_like) and float(number_like) == number_like:
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
