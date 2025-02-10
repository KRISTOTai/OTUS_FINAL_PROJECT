from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage


class Registrationpage(BasePage):
    REG_LINK = (By.CSS_SELECTOR, "li.breadcrumb-item a[href*='account/register'")
    FIRST_NAME = (By.XPATH, "//div[@class='col-sm-10']/input[@name='firstname' and @class='form-control']")
    PAS = (By.XPATH, "//div[@class='col-sm-10']/input[@name='password' and @class='form-control']")
    CONTINUE_BUTTON = (By.XPATH, "//button[@type='submit' and @class='btn btn-primary']")

    def get_reg_url(self, url_homepage):
        self.get_url(url_homepage + '/en-gb?route=account/register')
