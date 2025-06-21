import allure
from .BasePage_DB import BasePageDB


class CouponsDB(BasePageDB):
    TABLE = "oc_coupon"
    COLUMN_NAME = "coupon_id"

    @allure.step('Вывожу все доступные купоны')
    def print_all_coupons(self, connection):
        self.print_all(connection, self.TABLE)

    @allure.step('Подсчитываю количество строк и возвращаю последнюю')
    def amount_coupons(self, connection):
        return self.amount_rows(connection, self.TABLE)

    @allure.step('Получаю купон по ID: {row_id}')
    def get_coupon_by_id(self, connection, row_id):
        return self.get_by_id(connection, row_id, self.TABLE, self.COLUMN_NAME)

    @allure.step('Удаляю последний купон')
    def delete_coupon(self, connection):
        return self.delete_row(connection, self.TABLE, self.COLUMN_NAME)
