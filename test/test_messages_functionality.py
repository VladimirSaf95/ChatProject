import os
import time
import pytest
import allure

from fixture.api_client import APIClient


# ROOM A
# Отправка текстового сообщения в чат
@allure.feature("Sending Messages")
@allure.story("Sending Text Messages")
@allure.severity(allure.severity_level.CRITICAL)
def test_send_messages(api_client):
    with allure.step("Sending messages and checking response"):
        responseA, responseB = api_client.sendmessages()

        with allure.step("Check response code for message A"):
            assert responseA.status_code == 200, "Response status code is not 200"

        with allure.step("Check for invalid message in response A"):
            assert "The message is invalid" not in responseA.text, "Invalid message found in response A"

        with allure.step("Check response code for message B"):
            assert responseB.status_code == 200, "Response status code is not 200"

        with allure.step("Check for invalid message in response B"):
            assert "The message is invalid" not in responseB.text, "Invalid message found in response B"

        with allure.step("Check for 'event_id' in JSON response A"):
            assert "event_id" in responseA.json(), "The key 'event_id' is not found in the JSON response A"

        with allure.step("Check for 'event_id' in JSON response B"):
            assert "event_id" in responseB.json(), "The key 'event_id' is not found in the JSON response B"

        with allure.step("Check response time for message A"):
            duration_threshold = 5
            assert responseA.elapsed.total_seconds() <= duration_threshold, "Response time for message A exceeds threshold"

        with allure.step("Check response time for message B"):
            duration_threshold = 5
            assert responseB.elapsed.total_seconds() <= duration_threshold, "Response time for message B exceeds threshold"


# Отправка эмоджи в чат
@allure.feature("Sending Messages")
@allure.story("Sending Emoji")
@allure.severity(allure.severity_level.NORMAL)
def test_send_emoji(api_client):
    with allure.step("Sending emoji and checking response"):
        data = {"body": "😅", "msgtype": "m.text", "senderId": f"@{api_client.senderid}:{api_client.room_second_part}"}

        response = api_client.post_token1(f"{api_client.roomA}%3A{api_client.room_second_part}/send/m.room.message",
                                          json=data)

        with allure.step("Check response code"):
            assert response.status_code == 200, "Response status code is not 200"

        with allure.step("Check for invalid message in response"):
            assert "The message is invalid" not in response.text, "Invalid message found in response"

        with allure.step("Check for 'event_id' in JSON response"):
            assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"

        with allure.step("Check response time"):
            duration_threshold = 5
            assert response.elapsed.total_seconds() <= duration_threshold, "Response time exceeds threshold"


# Простановка реакции на сообщение
@allure.feature("Reaction to Message")
@allure.story("Setting reaction")
@allure.severity(allure.severity_level.NORMAL)
def test_send_reaction(api_client):
    with allure.step("Setting reaction on message"):
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

        response = api_client.post_token1(f"{api_client.roomA}%3A{api_client.room_second_part}/send/m.reaction",
                                          json=data)

        with allure.step("Check response code"):
            assert response.status_code == 200, "Response status code is not 200"

        with allure.step("Check for invalid message in response"):
            assert "The message is invalid" not in response.text, "Invalid message found in response"

        with allure.step("Check for 'event_id' in JSON response"):
            assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"

        with allure.step("Check response time"):
            duration_threshold = 5
            assert response.elapsed.total_seconds() <= duration_threshold, "Response time exceeds threshold"

# Тег игрока в чате
@allure.feature("Tagging Players")
@allure.story("Tagging player in chat")
@allure.severity(allure.severity_level.NORMAL)
def test_tag_user(api_client):
    with allure.step("Tagging player in chat"):
        data = {"body": "@test96 fff", "msgtype": "m.text",
                "senderId": f"@{api_client.senderid}:{api_client.room_second_part}"}

        response = api_client.post_token1(f"{api_client.roomA}%3A{api_client.room_second_part}/send/m.room.message",
                                          json=data)

        with allure.step("Check response code"):
            assert response.status_code == 200, "Response status code is not 200"

        with allure.step("Check for invalid message in response"):
            assert "The message is invalid" not in response.text, "Invalid message found in response"

        with allure.step("Check for 'event_id' in JSON response"):
            assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"

        with allure.step("Check response time"):
            duration_threshold = 5
            assert response.elapsed.total_seconds() <= duration_threshold, "Response time exceeds threshold"


