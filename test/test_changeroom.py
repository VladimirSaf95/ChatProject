from fixture.helper_base import HelperBase
import pytest
import time

def test_click_chat_room(app):
    helper_base = HelperBase(app)
    # Проверяем, если чат открыт, если нет, то открываем
    if not helper_base.check_chatbutton_existence():
        helper_base.clickchatbutton()
        time.sleep(5)

    selectorB = f'[data-test-id-roomitem="chat-carouselRooms-room{app.roomB}:matrix.netreportservice.xyz"]'
    selectorA = f'[data-test-id-roomitem="chat-carouselRooms-room{app.roomA}:matrix.netreportservice.xyz"]'

    helper_base.click_element_by_css_selector(selectorB)

    room_items = helper_base.find_elements_by_css_selector(selectorB)

    for item in room_items:
        # Проверяем наличие атрибута 'data-test-id-room' у текущего элемента
        room_id = item.get_attribute('data-test-id-room')
        assert room_id is not None, f"data-test-id-room не найден или пустой для элемента с атрибутом data-test-id-roomitem: {item}"

    helper_base.click_element_by_css_selector(selectorA)
    room_items_A = helper_base.find_elements_by_css_selector(selectorA)

    for item in room_items_A:
        # Проверяем наличие атрибута 'data-test-id-room' у текущего элемента
        room_id = item.get_attribute('data-test-id-room')
        assert room_id is not None and room_id != '', f"data-test-id-room не найден или пустой для элемента с атрибутом data-test-id-roomitem: {item}"
