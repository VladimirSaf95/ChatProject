import os
import time
from urllib.parse import quote
import json
import pytest

from fixture.api_client import APIClient


# ROOM A
# Отправка текстового сообщения в чат
def test_sendmessages(api_client):
    responseA, responseB = api_client.sendmessages()

    #Проверка на код ответа
    assert responseA.status_code == 200
    assert "The message is invalid" not in responseA.text
    assert responseB.status_code == 200
    assert "The message is invalid" not in responseB.text

    #Проверка на ключ в ответе json
    assert "event_id" in responseA.json(), "The key 'event_id' is not found in the JSON response"
    assert "event_id" in responseB.json(), "The key 'event_id' is not found in the JSON response"

    # Проверяем скорость получения ответа. В случае больше 3 с, тест будет провален.
    duration_threshold = 5
    assert responseA.elapsed.total_seconds() <= duration_threshold
    assert responseB.elapsed.total_seconds() <= duration_threshold


# Отправка эмоджи в чат
def test_sendemoji(api_client):
    data = {"body": "😅", "msgtype": "m.text", "senderId": f"@{api_client.senderid}:matrix.netreportservice.xyz"}

    response = api_client.post_token1(f"{api_client.roomA}%3Amatrix.netreportservice.xyz/send/m.room.message",
                                      json=data)

    assert response.status_code == 200
    assert "The message is invalid" not in response.text

    # Проверка на ключ в ответе json
    assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"

    # Проверяем скорость получения ответа. В случае больше 3 с, тест будет провален.
    duration_threshold = 5
    assert response.elapsed.total_seconds() <= duration_threshold


# Простановка реакции на сообщение
def test_sendreaction(api_client):

    event_id = os.environ.get("EVENT_ID_A")
    if event_id is None:
        responseA = api_client.sendmessages(response_b=False)
        event_id = os.environ.get("EVENT_ID_A")

    data = {
        "m.relates_to": {
            "event_id": event_id,
            "key": "👍",
            "rel_type": "m.annotation"
        }
    }

    response = api_client.post_token1(f"{api_client.roomA}%3Amatrix.netreportservice.xyz/send/m.reaction", json=data)

    assert response.status_code == 200
    assert "The message is invalid" not in response.text

    # Проверка на ключ в ответе json
    assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"

    # Проверяем скорость получения ответа. В случае больше 3 с, тест будет провален.
    duration_threshold = 5
    assert response.elapsed.total_seconds() <= duration_threshold


# Тег игрока в чате token_2
def test_sendtaguser(api_client):
    data = {"body": "@test96 fff", "msgtype": "m.text",
            "senderId": f"@{api_client.senderid}:matrix.netreportservice.xyz"}

    response = api_client.post_token1(f"{api_client.roomA}%3Amatrix.netreportservice.xyz/send/m.room.message",
                                      json=data)

    assert response.status_code == 200
    assert "The message is invalid" not in response.text

    # Проверка на ключ в ответе json
    assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"

    # Проверяем скорость получения ответа. В случае больше 3 с, тест будет провален.
    duration_threshold = 5
    assert response.elapsed.total_seconds() <= duration_threshold


# Отправка разрешенного и запрещенного урла в чат
def test_sendurl(api_client):
    data_url1 = {"body": "google.com", "msgtype": "m.text",
                 "senderId": f"@{api_client.senderid}:matrix.netreportservice.xyz"}
    data_url2 = {"body": "example.com", "msgtype": "m.text",
                 "senderId": "@97884aeb-3618-46e0-bb1f-eeed55db52f1:matrix.netreportservice.xyz"}

    response1 = api_client.post_token1(f"{api_client.roomA}%3Amatrix.netreportservice.xyz/send/m.room.message",
                                       json=data_url1)
    assert response1.status_code == 200
    assert "The message is invalid" not in response1.text

    # Проверка на ключ в ответе json
    assert "event_id" in response1.json(), "The key 'event_id' is not found in the JSON response"

    response2 = api_client.post_token1(f"{api_client.roomA}%3Amatrix.netreportservice.xyz/send/m.room.message",
                                       json=data_url2)
    assert response2.status_code == 200
    assert "The message is invalid" in response2.text

    # Проверка на ключ в ответе json
    assert "event_id" not in response2.json(), "The key 'event_id' is not found in the JSON response"

    # Проверяем скорость получения ответа. В случае больше 3 с, тест будет провален.
    duration_threshold = 5
    assert response1.elapsed.total_seconds() <= duration_threshold
    assert response2.elapsed.total_seconds() <= duration_threshold


# Отправка запрещенного символа в чат
def test_sendnotallowsymbol(api_client):
    data_url1 = {"body": "LOL", "msgtype": "m.text", "senderId": f"@{api_client.senderid}:matrix.netreportservice.xyz"}

    response = api_client.post_token1(f"{api_client.roomA}%3Amatrix.netreportservice.xyz/send/m.room.message",
                                      json=data_url1)
    assert response.status_code == 200
    assert "The message is invalid" in response.text

    # Проверка на ключ в ответе json
    assert "event_id" not in response.json(), "The key 'event_id' is not found in the JSON response"

    # Проверяем скорость получения ответа. В случае больше 3 с, тест будет провален.
    duration_threshold = 5
    assert response.elapsed.total_seconds() <= duration_threshold


