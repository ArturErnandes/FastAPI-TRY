import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()

conn = psycopg2.connect(
    dbname = "bd_try",
    user = "postgres",
    password = os.getenv("PASS"),
    host = "localhost",
    port = 5555
)


cursor = conn.cursor()

cursor.execute('SELECT * FROM main')
print(cursor.fetchall())