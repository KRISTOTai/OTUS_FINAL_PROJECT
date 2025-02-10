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
