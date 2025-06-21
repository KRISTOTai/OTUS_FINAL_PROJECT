from page_objects.Users_DB_Page import UsersDB
from page_objects.Coupon_DB_Page import CouponsDB
import allure
import pytest


@allure.epic('DB actions')
@allure.title('Check table')
@pytest.mark.dependency()
@pytest.mark.order(1)
def test_check_user_table(connection):
    db = UsersDB()
    db.print_all_customers(connection)


@allure.epic('DB actions')
@allure.feature('Create_user')
@allure.title('Create_new_user')
@pytest.mark.dependency(depends=["test_check_user_table"])
@pytest.mark.order(2)
def test_create_new_user(connection):
    new_user_id = UsersDB().create_new_user(connection)

    result = UsersDB().get_user_by_id(connection, new_user_id).get("value")
    formated_result = " | ".join(str(col) for col in result)
    assert result is not None, "Пользователь не был добавлен в таблицу"
    print(f"Пользователь с ID {new_user_id} добавлен: {formated_result}")


@allure.epic('DB actions')
@allure.feature('Create_user')
@allure.title('Update_new_user')
@pytest.mark.dependency(depends=["test_create_new_user"])
@pytest.mark.order(3)
def test_update_new_user(connection):
    user_before_update = UsersDB().amount_users(connection).get("last_row")
    last_row_id = UsersDB().update_user(connection, id_user=None).get("id_user")
    user_after_update = UsersDB().get_user_by_id(connection, last_row_id).get("value")
    assert user_before_update[4] != user_after_update[4], f"Имена после апдейта совпали"
    assert user_before_update[5] != user_after_update[5], f"Фамилии после апдейта совпали"


@allure.epic('DB actions')
@allure.feature('Delete_user')
@allure.title('Delete_last_user')
@pytest.mark.dependency(depends=["test_update_new_user"])
@pytest.mark.order(4)
def test_delete_last_user(connection):
    amount_users_before = UsersDB().amount_users(connection).get("length")
    amount_users_after = UsersDB().delete_user(connection, row_id=None)
    assert amount_users_before - 1 == amount_users_after, f'Количество пользователей не стало меньше после удаления'


@allure.epic('DB actions')
@allure.title('Check table')
@pytest.mark.dependency()
@pytest.mark.order(5)
def test_check_coupons_table(connection):
    db = CouponsDB()
    db.print_all_coupons(connection)


@allure.epic('DB actions')
@allure.feature('Create_coupon')
@allure.title('Create_new_coupon')
@pytest.mark.dependency(depends=["test_check_coupons_table"])
@pytest.mark.order(6)
def test_create_new_coupon(connection):
    new_coupon_id = CouponsDB().create_new_coupon(connection)
    result = CouponsDB().get_coupon_by_id(connection, new_coupon_id).get("value")
    formated_result = " | ".join(str(col) for col in result)
    assert result is not None, "Купон не был добавлен в таблицу"
    print(f"Купон с ID {new_coupon_id} добавлен: {formated_result}")


@allure.epic('DB actions')
@allure.feature('Create_coupon')
@allure.title('Update_new_coupon')
@pytest.mark.dependency(depends=["test_create_new_coupon"])
@pytest.mark.order(7)
@pytest.mark.parametrize(("code", "uses_total", "uses_customer", "date_end"),
                         [(999, 15, 15, "2026-01-01"), (888, 100, 100, "2027-01-01")], ids=[tuple, tuple])
def test_update_coupon_period(connection, code, uses_total, uses_customer, date_end):
    params = (code, uses_total, uses_customer, date_end)
    rowcount = CouponsDB().update_coupon_period(connection, params, id_coupon=None).get("rowcount")
    assert rowcount == 1, "Обновление не прошло"


@allure.epic('DB actions')
@allure.feature('Create_coupon')
@allure.title('Update_new_coupon')
@pytest.mark.dependency(depends=["test_create_new_coupon"])
@pytest.mark.order(8)
@pytest.mark.parametrize(("name", "code", "discount", "total"),
                         [("10% Discount", 999, 10.0, 10.0), ("15% Discount", 888, 15.0, 15.0)], ids=[tuple, tuple])
def test_update_coupon_discount(connection, name, code, discount, total):
    params = (name, code, discount, total)
    rowcount = CouponsDB().update_coupon_discount(connection, params, id_coupon=None).get("rowcount")
    assert rowcount == 1, "Обновление не прошло"


@allure.epic('DB actions')
@allure.feature('Delete_user')
@allure.title('Delete_last_user')
@pytest.mark.dependency(depends=["test_update_new_user"])
@pytest.mark.order(9)
def test_delete_coupon_neg(connection):
    amount_coupons_before = CouponsDB().amount_coupons(connection).get("length")
    amount_coupons_after = CouponsDB().delete_coupon(connection, row_id=None)
    assert amount_coupons_before - 1 == amount_coupons_after, "Количество купонов не уменьшилось после удаления"
