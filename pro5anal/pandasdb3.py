# pandas의 DataFrame 자료를 원격 Db 테이블에 저장
# pip install sqlalchemy
import pandas as pd
from sqlalchemy import create_engine
import pymysql

data = {
    'code':[1,2,3,4,5,10,11,12],
    'sang':['장갑','벙어리장갑','가죽장갑','가죽점퍼','사이다','콜라','맥주','와인'],
    'su':[3,4,10,5,25,20,22,7],
    'dan':[10000,12000,50000,650000,3000,2300,10000,70000]
}
try:
    frame = pd.DataFrame(data)
    print(frame)

    engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/test?charset=utf8mb4")

    # 저장
    frame.to_sql(name='sangdata', con=engine, if_exists='replace', index=False)

    # 읽기
    df = pd.read_sql('select * from sangdata', engine)
    print(df)
    
except Exception as e:
    print('처리 오류 :', e)

"""
.env 파일
DB_USER=root
DB_PASSWORD=123

from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:\
    {os.getenv('DB_PASSWORD')}@127.0.0.1:3306/test?charset=utf8mb4"
)
"""
