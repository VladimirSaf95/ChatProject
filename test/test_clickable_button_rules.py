from fixture.helper_base import HelperBase
import pytest
import time
import requests
import allure


#Проверка отображение правил чата на локали RU и EN
@allure.feature("Chat Rules")
@allure.story("Opening Chat Rules in Different Locales")
@allure.severity(allure.severity_level.NORMAL)
def test_open_rules_in_different_locales(app):
    helper_base = HelperBase(app)
    test_id = "chat-header-rulesButton"
    selector = f'[data-testid="{test_id}"]'

    with allure.step("Opening chat rules"):
        # Проверяем, если чат открыт, если нет, то открываем
        if not helper_base.check_chatbutton_existence():
            helper_base.clickchatbutton()
        # Кликаем по селектору иконки правил чата
        helper_base.click_element_by_css_selector(selector)
        # Проверяем, если отображается модальное окно с правилами
        assert helper_base.is_modal_displayed("ReactModal__Content")

    with allure.step("Verifying chat rules in English locale"):
        # Проверяем если включена локаль EN
        if app.is_valid_localation("/en"):
            # Находим элемент с текстом "Chat rules" на странице с английским языком
            chat_rules_element_en = helper_base.find_element_by_text("Chat rules")
            if chat_rules_element_en:
                # Получаем текст элемента
                chat_rules_text_en = chat_rules_element_en.text.strip()
                # Проверяем текст
                assert chat_rules_text_en == "Chat rules", "Text does not match 'Правила чата' in EN"
            else:
                print("No element found with text 'Правила чата' on EN page")

    with allure.step("Switching to Russian locale and verifying chat rules"):
        # Проверяем если включена локаль RU, если нет, переключаемся на нее
        if not app.is_valid_localation("/ru"):
            app.open_changelocation_ru()
            # Даем время на прогрузку контента страницы
            time.sleep(3)
        # Проверяем если включена локаль RU
        if app.is_valid_localation("/ru"):
            response = requests.get(app.is_valid_s())
            # Проверяем, что код статуса равен 200
            if response.status_code == 200:
                # Кликаем по селектору иконки правил чата
                helper_base.click_element_by_css_selector(selector)
                # Находим элемент с текстом "Правила чата" на странице с русским языком
                chat_rules_element_ru = helper_base.find_element_by_text("Правила чата")
                if chat_rules_element_ru:
                    # Получаем текст элемента
                    chat_rules_text_ru = chat_rules_element_ru.text.strip()
                    # Проверяем текст
                    assert chat_rules_text_ru == "Правила чата", "Text does not match 'Правила чата' in RU"
                else:
                    print("No element found with text 'Правила чата' on RU page")
            else:
                print("Page not found or unreachable")

#Закрытие модального окна с правилами чата
@allure.feature("Chat Rules")
@allure.story("Closing Chat Rules Modal")
@allure.severity(allure.severity_level.NORMAL)
def test_close_rules_modal(app):
    helper_base = HelperBase(app)
    test_id = "chat-rulesModal-closeButton"
    selector = f'[data-testid="{test_id}"]'
    with allure.step("Checking if test open rules in different locales passed"):
        if helper_base.check_css_selector_existence(selector):
            with allure.step("Click on the selector to close the modal window with chat rules"):
                 # Кликаем по селектору закрытия модального окна с правилами чата
                helper_base.click_element_by_css_selector(selector)

            with allure.step("Asserting modal window is closed"):
                # Проверяем, если не отображается модальное окно с правилами чата
                assert not helper_base.is_modal_displayed("ReactModal__Content")
        else:
            pytest.skip("The rules of chat did not open, skipping this test")