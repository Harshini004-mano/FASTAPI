"""
 # get operation
  # example 1

 from fastapi import FastAPI  # Capital F and A

app = FastAPI()  # Also capital F and A

@app.get("/")
def read_root():
    return {"Hello": "world"}  # No semicolon needed"""

# example 2
"""from fastapi import FastAPI  

app = FastAPI()  
@app.get("/home")
def read_root():
    return {"Hello": "world"}"""


"""
# example 3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from database import get_database_connection

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
   

# CREATE USER
@app.post("/users")
async def create_user(user: User):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"   
        values = (user.name, user.email)   
        cursor.execute(query, values)
        connection.commit()
        return {"message": "User created successfully"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        connection.close()

# READ ALL USERS
@app.get("/users")
async def read_users():
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

# READ SINGLE USER
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

# UPDATE USER
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (user.name, user.email, user_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "User updated successfully"}

# DELETE USER
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "User deleted successfully"} """

from fastapi import FastAPI
from pydantic import BaseModel
from database import get_database_connection

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    phone: str
    address: str

# CREATE
@app.post("/users")
async def create_user(user: User):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (name, email, phone, address) VALUES (%s, %s, %s, %s)"
    values = (user.name, user.email, user.phone, user.address)
    cursor.execute(query, values)
    connection.commit()
    connection.close()
    return {"message": "User created successfully"}

# READ (all)
@app.get("/users")
async def read_users():
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.close()
    return users


# UPDATE
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "UPDATE users SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
    values = (user.name, user.email, user.phone, user.address, user_id)
    cursor.execute(query, values)
    connection.commit()
    connection.close()
    return {"message": "User updated successfully"}

# DELETE
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    connection.commit()
    connection.close()
    return {"message": "User deleted successfully"}

