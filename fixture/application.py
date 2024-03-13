# Импортируем необходимые модули.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

class Application():

    def __init__(self, browser, base_url):
        if browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "safari":
            self.wd = webdriver.Safari()
        else:
            raise ValueError(f"Неправильно указан браузер: {browser}")

        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True  # Если успешно получили URL, считаем приложение валидным.
        except:
            return False  # Если возникла ошибка, считаем приложение невалидным.

    def is_valid_s(self):
        return self.wd.current_url

    def open_home_page(self):
        modified_base_url = self.base_url.rstrip('/')  # Удаляем / в конце, если есть
        self.wd.get(modified_base_url)

    def checkurl(self, endpoint):
        base_url = self.base_url.rstrip('/')  # Удаляем заключающий слеш, если он есть
        correct_url = f"{base_url}{endpoint}"
        return correct_url


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


