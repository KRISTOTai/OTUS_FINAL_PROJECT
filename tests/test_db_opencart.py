from page_objects.Users_DB_Page import UsersDB
from page_objects.Coupon_DB_Page import CouponsDB
import allure


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
