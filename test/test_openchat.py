from fixture.helper_base import HelperBase
import pytest
import time

#Проверка на открытие чата
def test_clickchatbutton(app):
    helper_base = HelperBase(app)
    #Кликаем по кнопке чата
    helper_base.clickchatbutton()
    #Делам проверку если чат был открыт
    assert helper_base.check_chatbutton_existence() is True

#Проверка на отображение деталей чата
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
    #Проверяем существование селектором различным эелементов у открытого чата
    for selector in selectors:
        assert helper_base.check_css_selector_existence(selector) is True





