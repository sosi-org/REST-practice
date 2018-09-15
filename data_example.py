
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
