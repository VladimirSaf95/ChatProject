from fixture.helper_base import HelperBase
import pytest

def test_click_chat_button_close(app):
    helper_base = HelperBase(app)
    if helper_base.check_chatbutton_existence() is True:
        app.open_home_page()
        helper_base.clickchatbutton()

    helper_base.click_element_by_css_selector(".hknOHE")
    assert helper_base.check_chatbutton_existence() is True


def test_showdetails_chat_after_close(app):
    helper_base = HelperBase(app)

    if helper_base.check_chatbutton_existence() is True:
        app.open_home_page()
        helper_base.clickchatbutton()

    selectors = [
        ".sc-ddjGPC", ".sc-dSCufp", ".sc-kAyceB", ".sc-fxwrCY",
        ".sc-jEACwC", ".sc-hIUJlX", ".sc-ggpjZQ",
        "[data-test-id='chat-carouselRooms-roomsWrapper']", ".sc-jnOGJG",
        "[data-testid='carousel-left-icon']", "[data-testid='rooms-list']",
        "#chat-widget-messages-wrapper", ".sc-hTUWRQ", ".jATDSc",
        ".sc-hknOHE", ".sc-JrDLc"
    ]

    for selector in selectors:
        assert helper_base.check_css_selector_existence(selector) is False