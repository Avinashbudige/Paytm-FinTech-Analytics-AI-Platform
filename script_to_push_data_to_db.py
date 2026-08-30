import sqlite3
import pandas as pd
import os

# read users data from CSV file
""" 
Load merchants.csv, users.csv, and ledger.csv into a normalized SQLite database paytm_payments.db 
with a schema that has 
    merchants(merchant_id PK, ...)
    users(user_id PK, signup_date)
    transactions(transaction_id PK, user_id FK, merchant_id FK, ...)

"""
base_path = os.path.dirname(os.path.abspath(__file__))
users_data = pd.read_csv(f'{base_path}/users.csv') 
transactions_data = pd.read_csv(f'{base_path}/ledger.csv')
merchants_data = pd.read_csv(f'{base_path}/merchants.csv') 



def push_data_to_db(data):  
    
    # create a connection to the SQLite database
    conn = sqlite3.connect(f'{base_path}/paytm_payments.db')
    cursor = conn.cursor()

    # create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS merchants (
            merchant_id INTEGER PRIMARY KEY,
            merchant_name TEXT,
            merchant_category TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            signup_date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            merchant_id INTEGER,
            amount REAL,
            transaction_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
        )
    ''')

    # insert data into tables
    data['merchants'].to_sql('merchants', conn, if_exists='replace', index=False)
    data['users'].to_sql('users', conn, if_exists='replace', index=False)
    data['transactions'].to_sql('transactions', conn, if_exists='replace', index=False)

    # commit changes and close the connection
    conn.commit()
    conn.close()
    
push_data_to_db({
    'merchants': merchants_data,
    'users': users_data,
    'transactions': transactions_data
})