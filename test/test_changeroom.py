from fixture.helper_base import HelperBase
import pytest
import time
import allure
import os

@allure.feature("Chat Rooms")
@allure.story("Clicking Chat Room")
@allure.severity(allure.severity_level.CRITICAL)
def test_click_chat_room(app):

    with allure.step("Checking if chat button exists"):
        helper_base = HelperBase(app)
        # Проверяем, если чат открыт, если нет, то открываем
        if not helper_base.check_chatbutton_existence():
            helper_base.clickchatbutton()
            # Даем время для загрузки каналов
            time.sleep(5)

    # Получаем селекторы для комнат A и B
    selectorA = f'[data-test-id-roomitem="chat-carouselRooms-room{app.roomA}:{app.room_second_part}"]'
    selectorB = f'[data-test-id-roomitem="chat-carouselRooms-room{app.roomB}:{app.room_second_part}"]'

    # Получаем элементы для комнаты A
    room_items_A = helper_base.find_elements_by_css_selector(selectorA)

    # Если список пустой, то прерываем тест
    if not room_items_A:
        pytest.fail("Room A items not found or empty")

    with allure.step("Clicking on Room B"):
        # Кликаем на комнату B
        helper_base.click_element_by_css_selector(selectorB)

    with allure.step("Verifying Room B is selected"):
        # Получаем элементы для комнаты B
        room_items_B = helper_base.find_elements_by_css_selector(selectorB)

        # Если список пустой, то прерываем тест
        if not room_items_B:
            pytest.fail("Room B items not found or empty")

        # Проверяем каждый элемент комнаты B
        for item in room_items_B:
            room_id = item.get_attribute('data-test-id-room')
            assert room_id is not None, f"data-test-id-room not found or empty for element with data-test-id-roomitem attribute: {item}"

    with allure.step("Clicking on Room A"):
        # Кликаем на комнату A
        helper_base.click_element_by_css_selector(selectorA)

    with allure.step("Verifying Room A is selected"):
        # Проверяем каждый элемент комнаты A
        for item in room_items_A:
            room_id = item.get_attribute('data-test-id-room')
            assert room_id is not None, f"data-test-id-room not found or empty for element with data-test-id-roomitem attribute: {item}"







