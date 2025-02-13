from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage


class Catalogpage(BasePage):
    SAMSUNG_LINK = (By.XPATH, "//h4/a[contains(@href, 'galaxy')]")
    HEART_BUTTON = (By.CSS_SELECTOR, "i.fa-solid.fa-heart")
    SHOPCART_BUTTON = (By.CSS_SELECTOR, "i.fa-solid.fa-shopping-cart")
    SORT_LIST = (By.XPATH, "//i[@class = 'fa-solid fa-table-list']")

    NAV_ITEM_LINK = (By.XPATH, "//li/a[contains(@href, 'samsung-galaxy-tab-10-1')]")
    NAV_ITEM_LINK_CSS = (By.CSS_SELECTOR, "li a[href*='samsung-galaxy-tab-10-1'")
    ADD_TO_CART = (By.CSS_SELECTOR, "[id = 'button-cart']")
    DESCRIPTION_ITEM = (By.CSS_SELECTOR, "li a.nav-link.active[href*='description']")
    REVIEW_ITEM = (By.CSS_SELECTOR, "li a.nav-link[href*='review']")

    IPHONE_TITLE = "iPhone"
    ALLERT_CLOSE = (By.CSS_SELECTOR, "div[id = 'alert'] button.btn-close")

    def get_catalog_url(self, url_homepage):
        self.get_url(url_homepage + '/en-gb/catalog/tablet')

    def get_cat_product_url(self, url_homepage):
        self.get_url(url_homepage + '/en-gb/product/tablet/samsung-galaxy-tab-10-1')