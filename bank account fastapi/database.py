import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="harshini@2004",
        database="testdb",
        port=3306
    )
