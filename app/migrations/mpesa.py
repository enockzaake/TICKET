import base64
import requests
import datetime as dt
from decouple import config
from .models import MpesaToken
from requests.auth import HTTPBasicAuth
import time
import pytz

class Mpesa():

    def __init__(self):
        self.base_url = config('MPESA_BASE_URL') 
        self.key = config('MPESA_CONSUMER_KEY')
        self.secret =config('MPESA_CONSUMER_SECRET')
        self.pass_key=config('MPESA_PASS_KEY')
        self.short_code = config('MPESA_SHORT_CODE')
        self.callback_base = config('MPESA_CALLBACK')
        
    def get_timestamp(self):
        today = dt.datetime.now()
        month = today.month if len(str(today.month)) != 1 else f"0{today.month}"
        day = today.day if len(str(today.day)) != 1 else f"0{today.day}"
        hour = today.hour if len(str(today.hour)) != 1 else f"0{today.hour}"
        minute = today.minute if len(str(today.minute)) != 1 else f"0{today.minute}"
        second = today.second if len(str(today.second)) != 1 else f"0{today.second}"
        timestamp = f"{today.year}{month}{day}{hour}{minute}{second}"
        return timestamp
    
    def get_password(self, time_stamp):
        password_str = self.short_code + self.pass_key + time_stamp
        password_bytes = password_str.encode("ascii")
        return base64.b64encode(password_bytes).decode("utf-8")

    def get_token(self):
        active_token = MpesaToken.objects.filter(expired = False)
        if active_token.exists():
            active_token = active_token.first()
            # adding utc to datetime.now() then subtracting
            time_difference = (active_token.expiry_time - pytz.utc.localize(dt.datetime.now())).total_seconds()
            print(time_difference)
            if time_difference > 0:
                return active_token.access_token
            else: 
                active_token.expired = True
                active_token.save()

        api_url = f'{self.base_url}generate?grant_type=client_credentials'
        response = requests.request("GET", api_url, auth=HTTPBasicAuth(self.key,self.secret))
            
        final_response = response.json()
        if 'access_token' in final_response:
            final_response['expiry_time'] = pytz.utc.localize(dt.datetime.now() + dt.timedelta(0,int(final_response['expires_in'])))
            MpesaToken.objects.create(**final_response)
            print(final_response)
            return final_response
        return "error"

    def paybill(self, phone_number, price):
        time_stamp = self.get_timestamp()
        password = self.get_password(time_stamp)
        base_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {self.get_token()}'
        }

        payload = {
            "BusinessShortCode": self.short_code,
            "Password": password,
            "Timestamp":time_stamp ,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": str(price),
            "PartyA": str(600977),
            "PartyB": self.short_code,
            "PhoneNumber": f"254{phone_number}",
            "CallBackURL": f"{self.callback_base}transact/pay/mpesa-response",
            "AccountReference": "QRTicket",
            "TransactionDesc": "Online tickets" 
        }
        print(payload)
        response = requests.request("POST", base_url, json = payload, headers = headers)
        print(response)
        return response.json()

    def payment_status(self,checkout_request_id):
        time_stamp = self.get_timestamp()
        password = self.get_password(time_stamp)
        base_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'

        print(self.get_token())
        headers = { 'Content-Type': 'application/json', 'Authorization': f'Bearer {self.get_token()}'}

        payload = {
            "BusinessShortCode": self.short_code,
            "Password": password,
            "Timestamp": time_stamp,
            "CheckoutRequestID": checkout_request_id,
        }

        response = requests.request("POST", base_url, json = payload, headers = headers )
        return response.json()