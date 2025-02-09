from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_objects.HomePage import Homepage
from page_objects.CatalogPage import Catalogpage
from page_objects.NavPanPage import Currency
from page_objects.NavPanPage import ShoppingCart
from page_objects.CartPage import Cart


def test_homepage(browser, url_homepage):
    Homepage(browser).get_hp_url(url_homepage)
    assert 'Store' in browser.title, f'Ожидался заголовок с надписью Store, а появился: {browser.title}'  # 1

    Homepage(browser).get_element(Homepage.SEARCH)  # 2 CSS_SELECTOR
    Homepage(browser).get_element(Homepage.CART_BUTTON)  # 3 XPATH
    desktops_link = Homepage(browser).get_element(Homepage.DESCTOPS_NAV_PAN)
    assert desktops_link.text.strip() == "Desktops", f"Ожидался текст: Desktops, однако получен: {desktops_link.text.strip()}"  # 4 CSS_SELECTOR + text
    mp3_link = Homepage(browser).get_element(Homepage.MP3_NAV_PAN)
    assert mp3_link.text.strip() == "MP3 Players", f"Ожидался текст: MP3 Players, однако получен: {mp3_link.text.strip()}"  # 5 CSS_SELECTOR + attribute


def test_cat_tablet(browser, url_homepage):
    Catalogpage(browser).get_catalog_url(url_homepage)
    assert 'Tablets' in browser.title, f'Ожидался заголовок с надписью Tablets, а появился: {browser.title}'  # 1

    tablet_link = Catalogpage(browser).get_element(Catalogpage.SAMSUNG_LINK)  # 2 XPATH
    assert 'Samsung Galaxy Tab 10.1' in tablet_link.text, f"Ожидался текст: Samsung Galaxy Tab 10.1, однако получен: {tablet_link.text.strip()}"
    Catalogpage(browser).get_element(Catalogpage.HEART_BUTTON)  # 3 CSS_SELECTOR
    Catalogpage(browser).get_element(Catalogpage.SHOPCART_BUTTON)  # 4 CSS_SELECTOR
    Catalogpage(browser).get_element(Catalogpage.SORT_LIST)  # 5 XPATH


def test_product_tablet(browser, url_homepage):
    Catalogpage(browser).get_cat_product_url(url_homepage)
    assert '10.1' in browser.title, f'Ожидался заголовок с надписью 10.1, а появился: {browser.title}'  # 1

    Catalogpage(browser).present_element(Catalogpage.NAV_ITEM_LINK, "Samsung Galaxy Tab 10.1")
    tablet_link = Catalogpage(browser).get_element(Catalogpage.NAV_ITEM_LINK_CSS)  # 2 XPATH + CSS_SELECTOR
    assert 'Samsung Galaxy Tab 10.1' == tablet_link.text, f"Ожидался текст: Samsung Galaxy Tab 10.1, однако получен: {tablet_link.text.strip()}"
    Catalogpage(browser).get_element(Catalogpage.ADD_TO_CART)  # 3 CSS_SELECTOR
    description_tablet = Catalogpage(browser).get_element(Catalogpage.DESCRIPTION_ITEM)  # 4 CSS_SELECTOR
    assert description_tablet.text == "Description", f'Здесь ожидается текст: Description, а получен {description_tablet.text}'
    review_tablet = Catalogpage(browser).get_element(Catalogpage.REVIEW_ITEM)  # 5 CSS_SELECTOR
    assert 'Reviews' in review_tablet.text, f'Здесь ожидается наличие текста: Review, а получен {description_tablet.text}'


# Registration/Authorisation
def test_registration(browser, url_homepage):
    Homepage(browser).get_url(url_homepage + '/en-gb?route=account/register')
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


# Registration/Authorisation
def test_auth(browser, access, url_homepage):
    username_text, password_text = access
    Homepage(browser).get_url(url_homepage + '/administration/')
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


def test_cart(browser, url_homepage):
    Homepage(browser).get_url(url_homepage)
    assert 'Store' in browser.title, f'Ожидался заголовок с надписью Store, а появился: {browser.title}'

    Homepage(browser).click_element(Homepage.IPHONE_ITEM)
    Catalogpage(browser).title_page(Catalogpage.IPHONE_TITLE)
    Catalogpage(browser).click_element(Catalogpage.ADD_TO_CART)
    Catalogpage(browser).click_element(Catalogpage.ALLERT_CLOSE)
    ShoppingCart(browser).click_element(ShoppingCart.SHOP_CART_BUTTON)
    cart_item = Cart(browser).get_element(Cart.PRODUCT_NAME)
    assert 'iPhone' in cart_item.text, f'Ожидался текст с наличием надписи iPhone, а появился: {cart_item.text}'


def test_currency(browser, url_homepage):
    Homepage(browser).get_hp_url(url_homepage)
    assert 'Store' in browser.title, f'Ожидался заголовок с надписью Store, а появился: {browser.title}'
    Currency(browser).click_element(Currency.CARET_DOWN)
    Currency(browser).click_element(Currency.EUR)
    change_price = Currency(browser).click_element(Currency.PRICE_ITEM)
    assert '€' in change_price.text, f'Ожидалась валюта €, а появилась: {change_price.text}'

    Catalogpage(browser).get_catalog_url(url_homepage)
    Currency(browser).click_element(Currency.CARET_DOWN)
    Currency(browser).click_element(Currency.GBP)
    change_price_gbp = Currency(browser).click_element(Currency.PRICE_ITEM)
    assert '£' in change_price_gbp.text, f'Ожидалась валюта £, а появилась: {change_price_gbp.text}'
