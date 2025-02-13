from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage


class Homepage(BasePage):
    SEARCH = (By.CSS_SELECTOR, "[name = 'search']")
    CART_BUTTON = (By.XPATH, "//button[contains(@class, 'btn btn-lg btn-inverse btn-block dropdown-toggle')]")
    DESCTOPS_NAV_PAN = (By.CSS_SELECTOR, "a.nav-link.dropdown-toggle")
    MP3_NAV_PAN = (By.CSS_SELECTOR, "a.nav-link.dropdown-toggle[href*='mp3-players']")
    IPHONE_ITEM = (By.XPATH, "//div[@class='col mb-3']//a[contains(@href, 'product/iphone')]/img[@title = 'iPhone']")

    def get_hp_url(self, url_homepage):
        self.get_url(url_homepage)
