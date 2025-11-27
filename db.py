import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
# .env 파일 불러오기
load_dotenv()

def get_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
    )
    return conn

# --- SELECT 쿼리 ---
def fetch(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows)

# --- INSERT, UPDATE, DELETE (Commit 필요) ---
def execute(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
