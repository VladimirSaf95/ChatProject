from fixture.helper_base import HelperBase
import pytest

def test_openrules(app):
    helper_base = HelperBase(app)
    #Проверяем, если чат открыт, если нет, то открываем
    if helper_base.check_chatbutton_existence() is False: helper_base.clickchatbutton()
    #Кликаем по селектору икнонки правил чата
    helper_base.click_element_by_css_selector(".hgwQLS")
    #Проверяем, если отображается моадальное окно с правилами
    assert helper_base.is_modal_displayed("ReactModal__Content") is True

def test_closerules(app, request):
    # Проверяем результат выполнения test_openrules
    result_openrules = request.session.testsfailed == 0

    if result_openrules:
        helper_base = HelperBase(app)
        # Кликаем по селектору закрытия правил чата
        helper_base.click_element_by_css_selector(".sc-bypJrT path")
        # Проверяем, если не отображается моадальное окно с правилами
        assert helper_base.is_modal_displayed("ReactModal__Content") is False
    #если test_openrules не был пройден, то пропускаем выполнение данного теста
    else:
        pytest.skip("Не был пройден тест по открытию правил чата")