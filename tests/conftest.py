from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions
import pytest
import logging
import datetime
import pymysql


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--container", action="store_true")
    parser.addoption("--url", default="http://192.168.31.246:8081", help="HomePage OpenCart")
    parser.addoption("--log_level", action="store", default="INFO")

    parser.addoption("--executor", action="store", default="192.168.31.246")
    parser.addoption("--video", action="store_true")
    parser.addoption("--logs", action="store_true")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--bv")

    parser.addoption("--host", default="127.0.0.1")
    parser.addoption("--port", default="3306")
    parser.addoption("--database", default="bitnami_opencart", help="Info from docker-compose")
    parser.addoption("--user", default="bn_opencart")
    parser.addoption("--password", default="")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")  # True - False
    log_level = request.config.getoption("--log_level")
    container = request.config.getoption("--container")

    logger = logging.getLogger(request.node.name)
    logger.setLevel(level=log_level)
    logger.info("=> Test started at %s" % datetime.datetime.now())

    if browser_name in ["brave_local", "br_local", "br"]:
        # Настраиваем параметры для Brave
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")  # Важно для Docker
            options.add_argument("--disable-dev-shm-usage")
        if container:
            options.binary_location = "/usr/bin/brave-browser"
        driver = webdriver.Chrome(
            service=BraveService(
                ChromeDriverManager(driver_version="135.0.7049.100", chrome_type=ChromeType.BRAVE).install()),
            options=options)
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


@pytest.fixture(scope="session")
def db_info(request):
    return (
        request.config.getoption("--host"),
        int(request.config.getoption("--port")),
        request.config.getoption("--database"),
        request.config.getoption("--user"),
        request.config.getoption("--password")
    )


@pytest.fixture(scope="session")
def connection(db_info, request):
    log_level = request.config.getoption("--log_level")

    logger = logging.getLogger(request.node.name)
    logger.setLevel(level=log_level)
    logger.info("=> Test DB started at %s" % datetime.datetime.now())
    host, port, database, user, password = db_info
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    yield conn
    conn.close()
    logger.info("=> Test DB finished at %s" % datetime.datetime.now())
