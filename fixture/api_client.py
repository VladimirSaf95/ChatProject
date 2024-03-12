import requests
import os

class APIClient:
    def __init__(self, base_url_api, token_1, token_s, token_adm, roomA, roomB, xnodeid, senderid, senderid_adm):
        self.base_url_api = base_url_api
        self.token_1 = token_1
        self.token_s = token_s
        self.token_adm = token_adm
        self.roomA = roomA
        self.roomB = roomB
        self.xnodeid = xnodeid
        self.senderid = senderid
        self.senderid_adm = senderid_adm

    def send_request(self, method, endpoint, headers=None, params=None, data=None, json=None):
        url = f"{self.base_url_api}/{endpoint}"

        # Set default headers if not provided
        if headers is None:
            headers = {}

        # Add authorization token to headers
        if 'Authorization' not in headers:
            headers['Authorization'] = f'Bearer {self.token_1}'

        response = None

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=headers, params=params, data=data, json=json)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, params=params, json=json)

            response.raise_for_status()

        except requests.exceptions.RequestException as err:
            print("Error:", err)

        return response

    def get(self, endpoint, params=None):
        return self.send_request('GET', f"_matrix/client/r0/rooms/{endpoint}", params=params)

    def get_token_s(self, endpoint, params=None):
        return self.send_request('GET', endpoint, headers={'Token': self.token_s}, params=params)

    def post_token1(self, endpoint, data=None, json=None):
        return self.send_request('POST', f"_matrix/client/r0/rooms/{endpoint}", headers={'Content-Type': 'application/json'}, data=data, json=json)

    def post_token_adm(self, endpoint, data=None, json=None):
        return self.send_request('POST', f"_matrix/client/r0/rooms/{endpoint}", headers={'Authorization': f'Bearer {self.token_adm}', 'Content-Type': 'application/json'}, data=data, json=json)

    def post_token_s(self, endpoint, data=None, json=None):
        return self.send_request('POST', endpoint, headers={'Token': self.token_s, 'Content-Type': 'application/json'}, data=data, json=json)

    def delete_token_s(self, endpoint, params=None, json=None):
        return self.send_request('DELETE', endpoint, headers={'Token': self.token_s}, params=params, json=json)

    def sendmessages(self, event_id_A=None, event_id_B=None,  response_a=True, response_b=True):

        data = {"body": "Text Test", "msgtype": "m.text",
                "senderId": f"@{self.senderid}:matrix.netreportservice.xyz"}

        responseA = self.post_token1(f"{self.roomA}%3Amatrix.netreportservice.xyz/send/m.room.message", json=data)
        responseB = self.post_token1(f"{self.roomB}%3Amatrix.netreportservice.xyz/send/m.room.message", json=data)

        responseA_json, responseB_json = responseA.json(), responseB.json()
        event_id_A, event_id_B = responseA_json.get('event_id'), responseB_json.get('event_id')


        if responseA.status_code == 200 and event_id_A:
            os.environ["EVENT_ID_A"] = event_id_A
        if responseB.status_code == 200 and event_id_B:
            os.environ["EVENT_ID_B"] = event_id_B

        if response_a and response_b:
            return responseA, responseB
        elif response_a:
            return responseA
        elif response_b:
            return responseB

    def getuserban(self):
        return self.get_token_s(f"api/v1/synapse/user/ban/{self.xnodeid}")

