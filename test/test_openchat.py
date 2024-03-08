from fixture.helper_base import HelperBase
import pytest

def test_clickchatbuttom(app):
    helper_base= HelperBase(app)
    app.open_home_page()
    test_id = "chat-chatButton-openButton"
    selector = f'[data-testid="{test_id}"]'
    helper_base.click_element_by_css_selector(selector)
    assert helper_base.check_css_selector_existence(selector) is True


def test_showdetailschat(app):
    helper_base = HelperBase(app)

    test_id = "chat-chatButton-openButton"
    selector_button = f'[data-testid="{test_id}"]'

    if helper_base.check_css_selector_existence(selector_button) is False:
        app.open_home_page()
        helper_base.clickchatbuttom()

    selectors = [
        ".sc-ddjGPC", ".sc-dSCufp", ".sc-kAyceB", ".sc-fxwrCY",
        ".sc-jEACwC", ".sc-hIUJlX", ".sc-ggpjZQ",
        "[data-test-id='chat-carouselRooms-roomsWrapper']", ".sc-jnOGJG",
        "[data-testid='carousel-left-icon']", "[data-testid='rooms-list']",
        "#chat-widget-messages-wrapper", ".sc-hTUWRQ", ".jATDSc",
        ".sc-hknOHE", ".fGzvHm", ".sc-JrDLc"
    ]

    for selector in selectors:
        assert helper_base.check_css_selector_existence(selector) is True