# Отправка гифки в чат
def test_sendgif(api_client):
    data = {
        "msgtype": "m.gif",
        "format": "org.matrix.custom.html",
        "senderId": f"@{api_client.senderid}:matrix.netreportservice.xyz",
        "body": "{\"type\":\"GIF\",\"imgUrl\":\"https://media.tenor.com/2w1XsfvQD5kAAAAM/hhgf.gif\"}"
    }

    response = api_client.post_token1(f"{api_client.roomA}%3Amatrix.netreportservice.xyz/send/m.room.message",
                                      json=data)

    assert response.status_code == 200
    error_message = "The message is invalid"
    assert error_message not in response.text, f"Неверное сообщение: '{error_message}'"

    # Проверка на ключ в ответе json
    assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"

    # Проверяем скорость получения ответа. В случае больше 3 с, тест будет провален.
    duration_threshold = 5
    assert response.elapsed.total_seconds() <= duration_threshold



# Простановка жалобы на сообщение, отправленное в функции test_sendmessages
def test_sendcomplaint(api_client):
    event_id = os.environ.get("EVENT_ID_A")
    if event_id is None:
        responseA = api_client.sendmessages(response_b=False)
        event_id = os.environ.get("EVENT_ID_A")

    data = {"eventUid": event_id, "channelUid": f"{api_client.roomA}%3Amatrix.netreportservice.xyz",
            "reason": "trolling"}

    response = api_client.post_token_s(f"api/v1/complaint/send/{api_client.xnodeid}", json=data)

    assert response.status_code == 200


# ROOM B
# Проверка по закреплению сообщения модератором
def test_pinnedmsg(api_client):
    event_id = os.environ.get("EVENT_ID_B")
    if event_id is None:
        responseB = api_client.sendmessages(response_a=False)
        event_id = os.environ.get("EVENT_ID_B")

    data = {"pinned": [{"messageId": event_id, "text": "Text Test"}]}

    response = api_client.post_token_adm(f"{api_client.roomB}%3Amatrix.netreportservice.xyz/send/m.room.pinned_events",
                                         json=data)
    response_json = response.json()
    event_id_pinmsg = response_json.get('event_id')

    if response.status_code == 200:
        os.environ["EVENT_ID_PINMSG"] = event_id_pinmsg

    assert response.status_code == 200

    # Проверка на ключ в ответе json
    assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"


# Проверка по откреплению сообщения модератором
def test_unpinnedmsg(api_client):
    event_id_pinmsg = os.environ.get("EVENT_ID_PINMSG")
    if event_id_pinmsg is None:
        pytest.skip("event_id_pinmsg не был передан из предыдущего теста")

    data = {}

    response = api_client.post_token_adm(f"{api_client.roomB}%3Amatrix.netreportservice.xyz/redact/{event_id_pinmsg}",
                                         json=data)

    assert response.status_code == 200

    # Проверка на ключ в ответе json
    assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"

# Проверка блокировки игрока
def test_blockplayers(api_client):
    # Получаем информацию о том, сколько было забанненых игроков ДО
    getuserbanbefore = api_client.getuserban()
    total_before = getuserbanbefore.json()["pagination"]["total"]

    event_id = os.environ.get("EVENT_ID_B")
    if event_id is None:
        responseB = api_client.sendmessages(response_a=False)
        event_id = os.environ.get("EVENT_ID_B")

    data = {
        "autoBanned": False,
        "nodeUid": api_client.xnodeid,
        "roomUid": api_client.roomB,
        "userUid": f"@{api_client.senderid}",
        "blockedBy": "@a524d297-b434-4957-85fc-ff6afff99e9b:matrix.netreportservice.xyz",
        "message": "Text Test",
        "duration": 3600,
        "messageId": event_id,
        "reason": "harassmentOffensiveLanguage",
        "nodeId": api_client.xnodeid
    }

    url = (
        f"api/v1/synapse/user/ban?"
        f"autoBanned=false&"
        f"nodeUid={quote(api_client.xnodeid)}&"
        f"roomUid={quote(api_client.roomB)}%3Amatrix.netreportservice.xyz&"
        f"userUid={quote(f'@{api_client.senderid}')}%3Amatrix.netreportservice.xyz&"
        f"blockedBy={quote(f'@{api_client.senderid_adm}')}%3Amatrix.netreportservice.xyz&"
        f"message=Text+Test&"
        f"messageId={quote(event_id.encode())}&"
        f"duration=3600&"
        f"reason=harassmentOffensiveLanguage&"
        f"nodeId={quote(api_client.xnodeid)}"
    )

    response = api_client.post_token_s(url, json=data)
    #Делаеим задержку времени, чтобы успел отработать запрос по получению забаненных игроков
    time.sleep(3)
    # Получаем информацию о том, сколько было забанненых игроков ПОСЛЕ
    getuserbanafter = api_client.getuserban()
    total_after = getuserbanafter.json()["pagination"]["total"]

    assert response.status_code == 200

    # Проверяем, что нужный ключ есть в ответе
    assert "total" in getuserbanbefore.json()["pagination"], "The key 'total' is not found in the JSON response before"
    assert "total" in getuserbanafter.json()["pagination"], "The key 'total' is not found in the JSON response after"

    # Проверяем, что забаненных игроков увеличилось на один
    assert total_after == total_before + 1, "The 'total' value did not increase by one"

    # #Проверяем, что заблокированный игрок не может писать в чат
    # response_blockplayer = api_client.sendmessages(response_b=False)
    # assert "event_id" not in response_blockplayer.json(), "The key 'event_id' is found in the JSON response"



# ROOM A
# Проверка работоспособности автобана
def test_checkedspam(api_client):
    data = {"body": "Text Test Spam", "msgtype": "m.text",
            "senderId": f"@{api_client.senderid}:matrix.netreportservice.xyz"}

    for _ in range(51):
        response = api_client.post_token1(f"{api_client.roomA}%3Amatrix.netreportservice.xyz/send/m.room.message",
                                          json=data)
        if response.status_code != 200:
            break
        time.sleep(4)

    assert response.status_code == 500


