# Импортируем необходимые модули.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

class Application():

    def __init__(self, browser, base_url, roomA, room_second_part, roomB):
        if browser == "chrome":
            # Создание экземпляра драйвера Chrome
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            self.wd = webdriver.Chrome(options=options)
        elif browser == "safari":
            # Создание экземпляра драйвера Safari
            self.wd = webdriver.Safari()
        else:
            raise ValueError(f"Неправильно указан браузер: {browser}")

        self.base_url = base_url
        self.room_second_part = room_second_part
        self.roomA = roomA
        self.roomB = roomB

    def is_valid(self):
        try:
            self.wd.current_url
            return True  # Если успешно получили URL, считаем приложение валидным.
        except:
            return False  # Если возникла ошибка, считаем приложение невалидным.

    def is_valid_s(self):
        return self.wd.current_url

    def is_valid_localation(self, local):
        return self.wd.current_url.endswith(local)

    def open_home_page(self):
        modified_base_url = self.checkurl("/en")  # Удаляем / в конце, если есть
        self.wd.get(modified_base_url)

    def checkurl(self, endpoint):
        base_url = self.base_url.rstrip('/')  # Удаляем заключающий слеш, если он есть
        correct_url = f"{base_url}{endpoint}"
        return correct_url

    def check_current_url(self):
        if "/user/login" in self.wd.current_url:
            print(self.wd.current_url)
            return True
        else:
            return False

    def open_changelocation_ru(self):
        login_url = self.checkurl("/ru")  # Вызываем метод checkurl класса
        self.wd.get(login_url)

    def open_signin_page(self):
        login_url = self.checkurl("/user/login")  # Вызываем метод checkurl класса
        self.wd.get(login_url)

    def open_signup_page(self):
        login_url = self.checkurl("/user/registration")  # Вызываем метод checkurl класса
        self.wd.get(login_url)

    def logout(self):
        logout_url = self.checkurl("/user/logout")  # Вызываем метод checkurl класса
        self.wd.get(logout_url)

    def destroy(self):
        # Завершаем работу браузера и освобождаем ресурсы.
        self.wd.quit()


