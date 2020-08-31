# api_global.py

import os
import traceback
import pymsteams
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



# Microsoft Teams

MSTEAMS_TEST = os.environ.get('TEST_MSTEAMS_WEBHOOK')


def send_msteams(message: str, program_name: str, channel: str = MSTEAMS_TEST, 
                 include_traceback: bool = True):
    ''' Send the message to the specified Microsoft Teams channel. '''
    ms_message = pymsteams.connectorcard(channel)
    ms_message.title(program_name)
    if include_traceback:
        message = f'{message}\n{traceback.format_exc()}'
    ms_message.text(f'<pre>\n{message}\n</pre>')
    
    ms_message.send()




# requests

def request_successful(response: requests.Response) -> True:
    ''' Raise a HTTPError if the response indicates a failed request. 
    Return True if it indicates a success. '''
    response.raise_for_status()
    return True