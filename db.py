import mysql.connector
import pandas as pd

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="k1g2h3123@",
        database="ChatAnalysis",
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
