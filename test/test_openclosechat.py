from fixture.helper_base import HelperBase
import pytest
import time
import allure

#Проверка на открытие чата
@allure.feature("Chat Functionality")
@allure.story("Clicking Chat Button")
@allure.severity(allure.severity_level.BLOCKER)
def test_clickchatbutton(app):
    helper_base = HelperBase(app)

    with allure.step("Clicking on the chat button"):
        # Кликаем по кнопке чата
        helper_base.clickchatbutton()

    with allure.step("Asserting chat button existence"):
        # Делаем проверку если чат был открыт
        assert helper_base.check_chatbutton_existence() is True

#Проверка на отображение деталей чата
@allure.feature("Chat Functionality")
@allure.story("Showing Chat Details")
@allure.severity(allure.severity_level.CRITICAL)
def test_showdetailschat(app):
    helper_base = HelperBase(app)
    # Проверяем, если чат открыт, если нет, то открываем
    if helper_base.check_chatbutton_existence() is False:
        helper_base.clickchatbutton()

    selectors = [
        "[data-testid='chat-header-closeButton']", "[data-testid='chat-header-rulesButton']", "[data-testid='gif-icon']",
        "[data-test-id='chat-carouselRooms-roomsWrapper']", "[data-testid='emoji-icon']",
        "[data-testid='carousel-left-icon']", "[data-testid='rooms-list']",
        "#chat-widget-messages-wrapper"
    ]

    with allure.step("Checking existence of chat details"):
        # Проверяем существование селектором различных элементов у открытого чата
        for selector in selectors:
            assert helper_base.check_css_selector_existence(selector) is True

#Проверка на закрытие чата
@allure.feature("Chat Functionality")
@allure.story("Clicking Chat Button to Close")
@allure.severity(allure.severity_level.CRITICAL)
def test_click_chat_button_close(app):
    helper_base = HelperBase(app)
    test_id = "chat-header-closeButton"
    selector = f'[data-testid="{test_id}"]'

    with allure.step("Checking if chat is open"):
        # Проверка, если чат открыт
        chat_open = helper_base.check_chatbutton_existence()
        assert chat_open is True, "Chat is not open"

    with allure.step("Clicking on the chat close button"):
        # Кликаем на иконку закрытия чата
        helper_base.click_element_by_css_selector(selector)

    with allure.step("Verifying that the chat is closed"):
        # Проверяем, что чат закрылся
        chat_closed = helper_base.check_chatbutton_existence()
        assert chat_closed is False, "Chat is still open after clicking close button"

    # Если чат не был открыт, то пропускаем тест
    if not chat_open:
        pytest.skip("The test for opening the chat room was not run in advance")





