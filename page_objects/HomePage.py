from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage
import allure


class Homepage(BasePage):
    SEARCH = (By.CSS_SELECTOR, "[name = 'search']")
    CART_BUTTON = (By.XPATH, "//button[contains(@class, 'btn btn-lg btn-inverse btn-block dropdown-toggle')]")
    DESCTOPS_NAV_PAN = (By.CSS_SELECTOR, "a.nav-link.dropdown-toggle")
    MP3_NAV_PAN = (By.CSS_SELECTOR, "a.nav-link.dropdown-toggle[href*='mp3-players']")
    IPHONE_ITEM = (By.XPATH, "//div[@class='col mb-3']//a[contains(@href, 'product/iphone')]/img[@title = 'iPhone']")

    def get_hp_url(self, url_homepage):
        self.get_url(url_homepage)

    @allure.step('Поиск элементов на стартовой странице')
    def get_elements_homepg(self):
        self.get_element(self.SEARCH)
        self.get_element(self.CART_BUTTON)
        desktops_link = self.get_element(self.DESCTOPS_NAV_PAN)
        mp3_link = self.get_element(self.MP3_NAV_PAN)
        return desktops_link, mp3_link
