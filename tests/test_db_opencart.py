from page_objects.users_DB_Page import UsersDB
import allure


@allure.epic('DB actions')
@allure.title('Check table')
def test_check_table(connection):
    db = UsersDB()
    db.print_all_customers(connection)


@allure.epic('DB actions')
@allure.feature('Create_user')
@allure.title('Update_user_neg')
def test_update_user_neg(connection):
    non_existent_id = 999999  # несуществующий ID
    first_name, last_name, email, telephone, _ = UsersDB().gen_random_users()

    with connection.cursor() as cursor:
        sql = """
        UPDATE oc_customer SET
            firstname = %s,
            lastname = %s,
            email = %s,
            telephone = %s
        WHERE customer_id = %s
        """
        cursor.execute(sql, (first_name, last_name, email, telephone, non_existent_id))
        connection.commit()
        assert cursor.rowcount == 0, "Обновление прошло, хотя пользователя не существует"


@allure.epic('DB actions')
@allure.feature('Delete_user')
@allure.title('Delete_user_neg')
def test_delete_user_neg(connection):
    non_existent_id = 999999

    with connection.cursor() as cursor:
        sql = "DELETE FROM oc_customer WHERE customer_id = %s;"
        cursor.execute(sql, (non_existent_id,))
        connection.commit()
        assert cursor.rowcount == 0, "Удалён несуществующий пользователь"
