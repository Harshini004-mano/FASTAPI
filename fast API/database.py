import mysql.connector

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="harshini@2004",
        port=3306,
        database="testdb"
    )
