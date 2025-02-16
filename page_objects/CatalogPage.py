from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage
import allure


class Catalogpage(BasePage):
    SAMSUNG_LINK = (By.XPATH, "//h4/a[contains(@href, 'galaxy')]")
    HEART_BUTTON = (By.CSS_SELECTOR, "i.fa-solid.fa-heart")
    SHOPCART_BUTTON = (By.CSS_SELECTOR, "i.fa-solid.fa-shopping-cart")
    SORT_LIST = (By.XPATH, "//i[@class = 'fa-solid fa-table-list']")

    NAV_ITEM_LINK = (By.XPATH, "//li/a[contains(@href, 'samsung-galaxy-tab-10-1')]")
    # NAV_ITEM_LINK_CSS = (By.CSS_SELECTOR, "li a[href*='samsung-galaxy-tab-10-1'")
    ADD_TO_CART = (By.CSS_SELECTOR, "[id = 'button-cart']")
    DESCRIPTION_ITEM = (By.CSS_SELECTOR, "li a.nav-link.active[href*='description']")
    REVIEW_ITEM = (By.CSS_SELECTOR, "li a.nav-link[href*='review']")

    IPHONE_TITLE = "iPhone"
    ALLERT_CLOSE = (By.CSS_SELECTOR, "div[id = 'alert'] button.btn-close")

    def get_catalog_url(self, url_homepage):
        self.get_url(url_homepage + '/en-gb/catalog/tablet')

    def get_cat_product_url(self, url_homepage):
        self.get_url(url_homepage + '/en-gb/product/tablet/samsung-galaxy-tab-10-1')

    @allure.step('Поиск элементов в каталоге')
    def get_elements_catalogpg(self):
        tablet_link = self.get_element(self.SAMSUNG_LINK)
        self.get_element(self.HEART_BUTTON)
        self.get_element(self.SHOPCART_BUTTON)
        self.get_element(self.SORT_LIST)
        return tablet_link

    @allure.step('Поиск элементов в карточке продукта')
    def get_elements_product_catalogpg(self):
        tablet_link = self.get_element(self.NAV_ITEM_LINK)
        description_tablet = self.get_element(self.DESCRIPTION_ITEM)
        review_tablet = self.get_element(self.REVIEW_ITEM)
        self.present_element(self.NAV_ITEM_LINK, "Samsung Galaxy Tab 10.1")
        self.get_element(self.ADD_TO_CART)
        return tablet_link, description_tablet, review_tablet

    @allure.step('Добавление в корзину')
    def get_elements_for_cart_catalogpg(self):
        self.title_page(self.IPHONE_TITLE)
        self.click_element(self.ADD_TO_CART)
        self.click_element(self.ALLERT_CLOSE)
