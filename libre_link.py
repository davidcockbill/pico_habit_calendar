#!/usr/bin/env python3

import urequests
from context import Context
from wifi import Wifi
import binascii
import hashlib
import time
from libre_config import USER, PASSWORD


class LibreLinkException(Exception):
    pass


class LibreLink:
    def __init__(self, user, pwd):
        self.username = user
        self.password = pwd
        self.url = 'https://api-eu2.libreview.io'
        self.headers = {
            'product': 'llu.android',
            'version': '4.16.0',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0',
            'accept': 'application/json',
        }
        self.patient_id = None

    def check_status_code(self, response):
        if response.status_code != 200:
            status_code = response.status_code
            print(f'{status_code}: {response.text}')
            raise LibreLinkException(f'Status: {status_code}')
    
    def get_reading(self):
        if self.patient_id:
            response = urequests.get(
                f'{self.url}/llu/connections/{self.patient_id}/graph',
                headers=self.headers,
            )
            self.check_status_code(response)

            json = response.json()
            value = json['data']['connection']['glucoseMeasurement']['Value']
            trend = json['data']['connection']['glucoseMeasurement']['TrendArrow']
            colour = json['data']['connection']['glucoseMeasurement']['MeasurementColor']
            return (value, trend, colour)
        else:
            return self.login()
        
    def login(self):
        print(f'Logging in to {self.username}')
        response = urequests.post(
            f"{self.url}/llu/auth/login",
            headers=self.headers,
            json={'email': self.username, 'password': self.password},
        )
        self.check_status_code(response)
        response_json = response.json()

        auth_token = response_json['data']['authTicket']['token']
        self.headers['authorization'] = f'Bearer {auth_token}'

        user_id = response_json["data"]["user"]["id"]
        sha256_digest = hashlib.sha256(user_id.encode('utf-8')).digest()
        account_id = binascii.hexlify(sha256_digest).decode('utf-8')

        self.headers['account-id'] = account_id
        patient_details = self.get_patient_details()
        self.patient_id = patient_details['patientId']

        value = patient_details['glucoseMeasurement']['Value']
        trend = patient_details['glucoseMeasurement']['TrendArrow']
        colour = patient_details['glucoseMeasurement']['MeasurementColor']
        return (value, trend, colour)

    def get_patient_details(self, patient_idx=0):
       response = urequests.get(f'{self.url}/llu/connections', headers=self.headers)
       print(f'{response.status_code}: {response.text}')

       json = response.json()
       return json['data'][patient_idx]


if __name__ == '__main__':
    Wifi(Context()).connect()
    client = LibreLink(USER, PASSWORD)
    print(f'{client.get_reading()}')
    time.sleep(30)
    print(f'{client.get_reading()}')

