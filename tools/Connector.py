import mysql.connector


class Connector:
    def __init__(self, config, type_conn="r"):
        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()
            self.database_name = self.connection.database
            self.is_writable = False if type_conn == "r" else True if type_conn == "rw" else False
            print(f"Connection established to db {self.database_name}")
            if self.is_writable:
                self.check_and_create_table()

        except mysql.connector.Error:
            try:
                self.database_name = config.pop("database")
                self.connection = mysql.connector.connect(**config)
                self.cursor = self.connection.cursor()
                self.is_writable = False if type_conn == "r" else True if type_conn == "rw" else False
                if not self.database_exists():
                    if self.is_writable:
                        self.create_database()
                    else:
                        print("Database is mode read-only!")
                print(f"Connection established to db {self.database_name}")
            except mysql.connector.Error as e:
                print(f"Error with connection {e}")

    def database_exists(self):
        self.cursor.execute("SHOW DATABASES LIKE %s", (self.database_name,))
        return self.cursor.fetchone() is not None

    def create_database(self):
        try:
            self.cursor.execute(f"CREATE DATABASE {self.database_name}")
            print(f"Database '{self.database_name}' created successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to create database '{self.database_name}': {err}")

    def check_and_create_table(self):
        table_exists = self.table_exists("sakila_history_search")
        if not table_exists:
            self.create_table()
        else:
            print("Table 'sakila_history_search' already exists.")

    def table_exists(self, table_name):
        self.cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        return self.cursor.fetchone() is not None

    def create_table(self):
        create_table_query = """
        CREATE TABLE sakila_history_search (
            id INT AUTO_INCREMENT PRIMARY KEY,
            query VARCHAR(100)
        )
        """
        try:
            self.cursor.execute(create_table_query)
            print("Table 'sakila_history_search' created successfully.")
        except mysql.connector.Error as e:
            print(f"Failed to create table 'sakila_history_search': {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed")
