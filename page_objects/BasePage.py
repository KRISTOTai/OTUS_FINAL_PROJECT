import allure
import time
import logging
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, browser):
        self.browser = browser
        self.logger = logging.getLogger(__class__.__name__)

    def wrapper_screenshot(self, action, error):
        try:
            return action()
        except error as e:
            screenshot_name = f"screen_{e.__class__.__name__}_{time.strftime('%Y%m%d_%H%M%S')}.png"
            allure.attach(body=self.browser.get_screenshot_as_png(),
                          name=screenshot_name,
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Ошибка: {e.__class__.__name__}")

    @allure.step('Открываю url: {url}')
    def get_url(self, url):
        self.logger.info(f"Get url {url}")
        return self.browser.get(url)

    @allure.step('Получаю элемент: {locator}')
    def get_element(self, locator: tuple, timeout=5):
        self.logger.info(f"Get element {locator}")
        return self.wrapper_screenshot(
            lambda: WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator)),
            TimeoutException)

    @allure.step('Кликаю на элемент: {locator}')
    def click_element(self, locator):
        self.logger.info(f"Click element {locator}")
        self.get_element(locator).click()

    @allure.step('Ищу текст {text} в элементе: {locator}')
    def present_element(self, locator: tuple, text: str, timeout=5):
        self.logger.info(f"Present element {locator}")
        return self.wrapper_screenshot(
            lambda: WebDriverWait(self.browser, timeout).until(EC.text_to_be_present_in_element(locator, text)),
            TimeoutException)

    @allure.step('Ищу заголовок с текстом {text}')
    def title_page(self, text: str, timeout=5):
        self.logger.info(f"Find title {text}")
        return self.wrapper_screenshot(
            lambda: WebDriverWait(self.browser, timeout).until(EC.title_contains(text)),
            TimeoutException)

    @allure.step('Скролю страницу до элемента')
    def scrolling_page(self, element):
        self.logger.info(f"Scrolling action")
        return self.wrapper_screenshot(
            lambda: self.browser.execute_script("arguments[0].scrollIntoView(true);", element),
            TimeoutException)

    @allure.step('Ищу отсутствующий элемент')
    def is_element_absent(self, locator, timeout=5):
        self.logger.info(f"Check deleted element {locator}")
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
            return False, print('Элемент найден, Ошибка')
        except TimeoutException:
            return True, print('Элемент ожидаемо не найден')

    @allure.step('Ловлю alert')
    def alert(self, timeout=2):
        self.logger.info(f"Catch alert")
        return WebDriverWait(self.browser, timeout).until(EC.alert_is_present())

    @allure.step('Обновляю страницу')
    def refresh_page(self):
        self.logger.info(f"Refresh page")
        self.browser.refresh()
