from faker import Faker
from datetime import datetime


class UsersDB:

    def print_all_customers(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM oc_customer")
            # Получаем названия колонок
            columns = [desc[0] for desc in cursor.description]
            # Получаем все строки
            rows = cursor.fetchall()
            # Печатаем заголовки
            print(" | ".join(columns))

            for row in rows:
                print(" | ".join(str(col) for col in row))
            print(f"Количество строк: {len(rows)}")

    def amount_users(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM oc_customer")
            rows = cursor.fetchall()
            last_row = rows[len(rows) - 1]
            return {"length": len(rows), "last_row": last_row}

    def gen_random_users(self):
        faker = Faker()
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        telephone = faker.phone_number()
        password = faker.password()
        return first_name, last_name, email, telephone, password

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
            return cursor.lastrowid

    def get_user_by_id(self, user_id, connection):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM oc_customer WHERE customer_id = %s"
            cursor.execute(sql, (user_id,))
            return {"columns": [desc[0] for desc in cursor.description], "value": cursor.fetchone()}

    def update_user(self, connection):
        id_user = self.amount_users(connection).get('last_row')[0]
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
        return id_user

    def delete_user(self, connection):
        # Вот такое приседание, потому, что бд после удаления записи, создает нового пользователя с id + 1 от старого
        id_user = self.amount_users(connection).get('last_row')[0]
        with connection.cursor() as cursor:
            sql = "DELETE FROM oc_customer WHERE customer_id = %s;"
            cursor.execute(sql, (id_user,))
            connection.commit()
        return self.amount_users(connection).get('length')
