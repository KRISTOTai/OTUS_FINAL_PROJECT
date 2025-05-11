import pytest
import allure
from page_objects.AdminPage import Adminpage


@allure.epic('Page actions')
@allure.feature('Handling with products')
@allure.title('Add new product on a Adminpage')
@pytest.mark.dependency()
@pytest.mark.order(1)
def test_add_item(browser, access, url_homepage):
    Adminpage(browser).get_auth_url(url_homepage)
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'

    Adminpage(browser).add_item_adminpg(access)


@allure.epic('Page actions')
@allure.feature('Handling with products')
@allure.title('Delete product on a Adminpage')
@pytest.mark.dependency(depends=["test_add_item"])
@pytest.mark.order(2)
def test_delete_item(browser, access, url_homepage):
    Adminpage(browser).get_auth_url(url_homepage)
    assert 'Administration' in browser.title, f'Ожидался заголовок с надписью Administration, а появился: {browser.title}'

    Adminpage(browser).delete_item_adminpg(access)
