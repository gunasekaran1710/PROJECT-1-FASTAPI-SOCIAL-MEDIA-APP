import psycopg2
from psycopg2.extras import RealDictCursor
try:
    conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='password123',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print('database was connected successfully')
except Exception as error:
    print('connection to the databse is fail')
    print('ERROR:',error)