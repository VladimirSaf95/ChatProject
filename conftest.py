import pytest
from fixture.application import Application
from fixture.api_client import APIClient
import os
import json


@pytest.fixture(scope="session", autouse=True)
def config(request):
    # Фикстура для загрузки конфигурации теста из JSON.
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), request.config.getoption("--target"))
    with open(config_file) as f:
        return json.load(f)

# Фикстура для UI тестов
@pytest.fixture(scope="session", autouse=True)
def app(request, config):
    # Фикстура для инициализации приложения (открытия браузера).
    web_config = config["web"]
    browser = request.config.getoption("--browser")

    app_fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    app_fixture.open_home_page()

    # При необходимости можно добавить код для предварительной настройки приложения.

    yield app_fixture  # Завершение фикстуры.

    # Код для финализации после каждого теста, если необходимо.
    # Например, выход из-под пользователя и закрытие браузера.
    # app_fixture.logout()
    app_fixture.destroy()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="safari")
    parser.addoption("--target", action="store", default="target.json")

# Фикстура для API тестов
@pytest.fixture(scope="session", autouse=True)
def api_client(request, config):
    # Фикстура для работы с API.
    api_config = config["api"]
    api_fixture = APIClient(base_url_api=api_config['baseUrl'], token_1=api_config['token_1'], token_adm=api_config['token_adm'], token_s=api_config['token_s'],roomA=api_config['roomA'], roomB=api_config['roomB'], xnodeid=api_config['X-Node-Id'], senderid=api_config['senderId'],
                            senderid_adm=api_config['senderId_adm'])

    # При необходимости можно добавить код для предварительной настройки API.

    yield api_fixture  # Завершение фикстуры.

    # Код для финализации после каждого теста, если необходимо