# Отправка разрешенного и запрещенного урла в чат
@allure.feature("Sending URLs")
@allure.story("Sending Allowed and Disallowed URLs")
@allure.severity(allure.severity_level.NORMAL)
def test_send_url(api_client):
    with allure.step("Sending allowed URL"):
        data_url1 = {"body": "google.com", "msgtype": "m.text",
                     "senderId": f"@{api_client.senderid}:{api_client.room_second_part}"}

        response1 = api_client.post_token1(f"{api_client.roomA}%3A{api_client.room_second_part}/send/m.room.message",
                                           json=data_url1)

        with allure.step("Asserting response for allowed URL"):
            assert response1.status_code == 200, "Response status code is not 200"
            assert "The message is invalid" not in response1.text, "Invalid message found in response"
            assert "event_id" in response1.json(), "The key 'event_id' is not found in the JSON response"

            duration_threshold = 5
            assert response1.elapsed.total_seconds() <= duration_threshold, "Response time exceeds threshold"

    with allure.step("Sending disallowed URL"):
        data_url2 = {"body": "example.com", "msgtype": "m.text",
                     "senderId": f"@{api_client.senderid}:{api_client.room_second_part}"}

        response2 = api_client.post_token1(f"{api_client.roomA}%3A{api_client.room_second_part}/send/m.room.message",
                                           json=data_url2)

        with allure.step("Asserting response for disallowed URL"):
            assert response2.status_code == 200, "Response status code is not 200"
            assert "The message is invalid" in response2.text, "Valid message found in response"
            assert "event_id" not in response2.json(), "The key 'event_id' is found in the JSON response"

            duration_threshold = 5
            assert response2.elapsed.total_seconds() <= duration_threshold, "Response time exceeds threshold"

# Отправка запрещенного символа в чат
@allure.feature("Sending Symbols")
@allure.story("Sending Disallowed Symbol")
@allure.severity(allure.severity_level.NORMAL)
def test_send_not_allow_symbol(api_client):
    with allure.step("Sending disallowed symbol"):
        data_url1 = {"body": "LOL", "msgtype": "m.text",
                     "senderId": f"@{api_client.senderid}:{api_client.room_second_part}"}

        response = api_client.post_token1(f"{api_client.roomA}%3A{api_client.room_second_part}/send/m.room.message",
                                          json=data_url1)

        with allure.step("Asserting response for disallowed symbol"):
            assert response.status_code == 200, "Response status code is not 200"
            assert "The message is invalid" in response.text, "Valid message found in response"
            assert "event_id" not in response.json(), "The key 'event_id' is found in the JSON response"

            duration_threshold = 5
            assert response.elapsed.total_seconds() <= duration_threshold, "Response time exceeds threshold"


# Отправка гифки в чат
@allure.feature("Sending GIFs")
@allure.story("Sending GIF in Chat")
@allure.severity(allure.severity_level.NORMAL)
def test_send_gif(api_client):
    data = {
        "msgtype": "m.gif",
        "format": "org.matrix.custom.html",
        "senderId": f"@{api_client.senderid}:{api_client.room_second_part}",
        "body": "{\"type\":\"GIF\",\"imgUrl\":\"https://media.tenor.com/2w1XsfvQD5kAAAAM/hhgf.gif\"}"
    }

    with allure.step("Sending GIF message"):
        response = api_client.post_token1(f"{api_client.roomA}%3A{api_client.room_second_part}/send/m.room.message",
                                          json=data)

    with allure.step("Asserting response status code"):
        assert response.status_code == 200, "Response status code is not 200"

    with allure.step("Asserting response text"):
        error_message = "The message is invalid"
        assert error_message not in response.text, f"Invalid message found in response: '{error_message}'"

    with allure.step("Asserting 'event_id' key in JSON response"):
        assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"

    with allure.step("Asserting response time"):
        duration_threshold = 5
        assert response.elapsed.total_seconds() <= duration_threshold, "Response time exceeds threshold"


