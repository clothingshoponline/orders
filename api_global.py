# api_global.py

import os
import requests

# corp constants

ORDERS_ENDPOINT = 'https://api.ssactivewear.com/v2/orders/'
RETURNS_ENDPOINT = 'https://api.ssactivewear.com/v2/returns/'
HEADERS = {'Content-Type': 'application/json'}

ACCOUNT = {'cso': os.environ.get('CSO_ACCOUNT'), 
           'walmart': os.environ.get('WALMART_ACCOUNT'),
           'ebay': os.environ.get('EBAY_ACCOUNT'),
           'amazon': os.environ.get('AMAZON_ACCOUNT'),
           'prime': os.environ.get('PRIME_ACCOUNT'),
           'primem': os.environ.get('PRIMEM_ACCOUNT')}

PASSWORD = {'cso': os.environ.get('CSO_PASS'), 
            'walmart': os.environ.get('WALMART_PASS'),
            'ebay': os.environ.get('EBAY_PASS'),
            'amazon': os.environ.get('AMAZON_PASS'),
            'prime': os.environ.get('PRIME_PASS'),
            'primem': os.environ.get('PRIMEM_PASS')}








# requests

def request_successful(response: requests.Response) -> True:
    ''' Raise a HTTPError if the response indicates a failed request. 
    Return True if it indicates a success. '''
    response.raise_for_status()
    return True