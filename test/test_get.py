from fixture.api_client import APIClient
import pytest
import json
import requests
import os


#ROOM A

#Проверка получение каналов
def test_getchanel(api_client):

    # Отправка GET-запроса
    response = api_client.get(f"{api_client.roomA}%3Amatrix.netreportservice.xyz/state/m.room.power_levels?roomId=", api_client.roomA)
    print("URL запроса:", response.url)

    # Проверка кода состояния
    assert response.status_code == 200
    assert "The message is invalid" not in response.text, "Неверное сообщение: 'The message is invalid'"

#Проверка получение заблокированных игроков
def test_getuserban(api_client):
    response = api_client.getuserban()

    assert response.status_code == 200

    json_response = response.json()

    # Проверка наличия всех параметров
    assert "blockedPlayers" in json_response, "The key 'blockedPlayers' is not found in the JSON response"
    assert "pagination" in json_response, "The key 'pagination' is not found in the JSON response"

    pagination = json_response.get("pagination", {})
    # Проверка наличия параметров внутри pagination
    assert "total" in pagination, "The key 'total' is not found in the 'pagination' section"
    assert "pageCount" in pagination, "The key 'pageCount' is not found in the 'pagination' section"
    assert "pageSize" in pagination, "The key 'pageSize' is not found in the 'pagination' section"
    assert "pageNumber" in pagination, "The key 'pageNumber' is not found in the 'pagination' section"

def test_getchanelmatrix(api_client):
    # Отправка GET-запроса
    response = requests.get(f"https://sandbox.multichat.work/api/v1/correspondence/rooms/{api_client.xnodeid}")

    # Проверка кода состояния
    assert response.status_code == 200

    # Проверка, что в ответе присутствуют ожидаемые значения
    rooms = response.json()

    # Проверка, что ответ содержит как минимум две записи
    assert len(rooms) >= 2, "Expected at least two rooms in the response"

    # Проверка для первой записи
    room_info_1 = rooms[0]

    assert room_info_1.get("default") == True
    assert room_info_1.get("name") == "Room A"
    assert room_info_1.get("matrixUid") == f"{api_client.roomA}:matrix.netreportservice.xyz"
    assert room_info_1.get("order") == 1
    assert "p2Uid" in room_info_1
    assert "avatarPath" in room_info_1

    # Проверка для второй записи
    room_info_2 = rooms[1]

    assert room_info_2.get("default") == False
    assert room_info_2.get("name") == "Room B"
    assert room_info_2.get("matrixUid") == f"{api_client.roomB}:matrix.netreportservice.xyz"
    assert room_info_2.get("order") == 2
    assert "p2Uid" in room_info_2
    assert "avatarPath" in room_info_2


