from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions
import pytest
import logging
import datetime


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--url", default="http://192.168.31.246:8081", help="HomePage OpenCart")
    parser.addoption("--log_level", action="store", default="INFO")

    parser.addoption("--executor", action="store", default="192.168.31.246")
    parser.addoption("--video", action="store_true")
    parser.addoption("--logs", action="store_true")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--bv")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")  # True - False
    log_level = request.config.getoption("--log_level")

    logger = logging.getLogger(request.node.name)
    logger.setLevel(level=log_level)
    logger.info("=> Test started at %s" % datetime.datetime.now())

    if browser_name in ["brave_local", "br_local", "br"]:
        brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        chromedriver_path = "C:/Users/Igoryan/.cache/selenium/chromedriver/win64/132.0.6834.159/chromedriver.exe"
        # Настраиваем параметры для Brave
        options = ChromeOptions()
        options.binary_location = brave_path
        if headless:
            options.add_argument("--headless=new")
        # Создаём экземпляр браузера
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "chrome":
        options = ChromeOptions()
        driver = remote_start(options, request)
    elif browser_name == "firefox":
        options = FFOptions()
        driver = remote_start(options, request)
    else:
        raise ValueError(f"Неизвестный браузер: {browser_name}")
    driver.maximize_window()

    yield driver

    driver.quit()
    logger.info("=> Test finished at %s" % datetime.datetime.now())


def remote_start(options, request):
    executor = request.config.getoption("--executor")
    browser_name = request.config.getoption("--browser")
    version = request.config.getoption("--bv")
    logs = request.config.getoption("--logs")
    video = request.config.getoption("--video")
    vnc = request.config.getoption("--vnc")
    caps = {
        "browserName": browser_name,
        # "browserVersion": version,
        "selenoid:options": {
            "enableVNC": vnc,
            "name": request.node.name,
            # "screenResolution": "1280x2000",
            "enableVideo": video,
            "enableLog": logs,
            "timeZone": "Europe/Moscow",
            "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru:en", "LC_ALL=ru_RU.UTF-8"]
        },
        # "acceptInsecureCerts": True,
    }

    for k, v in caps.items():
        options.set_capability(k, v)

    driver = webdriver.Remote(
        command_executor=f"http://{executor}:4444/wd/hub",
        options=options
    )
    return driver


@pytest.fixture()
def url_homepage(browser, request):
    return request.config.getoption("--url")


@pytest.fixture()
def access():
    opencart_username = 'user'
    opencart_password = 'bitnami'
    return opencart_username, opencart_password
