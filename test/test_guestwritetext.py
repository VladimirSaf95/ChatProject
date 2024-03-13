from fixture.helper_base import HelperBase
import pytest

#Проверка под гостем, что при клике на поле ввода сообщения открывается страница авторизации
def test_click_chat_button_close(app):
    helper_base = HelperBase(app)
    #Определяем селектор для нажатия по полю ввода сообщение
    selector = ".sc-hknOHE"
    #Если чат не был открыт, открываем его
    if helper_base.check_chatbutton_existence() is False:
        helper_base.clickchatbutton()
    #Кликаем по селектору
    helper_base.click_element_by_css_selector(selector)
    #Производим проверку, что открылась страница авторизации
    assert app.is_valid_s() == app.checkurl("/user/login")
