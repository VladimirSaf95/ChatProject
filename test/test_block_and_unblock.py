import os
import time
from urllib.parse import quote
import pytest
import allure

from fixture.api_client import APIClient

# Проверка получение заблокированных игроков
@allure.feature("Player Management")
@allure.story("Checking Blocked Players Retrieval")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_user_ban(api_client):
    with allure.step("Sending GET request for blocked players"):
        response = api_client.getuserban()

        with allure.step("Asserting response status code"):
            assert response.status_code == 200, "Response status code is not 200"

        with allure.step("Asserting JSON content"):
            json_response = response.json()

            assert "blockedPlayers" in json_response, "The key 'blockedPlayers' is not found in the JSON response"
            assert "pagination" in json_response, "The key 'pagination' is not found in the JSON response"

            pagination = json_response.get("pagination", {})
            assert "total" in pagination, "The key 'total' is not found in the 'pagination' section"
            assert "pageCount" in pagination, "The key 'pageCount' is not found in the 'pagination' section"
            assert "pageSize" in pagination, "The key 'pageSize' is not found in the 'pagination' section"
            assert "pageNumber" in pagination, "The key 'pageNumber' is not found in the 'pagination' section"


# ROOM B
# Проверка блокировки игрока
@allure.feature("Player Blocking")
@allure.story("Player Blocking Test")
@allure.severity(allure.severity_level.BLOCKER)
def test_block_players(api_client):
    with allure.step("Getting information about banned players before the test"):
        getuserbanbefore = api_client.getuserban()
        total_before = getuserbanbefore.json()["pagination"]["total"]

    with allure.step("Sending message and blocking player"):
        event_id = os.environ.get("EVENT_ID_B")
        if event_id is None:
            responseB = api_client.sendmessages(response_a=False)
            event_id = os.environ.get("EVENT_ID_B")

        data = {
            "autoBanned": False,
            "nodeUid": api_client.xnodeid,
            "roomUid": api_client.roomB,
            "userUid": f"@{api_client.senderid}",
            "blockedBy": f"@a524d297-b434-4957-85fc-ff6afff99e9b:{api_client.room_second_part}",
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
            f"roomUid={quote(api_client.roomB)}%3A{api_client.room_second_part}&"
            f"userUid={quote(f'@{api_client.senderid}')}%3A{api_client.room_second_part}&"
            f"blockedBy={quote(f'@{api_client.senderid_adm}')}%3A{api_client.room_second_part}&"
            f"message=Text+Test&"
            f"messageId={quote(event_id.encode())}&"
            f"duration=3600&"
            f"reason=harassmentOffensiveLanguage&"
            f"nodeId={quote(api_client.xnodeid)}"
        )

        response = api_client.post_token_s(url, json=data)
        time.sleep(3)

    with allure.step("Getting information about banned players after the test"):
        getuserbanafter = api_client.getuserban()
        total_after = getuserbanafter.json()["pagination"]["total"]

    with allure.step("Verifying response status code"):
        assert response.status_code == 200

    with allure.step("Verifying 'total' key in response JSON before and after"):
        assert "total" in getuserbanbefore.json()["pagination"], "The key 'total' is not found in the JSON response before"
        assert "total" in getuserbanafter.json()["pagination"], "The key 'total' is not found in the JSON response after"

    with allure.step("Verifying the increase in banned players count"):
        assert total_after == total_before + 1, "The 'total' value did not increase by one"

    # #Проверяем, что заблокированный игрок не может писать в чат
    # response_blockplayer = api_client.sendmessages(response_b=False)
    # assert "event_id" not in response_blockplayer.json(), "The key 'event_id' is found in the JSON response"


@allure.feature("User Management")
@allure.story("Unblocking Players")
@allure.severity(allure.severity_level.CRITICAL)
def test_unblock_players(api_client):
    with allure.step("Waiting for previous operations to complete"):
        # Задержка по времени необходимо для того, чтобы успел отработать запрос по блокировке игрока
        time.sleep(15)

    with allure.step("Fetching information about blocked players before unblocking"):
        # Получаем информацию о том, сколько было забанненых игроков ДО
        getuserbanbefore = api_client.getuserban()
        total_before = getuserbanbefore.json()["pagination"]["total"]

    with allure.step("Checking if event_id is available"):
        event_id = os.environ.get("EVENT_ID_B")

        # Проверка, что event_id был получен в предыдущем тесте
        if event_id is None:
            responseB = api_client.sendmessages(response_a=False)
            event_id = os.environ.get("EVENT_ID_B")

    with allure.step("Preparing data for unblocking user"):
        # Подготовка данных для POST-запроса
        data = {
            "nodeUid": api_client.xnodeid,
            "roomUid": api_client.roomB,
            "userUid": f"@{api_client.senderid}"
        }

        # Используйте quote для каждого параметра, который требует URL-кодирования
        url = (
            f"api/v1/synapse/user/ban?"
            f"nodeUid={quote(api_client.xnodeid)}&"
            f"userUid={quote(f'@{api_client.senderid}')}%3A{api_client.room_second_part}&"
            f"roomUid={quote(api_client.roomB)}%3A{api_client.room_second_part}&"
        )

    with allure.step("Sending request to unblock user"):
        response = api_client.delete_token_s(url, json=data)
        # Необходима задержка, чтобы успел отработать запрос на получение забаненных юзеров
        time.sleep(3)
        print("URL запроса:", response.url)

    with allure.step("Asserting response status code"):
        assert response.status_code == 200, "Response status code is not 200"

    with allure.step("Fetching information about blocked players after unblocking"):
        # Получаем информацию о том, сколько было забанненых игроков ПОСЛЕ
        getuserbanafter = api_client.getuserban()
        total_after = getuserbanafter.json()["pagination"]["total"]

    with allure.step("Asserting response content"):
        # Проверка, что нужный ключ есть в ответе
        assert "total" in getuserbanbefore.json()["pagination"], "The key 'total' is not found in the JSON response before"
        assert "total" in getuserbanafter.json()["pagination"], "The key 'total' is not found in the JSON response after"

        # Проверка, что забаненных игроков уменьшилось на один
        assert total_after == total_before - 1, "The 'total' value did not decrease by one"

    with allure.step("Sending message to verify unblocked player can write in chat"):
        # Проверяем, что заблокированный игрок может писать в чат
        response_unblockplayer = api_client.sendmessages(response_b=False)
        assert "event_id" in response_unblockplayer.json(), "The key 'event_id' is not found in the JSON response"