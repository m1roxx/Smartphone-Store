import psycopg2


class UserManager:
    def __init__(self, connection):
        self.connection = connection

    def register_user(self, username, password):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                existing_user = cursor.fetchone()
                if existing_user:
                    print("Username already exists. Please choose a different username.")
                    return False
                else:
                    query = "INSERT INTO users (username, password, role) VALUES (%s, %s, 'customer')"
                    cursor.execute(query, (username, password))
                    self.connection.commit()
                    print("Registration successful.")
                    return True
        except Exception as e:
            print("Error registering user:", e)
            return False

    def login_user(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            if user:
                user_info = {
                    'user_id': user[0],
                    'username': user[1],
                    'password': user[2],
                    'role': user[3]
                }
                print("Login successful.")
                return user_info

            else:
                return None
