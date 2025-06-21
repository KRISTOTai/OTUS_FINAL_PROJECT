import allure
from .BasePage_DB import BasePageDB


class CouponsDB(BasePageDB):
    TABLE = "oc_coupon"
    COLUMN_NAME = "coupon_id"
    PARAMS = ("20% Discount", 5555, "F", 20.0, 20.0, "2025-11-11", "2026-11-11", 100, 100)

    @allure.step('Вывожу все доступные купоны')
    def print_all_coupons(self, connection):
        self.print_all(connection, self.TABLE)

    @allure.step('Создаю новый купон')
    def create_new_coupon(self, connection):
        return self.create_new_coupons(connection, self.PARAMS)

    @allure.step('Подсчитываю количество строк и возвращаю последнюю')
    def amount_coupons(self, connection):
        return self.amount_rows(connection, self.TABLE)

    @allure.step('Получаю купон по ID: {row_id}')
    def get_coupon_by_id(self, connection, row_id):
        return self.get_by_id(connection, row_id, self.TABLE, self.COLUMN_NAME)

    @allure.step('Удаляю последний купон')
    def delete_coupon(self, connection, row_id):
        return self.delete_row(connection, row_id, self.TABLE, self.COLUMN_NAME)
