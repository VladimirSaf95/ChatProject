from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException, InvalidElementStateException
from selenium.webdriver.common.action_chains import ActionChains
import logging
import os
import jsonpickle

class HelperBase:
    TIMEOUT = 3

    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
        self.setup_browser_window_size()

    def setup_browser_window_size(self):
        # Устанавливаем размер окна браузера
        self.app.wd.set_window_size(1200, 700)

    def scroll_to_element(self, element):
        wd = self.app.wd
        wd.execute_script("arguments[0].scrollIntoView(true);", element)

    def fill_field(self, field_id, value):
        wd = self.app.wd
        try:
            element = wd.find_element(By.ID, field_id)
            self.scroll_to_element(element)
            if element.is_enabled():
                try:
                    element.clear()
                    element.send_keys(value)
                except InvalidElementStateException as e:
                    self.logger.error(f"Failed to clear element {field_id}: {e}")
            else:
                self.logger.warning(f"Element {field_id} is not enabled and cannot be cleared.")
        except NoSuchElementException:
            self.logger.error(f"Element {field_id} not found")

    def click_element_by_xpath(self, xpath):
        wd = self.app.wd
        try:
            element = WebDriverWait(wd, self.TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            self.scroll_to_element(element)
            self.click_element_with_retry(element)
        except TimeoutException:
            self.logger.error(f"Timeout: Element {xpath} not found or not clickable")

    def click_element_by_css_selector(self, selector):
        wd = self.app.wd
        try:
            element = WebDriverWait(wd, self.TIMEOUT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            self.scroll_to_element(element)
            self.click_element_with_retry(element)
        except TimeoutException:
            self.logger.error(f"Timeout: Element {selector} not found or not clickable")

    def check_css_selector_existence(self, selector):
        wd = self.app.wd
        try:
            wd.find_element(By.CSS_SELECTOR, selector)
            return True
        except NoSuchElementException:
            return False

    def click_element_with_retry(self, element):
        try:
            element.click()
        except ElementClickInterceptedException:
            self.logger.warning("Click intercepted, attempting retry.")
            self.wait_and_click(element)

    def wait_and_click(self, element):
        wd = self.app.wd
        try:
            wd.execute_script("arguments[0].click();", element)
        except TimeoutException:
            self.logger.error("Timeout: Element not clickable after retry")

    def fillingregfields(self, *fields):
        for field_id, field_value in fields:
            self.fill_field(field_id, field_value)

    def checkofframe(self, framename, buttonname):
        wd = self.app.wd
        try:
            frame = wd.find_element(By.CSS_SELECTOR, framename)
            wd.switch_to.frame(frame)
            # Выполняйте действия внутри фрейма, например, клик по кнопке
            button = wd.find_elements(By.CSS_SELECTOR, buttonname)
            if button:
                button[0].click()
            # Возврат к основному контексту после выполнения действий внутри фрейма
            wd.switch_to.default_content()
        except NoSuchElementException:
            pass

    def checkoffmodal(self, modalname, mbuttonname=None):
        wd = self.app.wd
        try:
            WebDriverWait(wd, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, modalname)) and
                EC.visibility_of_element_located((By.CLASS_NAME, modalname))
            )
            if mbuttonname:
                button = wd.find_elements(By.CSS_SELECTOR, mbuttonname)
                if button:
                    button[0].click()
        except (TimeoutException, NoSuchElementException):
            pass

    def is_modal_displayed(self, modal_class):
        wd = self.app.wd
        try:
            WebDriverWait(wd, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, modal_class)) and
                EC.visibility_of_element_located((By.CLASS_NAME, modal_class))
            )
            return True  # Модальное окно отображается
        except (TimeoutException, NoSuchElementException):
            return False  # Модальное окно не отображается

    def click_checkbox_with_js(self, element):
        wd = self.app.wd
        try:
            wd.execute_script("arguments[0].click();", element)
            self.logger.info("Checkbox clicked successfully.")
        except Exception as e:
            self.logger.error(f"Failed to click checkbox: {e}")

    def check_checkboxes(self):
        wd = self.app.wd
        wait = WebDriverWait(wd, 2)

        # Находим элементы label с атрибутом for, связанными с чекбоксом
        labels = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'label[for="registration_termsAndConditions"]')))

        # Перебираем найденные label
        for label in labels:
            # Получаем связанный чекбокс по id
            checkbox_id = label.get_attribute("for")
            checkbox = wd.find_element(By.ID, checkbox_id)

            # Проверяем, не выбран ли чекбокс, и кликаем при необходимости
            if checkbox and not checkbox.is_selected():
                self.click_checkbox_with_js(checkbox)

    def fillmodal(self):
        self.checkoffmodal('modal__language', 'button[data-popup-language-button=""]')

    def find_elements_by_class(self, class_name):
        wd = self.app.wd
        elements = wd.find_elements(By.CLASS_NAME, class_name)
        return elements

    def find_elements_by_tag(self, tag_name):
        wd = self.app.wd
        elements = wd.find_elements(By.TAG_NAME, tag_name)
        return elements

    def check_chatbutton_existence(self):
        wd = self.app.wd
        test_id = "chat-close-icon"
        selector = f'[data-testid="{test_id}"]'
        try:
            wd.find_element(By.CSS_SELECTOR, selector)
            return True
        except NoSuchElementException:
            return False
    def clickchatbutton(self):
        test_id = "chat-chatButton-openButton"
        selector = f'[data-testid="{test_id}"]'
        self.click_element_by_css_selector(selector)

    def find_element_by_text(self, text):
        wd = self.app.wd
        try:
            return wd.find_element(By.XPATH, f"//*[text()='{text}']")
        except NoSuchElementException:
            return None
