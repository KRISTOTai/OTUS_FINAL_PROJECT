import time
import allure
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

    @allure.step('Поиск элементов на странице регистрации')
    def get_elements_regpg(self):
        register_link = self.get_element(self.REG_LINK)
        continue_button = self.get_element(self.CONTINUE_BUTTON)
        self.get_element(self.FIRST_NAME)
        self.get_element(self.PAS)
        return register_link, continue_button

    @allure.step('Заполнение полей при регистрации')
    def set_elements_new_reg(self):
        first_name, lastname, email = self.random_values()
        self.get_element(self.FIRST_NAME).send_keys(first_name)
        self.get_element(self.LAST_NAME).send_keys(lastname)
        self.get_element(self.EMAIL).send_keys(email)
        self.get_element(self.PAS).send_keys('123456')
        self.scrolling_page(self.get_element(self.PRIVATE_POLICY_BUTTON))
        time.sleep(0.5)
        self.click_element(self.PRIVATE_POLICY_BUTTON)
        time.sleep(0.5)
        self.click_element(self.CONTINUE_BUTTON)
        time.sleep(0.5)
