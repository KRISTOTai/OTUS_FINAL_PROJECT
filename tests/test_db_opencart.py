from page_objects.Users_DB_Page import UsersDB
from page_objects.Coupon_DB_Page import CouponsDB
import allure
import pytest


@allure.epic('DB actions')
@allure.title('Check table')
def test_check_users_table(connection):
    db = UsersDB()
    db.print_all_customers(connection)


@allure.epic('DB actions')
@allure.feature('Create_user')
@allure.title('Update_user_neg')
def test_update_user_neg(connection):
    non_existent_id = 999999  # несуществующий ID
    rowcount = UsersDB().update_user(connection, non_existent_id).get("rowcount")
    assert rowcount == 0, "Обновление прошло, хотя пользователя не существует"


@allure.epic('DB actions')
@allure.feature('Delete_user')
@allure.title('Delete_user_neg')
def test_delete_user_neg(connection):
    non_existent_id = 999999
    amount_users_before = UsersDB().amount_users(connection).get("length")
    amount_users_after = UsersDB().delete_user(connection, non_existent_id)
    assert amount_users_before == amount_users_after, "Удалён несуществующий пользователь"


@allure.epic('DB actions')
@allure.title('Check table')
def test_check_coupons_table(connection):
    db = CouponsDB()
    db.print_all_coupons(connection)


@allure.epic('DB actions')
@allure.feature('Create_coupon')
@allure.title('Update_coupon_neg')
@pytest.mark.parametrize(("name", "code", "discount", "total"),
                         [("10% Discount", 999, 10.0, 10.0), ("15% Discount", 888, 15.0, 15.0)], ids=[tuple, tuple])
def test_update_coupon_discount_neg(connection, name, code, discount, total):
    params = (name, code, discount, total)
    non_existent_id = 999999  # несуществующий ID
    rowcount = CouponsDB().update_coupon_discount(connection, params, non_existent_id).get("rowcount")
    assert rowcount == 0, "Обновление прошло, хотя купона не существует"


@allure.epic('DB actions')
@allure.feature('Create_coupon')
@allure.title('Update_coupon_neg')
@pytest.mark.parametrize(("code", "uses_total", "uses_customer", "date_end"),
                         [(9990, 15, 15, "2026-01-01"), (8880, 150, 150, "2027-01-01")], ids=[tuple, tuple])
def test_update_coupon_period_neg(connection, code, uses_total, uses_customer, date_end):
    params = (code, uses_total, uses_customer, date_end)
    non_existent_id = 999999  # несуществующий ID
    rowcount = CouponsDB().update_coupon_period(connection, params, non_existent_id).get("rowcount")
    assert rowcount == 0, "Обновление прошло, хотя купона не существует"


@allure.epic('DB actions')
@allure.feature('Delete_coupon')
@allure.title('Delete_coupon_neg')
def test_delete_coupon_neg(connection):
    non_existent_id = 999999
    amount_coupons_before = CouponsDB().amount_coupons(connection).get("length")
    amount_coupons_after = CouponsDB().delete_coupon(connection, non_existent_id)
    assert amount_coupons_before == amount_coupons_after, "Удалён несуществующий купон"
