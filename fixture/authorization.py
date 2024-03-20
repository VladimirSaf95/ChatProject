import requests
import os

class Authorization:

    def __init__(self, base_url, xnodeid):
        self.base_url = base_url
        self.xnodeid = xnodeid

    def authorizationplayer(self):
        url = 'https://sso-api.k8demo.cyou/account/user/login'
        headers = {
            'accept': 'application/json',
            'x-Node-Id': self.xnodeid,
            'accept-version': '5',
            'Content-Type': 'application/json'
        }
        data = {
            "captchaToken": "string",
            "domain":  self.base_url,
            "login": "testchat101",
            "timezoneId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "password": "Qwert123",
            "playersDeviceInfo": {
                "userAgent": "string",
                "language": "string",
                "accept": "string",
                "canvas": "string",
                "plugins": "string",
                "sessionStorage": True,
                "indexedDb": True,
                "cpuClass": "string",
                "webgl": "string",
                "hasLiedLanguages": True,
                "hasLiedResolution": True,
                "hasLiedOs": True,
                "hasLiedBrowser": True,
                "adBlockOn": True,
                "screenResolution": "string",
                "localStorage": True,
                "webglVendorAndRenderer": "string",
                "fonts": "string",
                "audio": "string",
                "cookie": {
                    "additionalProp1": {
                        "additionalProp1": "string",
                        "additionalProp2": "string",
                        "additionalProp3": "string"
                    },
                    "additionalProp2": {
                        "additionalProp1": "string",
                        "additionalProp2": "string",
                        "additionalProp3": "string"
                    },
                    "additionalProp3": {
                        "additionalProp1": "string",
                        "additionalProp2": "string",
                        "additionalProp3": "string"
                    }
                },
                "cookiesEnabled": True,
                "domBlockers": "string",
                "fontPreferences": "string",
                "screenFrame": "string",
                "osCpu": "string",
                "vendor": "string",
                "vendorFlavors": "string",
                "colorGamut": "string",
                "invertedColors": "string",
                "forcedColors": True,
                "monochrome": 0,
                "contrast": 0,
                "reducedMotion": True,
                "hdr": True,
                "math": "string",
                "deviceType": "Desktop"
            }
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            token = response_json.get('token', '')
            os.environ['API_TOKEN'] = token
        else:
            print('Failed to get token:', response.text)

    def getmatrixtoken(self):
        headers = {
            'x-Node-Id': self.xnodeid,
            'Content-Type': 'application/json',
        }
        token = os.environ.get("API_TOKEN")
        data = {"token": token}
        response = requests.post(f"https://sandbox.multichat.work/api/v1/synapse/auth", json=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            access_token = response_json.get('accessToken')
            user_id = response_json.get('userId')
            user_id = user_id.replace('@', '').split(':')[0]
            os.environ['ACCESS_TOKEN'] = access_token
            os.environ['USER_ID'] = user_id
            return True
        else:
            print(f"Error in request: {response.status_code}")
            return False

    def getroomsid(self):
        response = requests.get(f"https://sandbox.multichat.work/api/v1/correspondence/rooms/{self.xnodeid}")
        if response.status_code == 200:
            rooms = response.json()
            if len(rooms) >= 2:
                for i, room_info in enumerate(rooms[:2], start=1):
                    room_id = room_info.replace('!', '').split(':')[0].get("matrixUid")
                    os.environ[f'ROOM{"A" if i == 1 else "B"}_ID'] = room_id
