from fixture.api_client import APIClient
import pytest
import json
import requests
import os
import allure


#ROOM A

# Проверка получение каналов
@allure.feature("Channel Operations")
@allure.story("Checking Channel Retrieval")
@allure.severity(allure.severity_level.CRITICAL)
def test_getchanel(api_client):
    with allure.step("Sending GET request for channels"):
        # Отправка GET-запроса
        response = api_client.get(f"{api_client.roomA}%3Amatrix.netreportservice.xyz/state/m.room.power_levels?roomId=", api_client.roomA)
        print("URL запроса:", response.url)

        with allure.step("Asserting response status code"):
            # Проверка кода состояния
            assert response.status_code == 200, "Response status code is not 200"

        with allure.step("Asserting response content"):
            assert "The message is invalid" not in response.text, "Invalid message found in response"

# Проверка получение заблокированных игроков
@allure.feature("Player Management")
@allure.story("Checking Blocked Players Retrieval")
@allure.severity(allure.severity_level.CRITICAL)
def test_getuserban(api_client):
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

@allure.feature("Channel Operations")
@allure.story("Checking Matrix Channel Retrieval")
@allure.severity(allure.severity_level.NORMAL)
def test_getchanelmatrix(api_client):
    with allure.step("Sending GET request for channels"):
        # Отправка GET-запроса
        response = requests.get(f"https://sandbox.multichat.work/api/v1/correspondence/rooms/{api_client.xnodeid}")

        with allure.step("Asserting response status code"):
            # Проверка кода состояния
            assert response.status_code == 200, "Response status code is not 200"

        with allure.step("Asserting response content"):
            rooms = response.json()

            with allure.step("Asserting minimum two rooms"):
                # Проверка, что ответ содержит как минимум две записи
                assert len(rooms) >= 2, "Expected at least two rooms in the response"

            with allure.step("Asserting room details"):
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


