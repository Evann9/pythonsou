import pymysql
import os

def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"), 
        port=int(os.getenv("DB_PORT", "3306")), 
        user=os.getenv("DB_USER", "root"), 
	    password=os.getenv("DB_PASSWORD", "123"), 
        database=os.getenv("DB_NAME", "coffeedb"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

def insert_survey(gender:str, age:int, co_survey:str) -> None:
    sql = "insert into survey (gender, age, co_survey) values (%s, %s, %s)"
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (gender, age, co_survey))
    finally:
        conn.close()

def fetchall_survey() -> list[dict]:
    sql = "select rnum, gender, age, co_survey from survey order by rnum asc"
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()
