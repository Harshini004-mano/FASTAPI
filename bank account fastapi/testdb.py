import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshini@2004",
            port=3306,
            database="testdb"
        )
        print("Connection successful")
        return conn
    except mysql.connector.Error as e:
        print("Couldn't connect to MySQL.")
        print("Error:", e)
        return None

# Test the connection
if __name__ == "__main__":
    get_connection()