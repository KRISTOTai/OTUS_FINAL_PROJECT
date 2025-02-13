from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage


class Cart(BasePage):
    PRODUCT_NAME = (By.XPATH, "//td[@class = 'text-start text-wrap']/a[contains(@href,'product/iphone')]")

    def get_cart_url(self, url_homepage):
        self.get_url(url_homepage + '/en-gb?route=checkout/cart')
