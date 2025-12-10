from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection

app = FastAPI()

# -------------------- Pydantic Models --------------------
class AccountCreate(BaseModel):
    account_holder: str
    account_number: str
    password: str

class LoginRequest(BaseModel):
    account_number: str
    password: str

class Transaction(BaseModel):
    amount: float

# -------------------- Routes --------------------
@app.post("/create_account")
def create_account(account: AccountCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO bank_accounts (account_holder, account_number, password, balance) VALUES (%s,%s,%s,%s)",
            (account.account_holder, account.account_number, account.password, 0)
        )
        conn.commit()
        return {"message": "Account created successfully!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/login")
def login(login: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM bank_accounts WHERE account_number=%s AND password=%s",
        (login.account_number, login.password)
    )
    account = cursor.fetchone()
    cursor.close()
    conn.close()
    if account:
        return {"message": "Login successful", "account_holder": account["account_holder"]}
    else:
        raise HTTPException(status_code=401, detail="Invalid account number or password")

@app.post("/deposit/{account_number}")
def deposit(account_number: str, transaction: Transaction):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM bank_accounts WHERE account_number=%s", (account_number,))
    account = cursor.fetchone()
    if not account:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Account not found")

    new_balance = account[0] + transaction.amount
    cursor.execute("UPDATE bank_accounts SET balance=%s WHERE account_number=%s", (new_balance, account_number))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"{transaction.amount} deposited successfully", "new_balance": new_balance}

@app.post("/withdraw/{account_number}")
def withdraw(account_number: str, transaction: Transaction):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM bank_accounts WHERE account_number=%s", (account_number,))
    account = cursor.fetchone()
    if not account:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Account not found")

    if account[0] < transaction.amount:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Insufficient balance")

    new_balance = account[0] - transaction.amount
    cursor.execute("UPDATE bank_accounts SET balance=%s WHERE account_number=%s", (new_balance, account_number))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"{transaction.amount} withdrawn successfully", "new_balance": new_balance}

@app.get("/balance/{account_number}")
def check_balance(account_number: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM bank_accounts WHERE account_number=%s", (account_number,))
    account = cursor.fetchone()
    cursor.close()
    conn.close()
    if account:
        return {"balance": account[0]}
    else:
        raise HTTPException(status_code=404, detail="Account not found")

@app.get("/bank_accounts")
def get_all_accounts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, account_holder, account_number, balance FROM bank_accounts")
    accounts = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"bank_accounts": accounts}


