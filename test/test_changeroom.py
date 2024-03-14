from fixture.helper_base import HelperBase
import pytest


def test_click_chat_room(app):
    helper_base = HelperBase(app)
    # Проверяем, если чат открыт, если нет, то открываем
    if not helper_base.check_chatbutton_existence():
        helper_base.clickchatbutton()

    selectorB = f'[data-test-id-roomitem="chat-carouselRooms-room{app.roomB}"]'
    selectorA = f'[data-test-id-roomitem="chat-carouselRooms-room{app.roomA}"]'

    helper_base.click_element_by_css_selector(selectorB)

    assert helper_base.check_css_selector_existence(
        'data-test-id-room="chat-carouselRooms-room"') and helper_base.check_css_selector_existence(selectorB)

    helper_base.click_element_by_css_selector(selectorA)

    assert helper_base.check_css_selector_existence(
        'data-test-id-room="chat-carouselRooms-room"') and helper_base.check_css_selector_existence(selectorA)