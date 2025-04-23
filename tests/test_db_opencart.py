from page_objects.users_DB_Page import UsersDB
import allure


@allure.epic('DB actions')
@allure.title('Check table')
def test_check_table(connection):
    db = UsersDB()
    db.print_all_customers(connection)


@allure.epic('DB actions')
@allure.feature('Create_user')
@allure.title('Create_new_user')
def test_create_new_user(connection):
    new_user_id = UsersDB().create_new_user(connection)

    result = UsersDB().get_user_by_id(new_user_id, connection).get("value")
    formated_result = " | ".join(str(col) for col in result)
    assert result is not None, "Пользователь не был добавлен в таблицу"
    print(f"Пользователь с ID {new_user_id} добавлен: {formated_result}")


@allure.epic('DB actions')
@allure.feature('Create_user')
@allure.title('Update_new_user')
def test_update_new_user(connection):
    user_before_update = UsersDB().amount_users(connection).get("last_row")
    last_row_id = UsersDB().update_user(connection)
    user_after_update = UsersDB().get_user_by_id(last_row_id, connection).get("value")
    assert user_before_update[4] != user_after_update[4], f"Имена после апдейта совпали"
    assert user_before_update[5] != user_after_update[5], f"Фамилии после апдейта совпали"


@allure.epic('DB actions')
@allure.feature('Delete_user')
@allure.title('Delete_last_user')
def test_delete_last_user(connection):
    amount_users_before = UsersDB().amount_users(connection).get("length")
    amount_users_after = UsersDB().delete_user(connection)
    assert amount_users_before - 1 == amount_users_after, f'Количество пользователей не стало меньше после удаления'


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
