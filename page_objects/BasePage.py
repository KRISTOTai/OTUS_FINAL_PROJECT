from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, browser):
        self.browser = browser

    def get_url(self, url):
        return self.browser.get(url)

    def get_element(self, locator: tuple, timeout=5):
        return WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))

    def click_element(self, locator):
        self.get_element(locator).click()

    def present_element(self, locator: tuple, text: str, timeout=5):
        return WebDriverWait(self.browser, timeout).until(EC.text_to_be_present_in_element(locator, text))

    def title_page(self, text: str, timeout=5):
        return WebDriverWait(self.browser, timeout).until(EC.title_contains(text))

    def scrolling_page(self, element):
        return self.browser.execute_script("arguments[0].scrollIntoView(true);", element)

    def is_element_absent(self, locator, timeout=5):

        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
            return False, print('Элемент найден, Ошибка')
        except TimeoutException:
            return True, print('Элемент ожидаемо не найден')

    def allert(self, timeout=2):
        return WebDriverWait(self.browser, timeout).until(EC.alert_is_present())

    def refresh_page(self):
        self.browser.refresh()
