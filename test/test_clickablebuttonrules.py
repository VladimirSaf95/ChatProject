from fixture.helper_base import HelperBase
import pytest
import time
import requests


#Проверка отображение правил чата на локали RU и EN
def test_openrules(app):
    helper_base = HelperBase(app)
    test_id = "chat-header-rulesButton"
    selector = f'[data-testid="{test_id}"]'
    # Проверяем, если чат открыт, если нет, то открываем
    if not helper_base.check_chatbutton_existence():
        helper_base.clickchatbutton()
    # Кликаем по селектору иконки правил чата
    helper_base.click_element_by_css_selector(selector)
    # Проверяем, если отображается модальное окно с правилами
    assert helper_base.is_modal_displayed("ReactModal__Content")

    #Проверяем если включена локаль EN, если да, то в модальном окне правил смотрим что тест на анг языке
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
    #Если установлена локаль, отличной от RU, то переключаем на нее
    if not app.is_valid_localation("/ru"):
        app.open_changelocation_ru()
        #Даем время на прогрузку контента страницы
        time.sleep(3)

    # Проверяем если включена локаль RU, если да, то в модальном окне правил смотрим что тест на анг языке
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