from fixture.helper_base import HelperBase
import pytest
import time
import allure

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

    with allure.step("Clicking on Room B"):
        # Определяем селекторы для двух каналов, по которым будем кликать
        selectorB = f'[data-test-id-roomitem="chat-carouselRooms-room{app.roomB}:matrix.netreportservice.xyz"]'
        helper_base.click_element_by_css_selector(selectorB)

    with allure.step("Verifying Room B is selected"):
        # Определяем в каком селекторе будем искать нужный нам атрибут
        room_items = helper_base.find_elements_by_css_selector(selectorB)
        # Проходим циклом по нужному нам селектору, чтобы найти нужный нам атрибут
        for item in room_items:
            # Проверяем наличие атрибута 'data-test-id-room' у текущего элемента
            room_id = item.get_attribute('data-test-id-room')
            assert room_id is not None, f"data-test-id-room not found or empty for element with data-test-id-roomitem attribute: {item}"

    with allure.step("Clicking on Room A"):
        # Выполняем аналогичные действия для канала A
        selectorA = f'[data-test-id-roomitem="chat-carouselRooms-room{app.roomA}:matrix.netreportservice.xyz"]'
        helper_base.click_element_by_css_selector(selectorA)

    with allure.step("Verifying Room A is selected"):
        room_items_A = helper_base.find_elements_by_css_selector(selectorA)
        for item in room_items_A:
            # Проверяем наличие атрибута 'data-test-id-room' у текущего элемента
            room_id = item.get_attribute('data-test-id-room')
            assert room_id is not None, f"data-test-id-room not found or empty for element with data-test-id-roomitem attribute: {item}"






