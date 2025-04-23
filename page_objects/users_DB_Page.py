from faker import Faker
from datetime import datetime
import allure
import logging


class UsersDB:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    @allure.step('Вывожу всех пользователей')
    def print_all_customers(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM oc_customer")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            row_count = len(rows)

            allure.attach(" | ".join(columns), name="Заголовки колонок", attachment_type=allure.attachment_type.TEXT)
            for row in rows:
                self.logger.info(" | ".join(str(col) for col in row))
            self.logger.info(f"Количество строк: {row_count}")
            allure.attach(str(row_count), name="Количество строк", attachment_type=allure.attachment_type.TEXT)

    @allure.step('Подсчитываю количество строк и возвращаю последнюю')
    def amount_users(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM oc_customer")
            rows = cursor.fetchall()
            last_row = rows[-1] if rows else None
            self.logger.info(f"Всего пользователей: {len(rows)}")
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

    @allure.step('Получаю пользователя по ID: {user_id}')
    def get_user_by_id(self, user_id, connection):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM oc_customer WHERE customer_id = %s"
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            self.logger.info(f"Получен пользователь: {" | ".join(str(col) for col in row)}")
            return {"columns": [desc[0] for desc in cursor.description], "value": row}

    @allure.step('Обновляю данные последнего пользователя')
    def update_user(self, connection):
        id_user = self.amount_users(connection).get('last_row')[0]
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
        return id_user

    @allure.step('Удаляю последнего пользователя')
    def delete_user(self, connection):
        # Вот такое приседание, потому, что бд после удаления записи, создает нового пользователя с id + 1 от старого
        id_user = self.amount_users(connection).get('last_row')[0]
        with connection.cursor() as cursor:
            sql = "DELETE FROM oc_customer WHERE customer_id = %s;"
            cursor.execute(sql, (id_user,))
            connection.commit()
            self.logger.info(f"Удалён пользователь с ID: {id_user}")
        return self.amount_users(connection).get('length')
