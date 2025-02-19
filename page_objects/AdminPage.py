import time
import allure
from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage


class Adminpage(BasePage):
    USERNAME = (By.CSS_SELECTOR, "input[id = 'input-username']")
    PAS = (By.CSS_SELECTOR, "input[id = 'input-password']")
    LOGING_BUTTON = (By.XPATH, "//button[@class='btn btn-primary' and @type='submit']")
    RIGHTS = (By.XPATH, "//footer[@id='footer']/a")
    TITLE_AUTH = "Administration"
    LOGOUT = (By.CSS_SELECTOR, "li[id = 'nav-logout'] a.nav-link")
    TITLE_ADMIN = "Dashboard"

    CATALOG_ADMIN = (By.XPATH, "//a[@class='parent collapsed' and @href='#collapse-1']")
    PRODUCTS_ADMIN = (By.XPATH, "//a[contains(@href,'?route=catalog/product')]")
    PLUS_BUTTON = (By.CSS_SELECTOR, "i.fa-solid.fa-plus")
    CR_PRODUCT_NAME = (By.CSS_SELECTOR, "[id = 'input-name-1']")
    CR_META_TAG = (By.CSS_SELECTOR, "[id = 'input-meta-title-1']")
    DATA_ADMIN = (By.XPATH, "//a[@class='nav-link' and @href='#tab-data']")
    CR_MODEL = (By.CSS_SELECTOR, "[id = 'input-model']")
    SEO_ADMIN = (By.XPATH, "//a[@class='nav-link' and @href='#tab-seo']")
    CR_KEYWORD = (By.CSS_SELECTOR, "[id = 'input-keyword-0-1']")
    CR_SAVE = (By.CSS_SELECTOR, "i.fa-solid.fa-floppy-disk")
    NAV_ARROW_ADMIN = (By.XPATH, "//li[@class='page-item']/a[@class='page-link' and contains(text(), '>|')]")
    LIST_PRODUCT_NAME = (By.XPATH, "//td[@class='text-start' and contains(text(), 'XXX')]")
    CHECKBOX_ADMIN = (By.XPATH,
                      "//td[@class='text-start' and contains(text(), 'XXX')]/ancestor::tr//input[@class='form-check-input' and @type='checkbox']")
    CR_TRASH = (By.CSS_SELECTOR, "i.fa-regular.fa-trash-can")

    def get_auth_url(self, url_homepage):
        self.get_url(url_homepage + '/administration/')

    def get_elements_adminpg(self):
        username = self.get_element(self.USERNAME)  # 2 CSS_SELECTOR
        password = self.get_element(self.PAS)  # 3 CSS_SELECTOR
        login_button = self.get_element(self.LOGING_BUTTON)  # 4 XPATH
        rights_link = self.get_element(self.RIGHTS)  # 5 XPATH
        return username, password, login_button, rights_link

    @allure.step('Авторизация в админке')
    def login_adminpg(self, access):
        username_text, password_text = access
        username, password, login_button, _ = self.get_elements_adminpg()
        username.click()
        username.send_keys(username_text)
        password.click()
        password.send_keys(password_text)
        login_button.click()
        self.title_page(self.TITLE_ADMIN)

    @allure.step('Выход из админки')
    def logout_adminpg(self):
        self.click_element(self.LOGOUT)
        self.title_page(self.TITLE_AUTH)

    @allure.step('Добавление товара')
    def add_item_adminpg(self, access):
        word = 'XXX'
        self.login_adminpg(access)  # Авторизация

        self.click_element(self.CATALOG_ADMIN)  # Добавление продукта
        self.click_element(self.PRODUCTS_ADMIN)
        self.click_element(self.PLUS_BUTTON)
        self.get_element(self.CR_PRODUCT_NAME).send_keys(word)
        self.get_element(self.CR_META_TAG).send_keys(word)
        self.click_element(self.DATA_ADMIN)
        self.get_element(self.CR_MODEL).send_keys(word)
        self.click_element(self.SEO_ADMIN)
        self.get_element(self.CR_KEYWORD).send_keys(word)
        self.click_element(self.CR_SAVE)

        self.click_element(self.PRODUCTS_ADMIN)  # Проверка добавления
        self.scrolling_page(self.get_element(Adminpage.NAV_ARROW_ADMIN))
        time.sleep(0.5)
        self.click_element(self.NAV_ARROW_ADMIN)
        self.get_element(self.LIST_PRODUCT_NAME)

    @allure.step('Удаление товара')
    def delete_item_adminpg(self, access):
        self.login_adminpg(access)  # Авторизация

        self.click_element(self.CATALOG_ADMIN)  # Удаление продукта
        self.click_element(self.PRODUCTS_ADMIN)
        self.scrolling_page(self.get_element(self.NAV_ARROW_ADMIN))
        time.sleep(0.5)
        self.click_element(self.NAV_ARROW_ADMIN)
        self.click_element(self.CHECKBOX_ADMIN)
        self.scrolling_page(self.get_element(self.CR_TRASH))
        time.sleep(0.5)
        self.click_element(self.CR_TRASH)
        self.alert().accept()

        self.refresh_page()  # Проверка удаления продукта
        self.scrolling_page(self.get_element(self.NAV_ARROW_ADMIN))
        time.sleep(0.5)
        self.click_element(self.NAV_ARROW_ADMIN)
        self.is_element_absent(self.CHECKBOX_ADMIN)
