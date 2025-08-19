import os
import psycopg2
from dotenv import load_dotenv

# 資料庫連線設定
def get_connection():
    load_dotenv()
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DB")
    )
    
def query_user(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT username FROM users WHERE username = %s", (username,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def query_user_and_password(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT username, password FROM users WHERE username = %s AND password = %s", (username, password))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def insert_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_user(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
    finally:
        cur.close()
        conn.close()