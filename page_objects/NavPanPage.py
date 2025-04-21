import time
from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage
import allure


class Currency(BasePage):
    PRICE_ITEM = (By.CSS_SELECTOR, "div.price span.price-new")
    CARET_DOWN = (By.CSS_SELECTOR, "i.fa-solid.fa-caret-down")
    EUR = (By.CSS_SELECTOR, "li a[href = 'EUR']")
    GBP = (By.CSS_SELECTOR, "li a[href = 'GBP']")

    @allure.step('Изменение валюты')
    def get_elements_currency(self, locator):
        self.click_element(self.CARET_DOWN)
        self.click_element(locator)
        time.sleep(0.5)
        return self.get_element(self.PRICE_ITEM)


class ShoppingCart(BasePage):
    SHOP_CART_BUTTON = (By.XPATH, "//a[@title = 'Shopping Cart']/span[@class = 'd-none d-md-inline']")
