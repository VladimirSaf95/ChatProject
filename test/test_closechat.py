from fixture.helper_base import HelperBase
import pytest

def test_click_chat_button_close(app):
    helper_base = HelperBase(app)
    test_id = "chat-header-closeButton"
    selector = f'[data-testid="{test_id}"]'
    # Проверка если чат открыт
    if helper_base.check_chatbutton_existence() is True:
        #Кликаем на иконку закрытие чата
        helper_base.click_element_by_css_selector(selector)
        #Проверяем что чат закрылся
        assert helper_base.check_chatbutton_existence() is False
    #Если чат не был открыт, то пропускаем тест
    else:
        pytest.skip("The test for opening the chat room was not run in advance")
