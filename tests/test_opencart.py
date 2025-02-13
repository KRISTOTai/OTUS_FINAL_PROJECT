from page_objects.HomePage import Homepage
from page_objects.CatalogPage import Catalogpage
from page_objects.NavPanPage import Currency
from page_objects.NavPanPage import ShoppingCart
from page_objects.CartPage import Cart
from page_objects.RegistrationPage import Registrationpage
from page_objects.AdminPage import Adminpage


def test_homepage(browser, url_homepage):
    Homepage(browser).get_hp_url(url_homepage)
    assert 'Store' in browser.title, f'Ожидался заголовок с надписью Store, а появился: {browser.title}'  # 1

    desktops_link, mp3_link = Homepage(browser).get_elements_homepg()  # 2-3 CSS_SELECTOR, XPATH
    assert desktops_link.text.strip() == "Desktops", f"Ожидался текст: Desktops, однако получен: {desktops_link.text.strip()}"  # 4 CSS_SELECTOR + text
    assert mp3_link.text.strip() == "MP3 Players", f"Ожидался текст: MP3 Players, однако получен: {mp3_link.text.strip()}"  # 5 CSS_SELECTOR + attribute


def test_cat_tablet(browser, url_homepage):
    Catalogpage(browser).get_catalog_url(url_homepage)
    assert 'Tablets' in browser.title, f'Ожидался заголовок с надписью Tablets, а появился: {browser.title}'  # 1

    tablet_link = Catalogpage(browser).get_elements_catalogpg()  # 2-5 XPATH, CSS_SELECTOR
    assert 'Samsung Galaxy Tab 10.1' in tablet_link.text, f"Ожидался текст: Samsung Galaxy Tab 10.1, однако получен: {tablet_link.text.strip()}"


def test_product_tablet(browser, url_homepage):
    Catalogpage(browser).get_cat_product_url(url_homepage)
    assert '10.1' in browser.title, f'Ожидался заголовок с надписью 10.1, а появился: {browser.title}'  # 1

    tablet_link, description_tablet, review_tablet = Catalogpage(
        browser).get_elements_product_catalogpg()  # 2-5 XPATH, CSS_SELECTOR
    assert 'Samsung Galaxy Tab 10.1' == tablet_link.text, f"Ожидался текст: Samsung Galaxy Tab 10.1, однако получен: {tablet_link.text.strip()}"
    assert description_tablet.text == "Description", f'Здесь ожидается текст: Description, а получен {description_tablet.text}'
    assert 'Reviews' in review_tablet.text, f'Здесь ожидается наличие текста: Review, а получен {description_tablet.text}'


def test_registration(browser, url_homepage):
    Registrationpage(browser).get_reg_url(url_homepage)
    assert 'Register Account' in browser.title, f'Ожидался заголовок с надписью Register Account, а появился: {browser.title}'  # 1

    register_link, continue_button = Registrationpage(browser).get_elements_regpg()  # 2-5 CSS_SELECTOR, XPATH
    assert register_link.text == 'Register', f'Ожидался текст с надписью Register, а появился: {register_link.text}'
    assert continue_button.text == 'Continue', f'Ожидался текст с надписью Continue, а появился: {continue_button.text}'


def test_reg_new_user(browser, url_homepage):
    Registrationpage(browser).get_reg_url(url_homepage)
    assert 'Register Account' in browser.title, f'Ожидался заголовок с надписью Register Account, а появился: {browser.title}'

    Registrationpage(browser).set_elements_new_reg()
    assert 'Your Account Has Been Created!' in browser.title, f'Ожидалась страница подтверждения аккаунта, а появилась {browser.title}'


def test_admin_auth(browser, access, url_homepage):
    Adminpage(browser).get_auth_url(url_homepage)
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'  # 1

    _, _, _, rights_link = Adminpage(browser).get_elements_adminpg()  # 2-5 CSS_SELECTOR, XPATH
    assert 'OpenCart' in rights_link.text, f'Ожидался текст с наличием надписи OpenCart, а появился: {rights_link.text}'

    Adminpage(browser).login_adminpg(access)
    assert 'Dashboard' in browser.title, f'Ожидался заголовок с надписью Dashboard, а появился: {browser.title}'
    Adminpage(browser).logout_adminpg()
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'


def test_add_item(browser, access, url_homepage):
    Adminpage(browser).get_auth_url(url_homepage)
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'

    Adminpage(browser).add_item_adminpg(access)


def test_delete_item(browser, access, url_homepage):
    Adminpage(browser).get_auth_url(url_homepage)
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'

    Adminpage(browser).delete_item_adminpg(access)


def test_cart(browser, url_homepage):
    Homepage(browser).get_url(url_homepage)
    assert 'Store' in browser.title, f'Ожидался заголовок с надписью Store, а появился: {browser.title}'

    Homepage(browser).click_element(Homepage.IPHONE_ITEM)
    Catalogpage(browser).get_elements_for_cart_catalogpg()
    ShoppingCart(browser).click_element(ShoppingCart.SHOP_CART_BUTTON)
    cart_item = Cart(browser).get_elements_cart()
    assert 'iPhone' in cart_item.text, f'Ожидался текст с наличием надписи iPhone, а появился: {cart_item.text}'


def test_currency(browser, url_homepage):
    Homepage(browser).get_hp_url(url_homepage)
    assert 'Store' in browser.title, f'Ожидался заголовок с надписью Store, а появился: {browser.title}'
    change_price = Currency(browser).get_elements_currency(Currency.EUR)
    assert '€' in change_price.text, f'Ожидалась валюта €, а появилась: {change_price.text}'

    Catalogpage(browser).get_catalog_url(url_homepage)
    change_price_gbp = Currency(browser).get_elements_currency(Currency.GBP)
    assert '£' in change_price_gbp.text, f'Ожидалась валюта £, а появилась: {change_price_gbp.text}'
