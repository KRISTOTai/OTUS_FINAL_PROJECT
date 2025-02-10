import time

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


def test_registration(browser, url_homepage):
    Registrationpage(browser).get_reg_url(url_homepage)
    assert 'Register Account' in browser.title, f'Ожидался заголовок с надписью Register Account, а появился: {browser.title}'  # 1

    register_link = Registrationpage(browser).get_element(Registrationpage.REG_LINK)  # 2 CSS_SELECTOR
    assert register_link.text == 'Register', f'Ожидался текст с надписью Register, а появился: {register_link.text}'
    Registrationpage(browser).get_element(Registrationpage.FIRST_NAME)  # 3 XPATH
    Registrationpage(browser).get_element(Registrationpage.PAS)  # 4 XPATH
    continue_button = Registrationpage(browser).get_element(Registrationpage.CONTINUE_BUTTON)  # 5 XPATH
    assert continue_button.text == 'Continue', f'Ожидался текст с надписью Continue, а появился: {continue_button.text}'


def test_reg_new_user(browser, url_homepage):
    pass


def test_admin_auth(browser, access, url_homepage):
    username_text, password_text = access
    Adminpage(browser).get_auth_url(url_homepage)
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'  # 1

    username = Adminpage(browser).get_element(Adminpage.USERNAME)  # 2 CSS_SELECTOR
    password = Adminpage(browser).get_element(Adminpage.PAS)  # 3 CSS_SELECTOR
    login_button = Adminpage(browser).get_element(Adminpage.LOGING_BUTTON)  # 4 XPATH
    rights_link = Adminpage(browser).get_element(Adminpage.RIGHTS)  # 5 XPATH
    assert 'OpenCart' in rights_link.text, f'Ожидался текст с наличием надписи OpenCart, а появился: {rights_link.text}'

    username.click()
    username.send_keys(username_text)
    password.click()
    password.send_keys(password_text)
    login_button.click()
    Adminpage(browser).title_page(Adminpage.TITLE_ADMIN)
    assert 'Dashboard' in browser.title, f'Ожидался заголовок с надписью Dashboard, а появился: {browser.title}'

    Adminpage(browser).click_element(Adminpage.LOGOUT)
    Adminpage(browser).title_page(Adminpage.TITLE_AUTH)
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'


def test_add_item(browser, access, url_homepage):
    username_text, password_text = access
    word = 'XXX'
    Adminpage(browser).get_auth_url(url_homepage)
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'

    Adminpage(browser).click_element(Adminpage.USERNAME)
    Adminpage(browser).get_element(Adminpage.USERNAME).send_keys(username_text)
    Adminpage(browser).click_element(Adminpage.PAS)
    Adminpage(browser).get_element(Adminpage.PAS).send_keys(password_text)
    Adminpage(browser).click_element(Adminpage.LOGING_BUTTON)
    Adminpage(browser).title_page(Adminpage.TITLE_ADMIN)

    Adminpage(browser).click_element(Adminpage.CATALOG_ADMIN)
    Adminpage(browser).click_element(Adminpage.PRODUCTS_ADMIN)
    Adminpage(browser).click_element(Adminpage.PLUS_BUTTON)
    Adminpage(browser).get_element(Adminpage.CR_PRODUCT_NAME).send_keys(word)
    Adminpage(browser).get_element(Adminpage.CR_META_TAG).send_keys(word)
    Adminpage(browser).click_element(Adminpage.DATA_ADMIN)
    Adminpage(browser).get_element(Adminpage.CR_MODEL).send_keys(word)
    Adminpage(browser).click_element(Adminpage.SEO_ADMIN)
    Adminpage(browser).get_element(Adminpage.CR_KEYWORD).send_keys(word)
    Adminpage(browser).click_element(Adminpage.CR_SAVE)

    Adminpage(browser).click_element(Adminpage.PRODUCTS_ADMIN)
    Adminpage(browser).scrolling_page(Adminpage(browser).get_element(Adminpage.NAV_ARROW_ADMIN))
    time.sleep(0.5)
    Adminpage(browser).click_element(Adminpage.NAV_ARROW_ADMIN)
    Adminpage(browser).get_element(Adminpage.LIST_PRODUCT_NAME)


def test_delete_item(browser, access, url_homepage):
    username_text, password_text = access
    Adminpage(browser).get_auth_url(url_homepage)
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'

    Adminpage(browser).click_element(Adminpage.USERNAME)
    Adminpage(browser).get_element(Adminpage.USERNAME).send_keys(username_text)
    Adminpage(browser).click_element(Adminpage.PAS)
    Adminpage(browser).get_element(Adminpage.PAS).send_keys(password_text)
    Adminpage(browser).click_element(Adminpage.LOGING_BUTTON)
    Adminpage(browser).title_page(Adminpage.TITLE_ADMIN)

    Adminpage(browser).click_element(Adminpage.CATALOG_ADMIN)
    Adminpage(browser).click_element(Adminpage.PRODUCTS_ADMIN)
    Adminpage(browser).scrolling_page(Adminpage(browser).get_element(Adminpage.NAV_ARROW_ADMIN))
    time.sleep(0.5)
    Adminpage(browser).click_element(Adminpage.NAV_ARROW_ADMIN)
    Adminpage(browser).click_element(Adminpage.CHECKBOX_ADMIN)
    Adminpage(browser).scrolling_page(Adminpage(browser).get_element(Adminpage.CR_TRASH))
    time.sleep(0.5)
    Adminpage(browser).click_element(Adminpage.CR_TRASH)
    Adminpage(browser).allert().accept()

    Adminpage(browser).refresh_page()  # Проверка удаления элемента
    Adminpage(browser).scrolling_page(Adminpage(browser).get_element(Adminpage.NAV_ARROW_ADMIN))
    time.sleep(0.5)
    Adminpage(browser).click_element(Adminpage.NAV_ARROW_ADMIN)
    Adminpage(browser).is_element_absent(Adminpage.CHECKBOX_ADMIN)


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
