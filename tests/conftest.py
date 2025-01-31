from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions
import pytest


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--url", default="http://192.168.31.246:8081", help="HomePage OpenCart")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")  # True - False

    if browser_name in ["chrome", "ch"]:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
    elif browser_name in ["firefox", "ff"]:
        options = FFOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif browser_name in ["brave", "br"]:
        brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        chromedriver_path = "C:/Users/Igoryan/.cache/selenium/chromedriver/win64/131.0.6778.264/chromedriver.exe"
        # Настраиваем параметры для Brave
        options = ChromeOptions()
        options.binary_location = brave_path
        # Создаём экземпляр браузера
        service = Service(chromedriver_path)
        if headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=service, options=options)

    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture()
def access():
    opencart_username = 'user'
    opencart_password = 'bitnami'
    return opencart_username, opencart_password
