import logging
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

logging.basicConfig(level=logging.INFO)

# Define constants
DEFAULT_RECEIVING_NUMBER = '254746802541'
CONSUMER_KEY = '35KRcaSFHWxRKu3gLWgG3JgpAGUKA78rRA7BjeE2vN529tXJ'
CONSUMER_SECRET = 'xg4wAfPda9wGseSk5AN6yAoV6vAGNp4229esahXvARoxCRhXiCxxj33eR8q6eFp6'
SHORT_CODE = '174379'
PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

def get_mpesa_access_token():
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    token = response.json().get('access_token')
    logging.info(f"Obtained access token: {token}")
    return token

def initiate_payment(phone_number, amount):
    try:
        access_token = get_mpesa_access_token()
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {'Authorization': f'Bearer {access_token}'}
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f'{SHORT_CODE}{PASSKEY}{timestamp}'.encode()).decode()
        
        phone_number = phone_number.strip()
        if not phone_number.startswith('254'):
            phone_number = '254' + phone_number[1:]
        
        payload = {
            'BusinessShortCode': SHORT_CODE,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': SHORT_CODE,
            'PhoneNumber': phone_number,
            'CallBackURL': 'https://your-callback-url.com/callback',
            'AccountReference': phone_number,
            'TransactionDesc': 'Payment for event',
        }
        
        logging.info(f"Payload: {payload}")
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        logging.info(f"Response: {response.json()}")
        
        if 'CheckoutRequestID' not in response.json():
            logging.error(f"MPesa API response missing 'CheckoutRequestID': {response.json()}")
            return {'error': 'Failed to initiate payment'}
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error initiating payment: {e}")
        if e.response:
            logging.error(f"Response content: {e.response.content}")
        return {'error': 'Failed to initiate payment'}
