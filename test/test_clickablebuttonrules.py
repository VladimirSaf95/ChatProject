from fixture.helper_base import HelperBase
import pytest

def test_openrules(app):
    helper_base = HelperBase(app)

    if helper_base.check_chatbutton_existence() is False: helper_base.clickchatbutton()
    helper_base.click_element_by_css_selector(".hgwQLS")
    assert helper_base.is_modal_displayed("ReactModal__Content") is True

def test_closerules(app, request):
    # Проверяем результат выполнения test_openrules
    result_openrules = request.session.testsfailed == 0

    if result_openrules:
        helper_base = HelperBase(app)

        if helper_base.check_chatbutton_existence() is False: helper_base.clickchatbutton()
        helper_base.click_element_by_css_selector(".sc-bypJrT path")
        assert helper_base.is_modal_displayed("ReactModal__Content") is False

    else:
        pytest.skip("Не был пройден тест по открытию правил чата")