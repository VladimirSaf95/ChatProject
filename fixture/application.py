# Импортируем необходимые модули.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import os

class Application():

    def __init__(self, browser, base_url, roomA, room_second_part, roomB):
        if browser == "chrome":
            if os.getenv("DOCKER_CONTAINER"):
                # Указание пути к ChromeDriver и бинарному файлу Chrome в контейнере
                chrome_options = webdriver.ChromeOptions()
                chrome_options.binary_location = '/usr/bin/chromium-browser'  # Путь к бинарному файлу Chrome внутри контейнера
                chrome_driver_path = '/usr/bin/chromedriver'  # Путь к ChromeDriver внутри контейнера

                # Создание экземпляра драйвера Chrome
                self.wd = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
            else:
                # Если код запускается локально, то используем стандартный путь к ChromeDriver
                self.wd = webdriver.Chrome()
        elif browser == "safari":
            self.wd = webdriver.Safari()
        else:
            raise ValueError(f"Неправильно указан браузер: {browser}")

        self.base_url = base_url
        self.room_second_part = room_second_part
        self.roomA = roomA
        self.roomB = roomB

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

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


