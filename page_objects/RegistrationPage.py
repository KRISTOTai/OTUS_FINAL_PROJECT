from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage
from faker import Faker


class Registrationpage(BasePage):
    REG_LINK = (By.CSS_SELECTOR, "li.breadcrumb-item a[href*='account/register'")
    FIRST_NAME = (By.XPATH, "//div[@class='col-sm-10']/input[@name='firstname' and @class='form-control']")
    LAST_NAME = (By.CSS_SELECTOR, "[id = 'input-lastname']")
    EMAIL = (By.CSS_SELECTOR, "[id = 'input-email']")
    PAS = (By.XPATH, "//div[@class='col-sm-10']/input[@name='password' and @class='form-control']")
    CONTINUE_BUTTON = (By.XPATH, "//button[@type='submit' and @class='btn btn-primary']")
    PRIVATE_POLICY_BUTTON = (By.CSS_SELECTOR, "input.form-check-input[name = 'agree']")

    def get_reg_url(self, url_homepage):
        self.get_url(url_homepage + '/en-gb?route=account/register')

    def random_values(self):
        faker = Faker()
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        return first_name, last_name, email
