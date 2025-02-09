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
