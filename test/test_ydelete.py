from fixture.api_client import APIClient
import pytest
import json
import requests
import time
import os
from urllib.parse import quote

#ROOM B
def test_deletedmsg(api_client):

    event_id = os.environ.get("EVENT_ID_B")

    # Проверка, что event_id был получен в предыдущем тесте
    if event_id is None:
        responseB = api_client.sendmessages(response_a=False)
        event_id = os.environ.get("EVENT_ID_B")

    response = api_client.delete_token_s(f"api/v1/synapse/message/{api_client.roomB}%3Amatrix.netreportservice.xyz/{event_id}")

    assert response.status_code == 200


def test_unblockplayers(api_client):
    #Задержка по времени необходимо для того, чтобы успел отработать запрос по блокировке игрока
    time.sleep(15)
    #Получаем информацию о том, сколько было забанненых игроков ДО
    getuserbanbefore = api_client.getuserban()
    total_before = getuserbanbefore.json()["pagination"]["total"]

    event_id = os.environ.get("EVENT_ID_B")

    # Проверка, что event_id был получен в предыдущем тесте
    if event_id is None:
        responseB = api_client.sendmessages(response_a=False)
        event_id = os.environ.get("EVENT_ID_B")

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
        f"userUid={quote(f'@{api_client.senderid}')}%3Amatrix.netreportservice.xyz&"
        f"roomUid={quote(api_client.roomB)}%3Amatrix.netreportservice.xyz&"
    )

    response = api_client.delete_token_s(url, json=data)
    #Необходима задержка, чтобы успел отработать запрос на получение забаненных юзеров
    time.sleep(3)
    print("URL запроса:", response.url)

    # Проверка кода состояния
    assert response.status_code == 200

    # Получаем информацию о том, сколько было забанненых игроков ПОСЛЕ
    getuserbanafter = api_client.getuserban()
    total_after = getuserbanafter.json()["pagination"]["total"]

    #Проверяем, что нужный ключ есть в ответе
    assert "total" in getuserbanbefore.json()["pagination"], "The key 'total' is not found in the JSON response before"
    assert "total" in getuserbanafter.json()["pagination"], "The key 'total' is not found in the JSON response after"

    # Проверяем, что забаненных игроков уменьшелось на один
    assert total_after == total_before - 1, "The 'total' value did not decrease by one"

    # Проверяем, что заблокированный игрок может писать в чат
    response_unblockplayer = api_client.sendmessages(response_b=False)
    assert "event_id" in response_unblockplayer.json(), "The key 'event_id' is not found in the JSON response"