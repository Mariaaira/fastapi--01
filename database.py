# Database component is used to quickly and easily connect to databases such as PostgreSQL and MongoDB.
# It allows you to use familiar ORM-like querying methods,
# provides powerful data validation, supports asynchronous operations and much more.
import pymysql
# easily connect to databases such as PostgreSQL
# use familiar ORM-like querying methods
# provides powerful data validation

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:1234@localhost:3306/fastapi'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db1 = SessionLocal()
    try:
        yield db1
    finally:
        db1.close()


while True:

    try:
        db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='1234',
            db='fastapi',
            )
        print('Connected')
        break
    except Exception:
        raise Exception("Connection failed")

cursor = db.cursor()