import pytest
from fixture.application import Application
from fixture.api_client import APIClient
from fixture.authorization import Authorization
import os
import json


@pytest.fixture(scope="session", autouse=True)
def config(request):

    # Проверяем, запущен ли тест на GitHub Actions
    if os.getenv("GITHUB_ACTIONS"):
        # Если да, загружаем данные из переменных окружения
        return {
            "web": {
                "baseUrl": os.getenv("BASE_URL")
            },
            "api": {
                "baseUrl": os.getenv("API_BASE_URL"),
                "ssoUrl": os.getenv("SSO_URL"),
                "X-Node-Id": os.getenv("X_NODE_ID"),
                "Login_player": os.getenv("LOGIN_PLAYER"),
                "Password_player": os.getenv("PASSWORD_PLAYER"),
                "Login_admin": os.getenv("LOGIN_ADMIN"),
                "Password_admin": os.getenv("PASSWORD_ADMIN")
            }
        }
    else:
        # Если нет, загружаем данные из файла target.json
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), request.config.getoption("--target"))
        with open(config_file) as f:
            return json.load(f)

# Определяем фикстуру для инициализации Authorization
@pytest.fixture(scope="session", autouse=True)
def init_authorization(request, config):
    # Получаем необходимые данные из конфигурации
    api_config = config["api"]
    web_config = config["web"]

    # Создаем экземпляр класса Authorization
    auth = Authorization(base_url=web_config['baseUrl'], api_base_url=api_config['baseUrl'], xnodeid=api_config['X-Node-Id'], sso_url=api_config['ssoUrl'])

    # Получение токена API и Matrix для игрока
    player_api_token = auth.get_api_token(api_config['Login_player'], api_config['Password_player'])
    player_access_token, player_user_id = auth.get_matrix_token(player_api_token)


    # Получение токена API и Matrix для администратора
    admin_api_token = auth.get_api_token(api_config['Login_admin'], api_config['Password_admin'])
    admin_access_token, admin_user_id = auth.get_matrix_token(admin_api_token)

    # Получение идентификаторов комнат
    roomA, room_second_part, roomB = auth.get_rooms_id()
    
    print(f'Значения {player_access_token, player_user_id, admin_access_token, admin_user_id,  roomA, room_second_part, roomB}')
    # Возвращаем кортеж с объектом Authorization и идентификаторами комнат, чтобы его можно было использовать в тестах
    return auth, player_access_token, player_user_id, admin_access_token, admin_user_id,  roomA, room_second_part, roomB, admin_api_token


# Фикстура для API тестов
@pytest.fixture(scope="session", autouse=True)
def api_client(request, config, init_authorization):
    # Фикстура для работы с API.
    api_config = config["api"]
    auth, player_access_token, player_user_id, admin_access_token, admin_user_id,  roomA, room_second_part, roomB, admin_api_token = init_authorization

    api_fixture = APIClient(
        base_url_api=api_config['baseUrl'],
        token_1=player_access_token,
        token_s=admin_api_token,
        token_adm=admin_access_token,
        roomA=roomA,
        room_second_part=room_second_part,
        roomB=roomB,
        xnodeid=api_config['X-Node-Id'],
        senderid=player_user_id,
        senderid_adm=admin_user_id
    )

    # При необходимости можно добавить код для предварительной настройки API.

    yield api_fixture  # Завершение фикстуры.

    # Код для финализации после каждого теста, если необходимо

# Фикстура для UI тестов
@pytest.fixture(scope="session", autouse=False)
def app(request, config, init_authorization):
    # Фикстура для инициализации приложения (открытия браузера).
    web_config = config["web"]
    browser = request.config.getoption("--browser")
    auth, player_access_token, player_user_id, admin_access_token, admin_user_id, roomA, room_second_part, roomB, admin_api_token = init_authorization

    app_fixture = Application(browser=browser, base_url=web_config['baseUrl'], roomA=roomA, room_second_part=room_second_part, roomB=roomB)
    app_fixture.open_home_page()

    # При необходимости можно добавить код для предварительной настройки приложения.

    yield app_fixture  # Завершение фикстуры.

    # Код для финализации после каждого теста, если необходимо.
    # Например, выход из-под пользователя и закрытие браузера.
    # app_fixture.logout()
    app_fixture.destroy()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "dependency(): mark test to run only if dependencies have passed"
    )