# Простановка жалобы на сообщение
@allure.feature("Sending Complaints")
@allure.story("Filing Complaint on Message")
@allure.severity(allure.severity_level.CRITICAL)
def test_send_complaint(api_client):
    event_id = os.environ.get("EVENT_ID_A")
    if event_id is None:
        responseA = api_client.sendmessages(response_b=False)
        event_id = os.environ.get("EVENT_ID_A")

    data = {"eventUid": event_id, "channelUid": f"{api_client.roomA}%3A{api_client.room_second_part}",
            "reason": "trolling"}

    with allure.step("Filing complaint on message"):
        response = api_client.post_token_s(f"api/v1/complaint/send/{api_client.xnodeid}", json=data)

    with allure.step("Asserting response status code"):
        assert response.status_code == 200, "Response status code is not 200"

# ROOM B
# Проверка по закреплению сообщения модератором
@allure.feature("Message Pinning")
@allure.story("Message Pinning by Moderator")
@allure.severity(allure.severity_level.NORMAL)
def test_pinned_msg(api_client):
    with allure.step("Sending message"):
        event_id = os.environ.get("EVENT_ID_B")
        if event_id is None:
            responseB = api_client.sendmessages(response_a=False)
            event_id = os.environ.get("EVENT_ID_B")

    with allure.step("Pinning message"):
        data = {"pinned": [{"messageId": event_id, "text": "Text Test"}]}
        response = api_client.post_token_adm(f"{api_client.roomB}%3A{api_client.room_second_part}/send/m.room.pinned_events",
                                             json=data)
        response_json = response.json()
        event_id_pinmsg = response_json.get('event_id')
        if response.status_code == 200:
            os.environ["EVENT_ID_PINMSG"] = event_id_pinmsg

    with allure.step("Verifying response status code"):
        assert response.status_code == 200

    with allure.step("Verifying event_id in response JSON"):
        assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"


# Проверка по откреплению сообщения модератором
@allure.feature("Message Unpinning")
@allure.story("Message Unpinning by Moderator")
@allure.severity(allure.severity_level.NORMAL)
def test_unpinned_msg(api_client):
    with allure.step("Getting pinned message ID"):
        event_id_pinmsg = os.environ.get("EVENT_ID_PINMSG")
        if event_id_pinmsg is None:
            pytest.skip("event_id_pinmsg was not passed from the previous test")

    with allure.step("Unpinning the message"):
        data = {}
        response = api_client.post_token_adm(f"{api_client.roomB}%3A{api_client.room_second_part}/redact/{event_id_pinmsg}",
                                             json=data)

    with allure.step("Verifying response status code"):
        assert response.status_code == 200

    with allure.step("Verifying event_id in response JSON"):
        assert "event_id" in response.json(), "The key 'event_id' is not found in the JSON response"

# ROOM A
# Проверка работоспособности автобана
@allure.feature("Spam Checking")
@allure.story("Spam Checking Test")
@allure.severity(allure.severity_level.CRITICAL)
def test_checked_spam(api_client):
    with allure.step("Sending spam messages"):
        data = {"body": "Text Test Spam", "msgtype": "m.text",
                "senderId": f"@{api_client.senderid}:{api_client.room_second_part}"}

        for _ in range(4):
            response = api_client.post_token1(f"{api_client.roomA}%3A{api_client.room_second_part}/send/m.room.message",
                                              json=data)
            if response.status_code != 200:
                break
            time.sleep(4)

    with allure.step("Verifying response status code"):
        assert response.status_code == 500

#ROOM B
@allure.feature("Message Operations")
@allure.story("Deleting Messages")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_dmsg(api_client):
    with allure.step("Checking if event_id is available"):
        event_id = os.environ.get("EVENT_ID_B")

        # Проверка, что event_id был получен в предыдущем тесте
        if event_id is None:
            responseB = api_client.sendmessages(response_a=False)
            event_id = os.environ.get("EVENT_ID_B")

    with allure.step("Sending DELETE request to delete message"):
        response = api_client.delete_token_s(f"api/v1/synapse/message/{api_client.roomB}%3A{api_client.room_second_part}/{event_id}")

        with allure.step("Asserting response status code"):
            assert response.status_code == 200, "Response status code is not 200"
