from fixture.helper_base import HelperBase
import pytest
import time

def test_openrules(app):
    helper_base = HelperBase(app)

    test_id = "chat-chatButton-openButton"
    selector_button = f'[data-testid="{test_id}"]'

    if helper_base.check_css_selector_existence(selector_button) is False:
        app.open_home_page()
        helper_base.clickchatbuttom()

    helper_base.click_element_by_css_selector(".hKXQyY")

    assert helper_base.is_modal_displayed("ReactModal__Content") is True
    return True

def test_closerules(app):

    if test_openrules:
        helper_base = HelperBase(app)

        test_id = "chat-chatButton-openButton"
        selector_button = f'[data-testid="{test_id}"]'

        if helper_base.check_css_selector_existence(selector_button) is False:
            app.open_home_page()
            helper_base.clickchatbuttom()


        helper_base.click_element_by_css_selector(".sc-bypJrT path")

        assert helper_base.is_modal_displayed("ReactModal__Content") is False

    else:
        pytest.skip("Не был пройден тест по открытию правил чата")