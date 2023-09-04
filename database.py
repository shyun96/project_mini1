
from pymysql import connect

connectionString = {
    'host': '172.20.132.169',
    'port': 3306,
    'database': 'shop',
    'user': 'user1',
    'password': '1234',
    'charset': 'utf8'
}

#POST요청
def create_db(username,Name,TelePhone,password):
    #print(username,Name,TelePhone,password)
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = f"""INSERT INTO user (id,name,phone,password) VALUES("{username}","{Name}","{TelePhone}","{password}")"""
            print(cursor.execute(sql))
            con.commit()
            
    except Exception as e:
        print(e)

#GET요청
# def read_db()
    
    