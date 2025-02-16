import allure
import time
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, browser):
        self.browser = browser

    def wrapper_screenshot(self, action, error):
        try:
            return action()
        except error as e:
            screenshot_name = f"screen_{e.__class__.__name__}_{time.strftime('%Y%m%d_%H%M%S')}.png"
            allure.attach(body=self.browser.get_screenshot_as_png(),
                          name=screenshot_name,
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError(e.__class__.__name__)

    @allure.step('Открываю url: {url}')
    def get_url(self, url):
        return self.browser.get(url)

    @allure.step('Получаю элемент: {locator}')
    def get_element(self, locator: tuple, timeout=5):
        return self.wrapper_screenshot(
            lambda: WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator)),
            TimeoutException)

    @allure.step('Кликаю на элемент: {locator}')
    def click_element(self, locator):
        self.get_element(locator).click()

    @allure.step('Ищу текст {text} в элементе: {locator}')
    def present_element(self, locator: tuple, text: str, timeout=5):
        return self.wrapper_screenshot(
            lambda: WebDriverWait(self.browser, timeout).until(EC.text_to_be_present_in_element(locator, text)),
            TimeoutException)

    @allure.step('Ищу заголовок с текстом {text}')
    def title_page(self, text: str, timeout=5):
        return self.wrapper_screenshot(
            lambda: WebDriverWait(self.browser, timeout).until(EC.title_contains(text)),
            TimeoutException)

    @allure.step('Скролю страницу до элемента')
    def scrolling_page(self, element):
        return self.wrapper_screenshot(
            lambda: self.browser.execute_script("arguments[0].scrollIntoView(true);", element),
            TimeoutException)

    @allure.step('Ищу отсутствующий элемент')
    def is_element_absent(self, locator, timeout=5):

        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
            return False, print('Элемент найден, Ошибка')
        except TimeoutException:
            return True, print('Элемент ожидаемо не найден')

    @allure.step('Ловлю alert')
    def alert(self, timeout=2):
        return WebDriverWait(self.browser, timeout).until(EC.alert_is_present())

    @allure.step('Обновляю страницу')
    def refresh_page(self):
        self.browser.refresh()
