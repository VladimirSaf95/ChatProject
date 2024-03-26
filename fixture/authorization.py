import requests
import os

class Authorization:

    def __init__(self, base_url, xnodeid):
        self.base_url = base_url
        self.xnodeid = xnodeid

    def get_api_token(self, login, password):

        if self.base_url.startswith("https://"):
            self.base_url = self.base_url[8:]  # Удаляем "https://"

        if self.base_url.endswith("/"):
            self.base_url = self.base_url[:-1]  # Удаляем последний символ "/"

        url = 'https://sso-api.k8demo.cyou/account/user/login'
        headers = {
            'accept': 'application/json',
            'x-Node-Id': self.xnodeid,
            'accept-version': '5',
            'Content-Type': 'application/json'


        }
        data = {
            "captchaToken": "string",
            "domain": self.base_url,
            "login": login,
            "timezoneId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "password": password,
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
        if response.status_code == 201:
            response_json = response.json()
            token = response_json.get('token', '')
            return token
        else:
            print('Failed to get token:', response.text)
            return None

    def get_matrix_token(self, api_token):
        headers = {
            'x-Node-Id': self.xnodeid,
            'Content-Type': 'application/json',
        }
        data = {"token": api_token}
        response = requests.post(f"https://sandbox.multichat.work/api/v1/synapse/auth?token={api_token}&nodeId={self.xnodeid}", json=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            access_token = response_json.get('accessToken')
            user_id = response_json.get('userId')
            user_id = user_id.replace('@', '').split(':')[0]
            return access_token, user_id
        else:
            print(f"Error in request: {response.status_code}")
            return None, None


    def get_rooms_id(self):
        response = requests.get(f"https://sandbox.multichat.work/api/v1/correspondence/rooms/{self.xnodeid}")
        # Проверка успешности запроса
        if response.status_code == 200:
            # Преобразование текста ответа в формат JSON
            response_json = response.json()

            # Получение matrixUid для первых двух элементов списка
            matrix_uids = [item['matrixUid'].split(':')[0] for item in response_json[:2]]

            # Проверка, что в списке есть два элемента
            if len(matrix_uids) >= 2:
                roomA = matrix_uids[0]
                roomB = matrix_uids[1]
                return roomA, roomB
        return None, None
