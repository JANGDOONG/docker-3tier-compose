from flask import Flask, jsonify
import pymysql
import os
from datetime import datetime

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/db")
def db_check():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            connect_timeout=3
        )
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()
        conn.close()
        return jsonify(db="ok")
    except Exception as e:
        return jsonify(db="fail", error=str(e)), 500

@app.route("/time")
def time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(time=now)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

