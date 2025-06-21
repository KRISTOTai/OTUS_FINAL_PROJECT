import allure
from .BasePage_DB import BasePageDB


class UsersDB(BasePageDB):
    TABLE = "oc_customer"
    COLUMN_NAME = "customer_id"

    @allure.step('Вывожу всех пользователей')
    def print_all_customers(self, connection):
        self.print_all(connection, self.TABLE)

    @allure.step('Подсчитываю количество строк и возвращаю последнюю')
    def amount_users(self, connection):
        return self.amount_rows(connection, self.TABLE)

    @allure.step('Получаю пользователя по ID: {row_id}')
    def get_user_by_id(self, connection, row_id):
        return self.get_by_id(connection, row_id, self.TABLE, self.COLUMN_NAME)

    @allure.step('Удаляю последнего пользователя')
    def delete_user(self, connection):
        return self.delete_row(connection, self.TABLE, self.COLUMN_NAME)
