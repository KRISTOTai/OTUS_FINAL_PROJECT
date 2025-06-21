from faker import Faker
from datetime import datetime
import allure
import logging


class BasePageDB:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    def print_all(self, connection, table):
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {table}')
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            row_count = len(rows)

            allure.attach(" | ".join(columns), name="Заголовки колонок", attachment_type=allure.attachment_type.TEXT)
            for row in rows:
                self.logger.info(" | ".join(str(col) for col in row))
            self.logger.info(f"Количество строк: {row_count}")
            allure.attach(str(row_count), name="Количество строк", attachment_type=allure.attachment_type.TEXT)

    def amount_rows(self, connection, table):
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {table}')
            rows = cursor.fetchall()
            last_row = rows[-1] if rows else None
            self.logger.info(f"Всего строк: {len(rows)}")
            return {"length": len(rows), "last_row": last_row}

    @allure.step('Генерирую случайные данные для пользователя')
    def gen_random_users(self):
        faker = Faker()
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        telephone = faker.phone_number()
        password = faker.password()
        self.logger.info(f"Создан пользователь: {first_name} {last_name}, email: {email}")
        return first_name, last_name, email, telephone, password

    @allure.step('Создаю нового пользователя')
    def create_new_user(self, connection):
        first_name, last_name, email, telephone, password = self.gen_random_users()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with connection.cursor() as cursor:
            sql = """
            INSERT INTO oc_customer (
                customer_group_id, store_id, language_id,
                firstname, lastname, email, telephone,
                password, custom_field, newsletter,
                ip, status, safe, token, code, date_added
            ) VALUES (
                1, 0, 1, %s, %s, %s, %s,
                %s, '', 0,
                '127.0.0.1', 1, 0, '', '', %s
            )
            """
            cursor.execute(sql, (first_name, last_name, email, telephone, password, now))
            connection.commit()
            user_id = cursor.lastrowid
            self.logger.info(f"Добавлен пользователь с ID: {user_id}")
            return user_id

    @allure.step('Создаю новый купон')
    def create_new_coupon(self, connection, params):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params = params + (now,)
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO oc_coupon (
                    name, code, type, discount,
                    logged, shipping, total,
                    date_start, date_end,
                    uses_total, uses_customer,
                    status, date_added
                ) VALUES (
                    %s, %s, %s, %s,
                    0, 0, %s,
                    %s, %s,
                    %s, %s,
                    0, %s
                )
            """
            cursor.execute(sql, params)
            connection.commit()
            coupon_id = cursor.lastrowid
            self.logger.info(f"Добавлен купон с ID: {coupon_id}")
            return coupon_id

    def get_by_id(self, connection, row_id, table, column_name):
        with connection.cursor() as cursor:
            sql = f'SELECT * FROM {table} WHERE {column_name} = %s'
            cursor.execute(sql, (row_id,))
            row = cursor.fetchone()
            self.logger.info(f"Получена строка: {" | ".join(str(col) for col in row)}")
            return {"columns": [desc[0] for desc in cursor.description], "value": row}

    @allure.step('Обновляю данные последнего пользователя')
    def update_user(self, connection, id_user):
        if id_user is None:
            id_user = self.amount_rows(connection, table="oc_customer").get('last_row')[0]
        allure.dynamic.description(f"id : {id_user}")
        first_name, last_name, email, telephone, _ = self.gen_random_users()
        with connection.cursor() as cursor:
            sql = """
            UPDATE oc_customer SET
                firstname = %s,
                lastname = %s,
                email = %s,
                telephone = %s
            WHERE customer_id = %s
            """
            cursor.execute(sql, (first_name, last_name, email, telephone, id_user))
            connection.commit()
            self.logger.info(f"Обновлён пользователь с ID: {id_user}")
        return {"id_user": id_user, "rowcount": cursor.rowcount}

    @allure.step('Изменяю скидку последнего купона')
    def update_coupon_discount(self, connection, params, id_coupon):
        if id_coupon is None:
            id_coupon = self.amount_rows(connection, table="oc_coupon").get('last_row')[0]
        allure.dynamic.description(f"id : {id_coupon}")
        params = params + (id_coupon,)
        with connection.cursor() as cursor:
            sql = """
                    UPDATE oc_coupon SET
                        name = %s,
                        code = %s,
                        discount = %s,
                        total= %s
                    WHERE coupon_id = %s
                    """
            cursor.execute(sql, params)
            connection.commit()
            self.logger.info(f"Изменена скидка на купоне с ID: {id_coupon}")
        return {"id_coupon": id_coupon, "rowcount": cursor.rowcount}

    @allure.step('Изменяю период действия последнего купона')
    def update_coupon_period(self, connection, params, id_coupon):
        if id_coupon is None:
            id_coupon = self.amount_rows(connection, table="oc_coupon").get('last_row')[0]
        allure.dynamic.description(f"id : {id_coupon}")
        params = params + (id_coupon,)
        with connection.cursor() as cursor:
            sql = """
                    UPDATE oc_coupon SET
                        code = %s,
                        uses_total = %s,
                        uses_customer = %s,
                        date_end= %s
                    WHERE coupon_id = %s
                    """
            cursor.execute(sql, params)
            connection.commit()
            self.logger.info(f"Изменен период действия на купоне с ID: {id_coupon}")
        return {"id_coupon": id_coupon, "rowcount": cursor.rowcount}

    def delete_row(self, connection, row_id, table, column_name):
        # Вот такое приседание, потому что бд после удаления записи, создает новую строку с id + 1 от старого
        if row_id is None:
            row_id = self.amount_rows(connection, table).get('last_row')[0]
        with connection.cursor() as cursor:
            sql = f'DELETE FROM {table} WHERE {column_name} = %s;'
            cursor.execute(sql, (row_id,))
            connection.commit()
            self.logger.info(f"Удалёние пользователя с ID: {row_id}")
        return self.amount_rows(connection, table).get('length')
