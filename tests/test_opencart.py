import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_homepage(browser, request):
    url_homepage = request.config.getoption("--url")
    browser.get(url_homepage)
    assert 'Store' in browser.title, f'Ожидался заголовок с надписью Store, а появился: {browser.title}'  # 1

    browser.find_element(By.CSS_SELECTOR, "[name = 'search']")  # 2 CSS_SELECTOR
    wait = WebDriverWait(browser, 2)
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//button[contains(@class, 'btn btn-lg btn-inverse btn-block dropdown-toggle')]")))  # 3 XPATH
    desktops_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.nav-link.dropdown-toggle")))
    assert desktops_link.text.strip() == "Desktops", f"Ожидался текст: Desktops, однако получен: {desktops_link.text.strip()}"  # 4 CSS_SELECTOR + text
    mp3_link = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a.nav-link.dropdown-toggle[href*='mp3-players']")))
    assert mp3_link.text.strip() == "MP3 Players", f"Ожидался текст: MP3 Players, однако получен: {mp3_link.text.strip()}"  # 5 CSS_SELECTOR + attribute


def test_cat_tablet(browser, request):
    url_homepage = request.config.getoption("--url")
    browser.get(url_homepage + '/en-gb/catalog/tablet')
    assert 'Tablets' in browser.title, f'Ожидался заголовок с надписью Tablets, а появился: {browser.title}'  # 1

    tablet_link = browser.find_element(By.XPATH, "//h4/a[contains(@href, 'galaxy')]")  # 2 XPATH
    assert 'Samsung Galaxy Tab 10.1' in tablet_link.text, f"Ожидался текст: Samsung Galaxy Tab 10.1, однако получен: {tablet_link.text.strip()}"
    wait = WebDriverWait(browser, 3)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "i.fa-solid.fa-heart")))  # 3 CSS_SELECTOR
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "i.fa-solid.fa-shopping-cart")))  # 4 CSS_SELECTOR
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//i[@class = 'fa-solid fa-table-list']")))  # 5 XPATH


def test_product_tablet(browser, request):
    url_homepage = request.config.getoption("--url")
    browser.get(url_homepage + '/en-gb/product/tablet/samsung-galaxy-tab-10-1')
    assert '10.1' in browser.title, f'Ожидался заголовок с надписью 10.1, а появился: {browser.title}'  # 1

    wait = WebDriverWait(browser, 2)
    wait.until(EC.text_to_be_present_in_element((By.XPATH, "//li/a[contains(@href, 'samsung-galaxy-tab-10-1')]"),
                                                "Samsung Galaxy Tab 10.1"))
    tablet_link = browser.find_element(By.CSS_SELECTOR,
                                       "li a[href*='samsung-galaxy-tab-10-1'")  # 2 XPATH + CSS_SELECTOR
    assert 'Samsung Galaxy Tab 10.1' == tablet_link.text, f"Ожидался текст: Samsung Galaxy Tab 10.1, однако получен: {tablet_link.text.strip()}"
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[id = 'button-cart']")))  # 3 CSS_SELECTOR
    description_tablet = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "li a.nav-link.active[href*='description']")))  # 4 CSS_SELECTOR
    assert description_tablet.text == "Description", f'Здесь ожидается текст: Description, а получен {description_tablet.text}'
    review_tablet = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "li a.nav-link[href*='review']")))  # 5 CSS_SELECTOR
    assert 'Reviews' in review_tablet.text, f'Здесь ожидается наличие текста: Review, а получен {description_tablet.text}'


def test_registration(browser, request):
    url_homepage = request.config.getoption("--url")
    browser.get(url_homepage + '/en-gb?route=account/register')
    assert 'Register Account' in browser.title, f'Ожидался заголовок с надписью Register Account, а появился: {browser.title}'  # 1

    register_link = browser.find_element(By.CSS_SELECTOR,
                                         "li.breadcrumb-item a[href*='account/register'")  # 2 CSS_SELECTOR
    assert register_link.text == 'Register', f'Ожидался текст с надписью Register, а появился: {register_link.text}'
    wait = WebDriverWait(browser, 2)
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@class='col-sm-10']/input[@name='firstname' and @class='form-control']")))  # 3 XPATH
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@class='col-sm-10']/input[@name='password' and @class='form-control']")))  # 4 XPATH
    continue_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@type='submit' and @class='btn btn-primary']")))  # 5 XPATH
    assert continue_button.text == 'Continue', f'Ожидался текст с надписью Continue, а появился: {continue_button.text}'


def test_auth(browser, access, request):
    username_text, password_text = access
    url_homepage = request.config.getoption("--url")
    browser.get(url_homepage + '/administration/')
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'  # 1

    wait = WebDriverWait(browser, 2)
    username = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input[id = 'input-username']")))  # 2 CSS_SELECTOR
    password = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input[id = 'input-password']")))  # 3 CSS_SELECTOR
    login_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@class='btn btn-primary' and @type='submit']")))  # 4 XPATH
    rights_link = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//footer[@id='footer']/a")))  # 5 XPATH
    assert 'OpenCart' in rights_link.text, f'Ожидался текст с наличием надписи OpenCart, а появился: {rights_link.text}'

    username.click()
    username.send_keys(username_text)
    password.click()
    password.send_keys(password_text)
    login_button.click()
    wait = WebDriverWait(browser, 2)
    wait.until(EC.title_contains("Dashboard"))
    assert 'Dashboard' in browser.title, f'Ожидался заголовок с надписью Dashboard, а появился: {browser.title}'

    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "li[id = 'nav-logout'] a.nav-link"))).click()
    wait.until(EC.title_contains("Administration"))
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'


def test_cart(browser, request):
    url_homepage = request.config.getoption("--url")
    browser.get(url_homepage)
    assert 'Store' in browser.title, f'Ожидался заголовок с надписью Store, а появился: {browser.title}'

    wait = WebDriverWait(browser, 5)
    wait.until(EC.visibility_of_element_located(
        (By.XPATH,
         "//div[@class='col mb-3']//a[contains(@href, 'product/iphone')]/img[@title = 'iPhone']"))).click()
    wait.until(EC.title_contains("iPhone"))
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR,
         "button[id = 'button-cart']"))).click()
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div[id = 'alert'] button.btn-close"))).click()
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[@title = 'Shopping Cart']/span[@class = 'd-none d-md-inline']"))).click()
    cart_item = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//td[@class = 'text-start text-wrap']/a[contains(@href,'product/iphone')]")))
    assert 'iPhone' in cart_item.text, f'Ожидался текст с наличием надписи iPhone, а появился: {cart_item.text}'


def test_currency(browser, request):
    url_homepage = request.config.getoption("--url")
    browser.get(url_homepage)
    assert 'Store' in browser.title, f'Ожидался заголовок с надписью Store, а появился: {browser.title}'

    wait = WebDriverWait(browser, 3)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR,
         "i.fa-solid.fa-caret-down"))).click()
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR,
         "li a[href = 'EUR']"))).click()
    change_price = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR,
         "div.price span.price-new")))
    assert '€' in change_price.text, f'Ожидалась валюта €, а появилась: {change_price.text}'

    browser.get(url_homepage + '/en-gb/catalog/tablet')
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR,
         "i.fa-solid.fa-caret-down"))).click()
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR,
         "li a[href = 'GBP']"))).click()
    change_price_gbp = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR,
         "div.price span.price-new")))
    assert '£' in change_price_gbp.text, f'Ожидалась валюта £, а появилась: {change_price_gbp.text}'
