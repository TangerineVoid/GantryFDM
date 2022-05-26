import mysql.connector
from mysql.connector import Error


class SqlCOM:
    # instance attributes

    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.connection = None

    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                database=self.database
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return self.connection

    def create_database(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Database created successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def add_value(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Value was added successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def select_from(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            val = cursor.fetchall()
            print("Value was read successfully")
            return val
        except Error as e:
            print(f"The error '{e}' occurred")



#connection = create_connection("localhost", "root", "admin", "sm_app")
#connection = create_connection("localhost", "root", "admin")
#create_database_query = "CREATE DATABASE sm_app"
#create_database(connection, create_database_query)