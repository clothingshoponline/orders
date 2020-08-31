# corp_api.py

import json
import requests
import orders
import api_global


def get_order(po_num: str, marketplace: str) -> orders.Order:
    ''' Return the order from Corp as an orders.Order object. 
    Raise a ValueError if marketplace is not one of the following (not case sensitive):
    CSO, Walmart, eBay, Amazon, Prime, PrimeM. Raise a HTTPError if the request fails. '''
    marketplace = marketplace.lower()
    if marketplace not in list(api_global.ACCOUNT.keys()):
        raise ValueError(f'marketplace {marketplace} does not exist')
    order = orders.Order()
    order.po_number = po_num
    order.marketplace = marketplace
    account_num = api_global.ACCOUNT[order.marketplace]
    password = api_global.PASSWORD[order.marketplace]

    response = requests.get(api_global.ORDERS_ENDPOINT + order.po_number + '?lines=true', 
                            auth = (account_num, password), 
                            headers = api_global.HEADERS)

    if api_global.request_successful(response):
        order_list = response.json()

    for package in order_list:
        if (package['poNumber'] == order.po_number and package['orderType'] != 'Credit' 
            and package['orderStatus'] != 'Cancelled'):
            for line in package['lines']:
                order.add(line['sku'], line['qtyShipped'], package['invoiceNumber'])

    return order

def return_request(order: orders.Order, return_reason: int, return_reason_comment: str = '', 
                   test: bool = True, email: str = '') -> str:
    ''' Attempt to return the order. Send a confirmation email if email is specified. 
    Raise a ValueError if any needed info is invalid. Raise a HTTPError if the request fails. 
    Return the Return Authorization (RA) Number if it succeeds. 
    Return reasons from api.ssactivewear.com documentation:
    1 = Do Not Need, Ordered wrong color, size, qty
    2 = Damaged / Deffective Item
    3 = Keying Error (Ordered X, billed and received Y)
    5 = Wrong Qty (Ordered 10, received 2)
    6 = Other
    7 = Wrong Qty (Ordered 2, received 10)
    10 = Picking Error (Wrong size)
    11 = Picking Error (Wrong style or color).
    The return_reason_comment is only logged in Corp's error log when return_reason is not 1. '''
    if return_reason not in [1, 2, 3, 5, 6, 7, 10, 11]:
        raise ValueError('invalid return_reason')
    elif email != '' and '@' not in email:
        raise ValueError('invalid email')
    elif order.marketplace not in list(api_global.ACCOUNT.keys()):
        raise ValueError('invalid marketplace')
    elif len(order.invoices()) == 0:
        raise ValueError('no invoices in order')

    lines = []
    for invoice in order.invoices():
        for line in order.lines_in_package(invoice):
            lines.append({'invoiceNumber': invoice, 'identifier': line.sku, 'qty': line.qty, 
                          'showBoxes': False, 'returnReason': return_reason, 'isReplace': False, 
                          'returnReasonComment': return_reason_comment})

    account_num = api_global.ACCOUNT[order.marketplace]
    password = api_global.PASSWORD[order.marketplace]
    data = json.dumps({'emailConfirmation': email, 'testOrder': test, 
                       'shippingLabelRequired': False, 'lines': lines})
    response = requests.post(api_global.RETURNS_ENDPOINT, 
                             auth = (account_num, password), 
                             headers = api_global.HEADERS, data = data)

    if api_global.request_successful(response):
        ra_num = response.json()[0]['returnInformation']['raNumber']

    return ra_num


