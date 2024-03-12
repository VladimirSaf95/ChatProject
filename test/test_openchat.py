from fixture.helper_base import HelperBase
import pytest

def test_clickchatbutton(app):
    helper_base = HelperBase(app)
    helper_base.clickchatbutton()
    #Делам проверку по данному селектору, поскольку он отображается при открытом чате
    assert helper_base.check_chatbutton_existence() is True


def test_showdetailschat(app):
    helper_base = HelperBase(app)
    if helper_base.check_chatbutton_existence() is False: helper_base.clickchatbutton()

    selectors = [
        ".sc-ddjGPC", ".sc-dSCufp", ".sc-kAyceB", ".sc-fxwrCY",
        ".sc-jEACwC", ".sc-hIUJlX", ".sc-ggpjZQ",
        "[data-test-id='chat-carouselRooms-roomsWrapper']", ".sc-jnOGJG",
        "[data-testid='carousel-left-icon']", "[data-testid='rooms-list']",
        "#chat-widget-messages-wrapper", ".sc-hTUWRQ", ".jATDSc",
        ".sc-hknOHE", ".sc-JrDLc"
    ]

    for selector in selectors:
        assert helper_base.check_css_selector_existence(selector) is True





