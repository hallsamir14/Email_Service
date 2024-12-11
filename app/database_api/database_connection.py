from typing import Optional
import mysql.connector
from mysql.connector import errorcode


def set_connection(
    host: Optional[str] = "localhost",
    user: Optional[str] = "root",
    password: Optional[str] = "",
    database_ID: str = "ecommerce",
) -> mysql.connector.connection.MySQLConnection:
    try:
        # print credentials for development only
        print(host + " " + user + " " + password + " " + database_ID)

        return mysql.connector.connect(
            host=host, user=user, password=password, database=database_ID
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return None
        else:
            print(err)
            return None


# -----------------------------------------------------------------------------
# main function for dev testing only
# -----------------------------------------------------------------------------
def main():
    connection = set_connection()
    if connection:
        print("Connected to database")
        # close_connection(connection)
    else:
        print("Failed to connect to database")
    # TODO:try and exception logic here
    # exmample query
    curser = connection.cursor()
    curser.execute("SELECT * FROM products")
    for row in curser.fetchall():
        print(row)
    connection.close()


if __name__ == "__main__":
    main()
