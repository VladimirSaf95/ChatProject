from fixture.helper_base import HelperBase
import pytest
import allure

#Проверка под гостем, что при клике на поле ввода сообщения открывается страница авторизации
@allure.feature("Guest Chat Functionality")
@allure.story("Writing Text as Guest")
@allure.severity(allure.severity_level.NORMAL)
def test_guest_write_text(app):
    helper_base = HelperBase(app)
    # Если чат не был открыт, открываем его
    if not helper_base.check_chatbutton_existence():
        helper_base.clickchatbutton()

    with allure.step("Clicking on the chat input field"):
        # Определяем селектор для нажатия по полю ввода сообщения
        selector = ".sc-hknOHE"
        helper_base.click_element_by_css_selector(selector)

    with allure.step("Asserting redirection to login page"):
        # Производим проверку, что открылась страница авторизации
        assert app.check_current_url() == True