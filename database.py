
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
        
#로그인 체크
def id_check(user_id, pwd):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM user " + "where id = %s and password = %s;"
            cursor.execute(sql, [user_id, pwd])
            result = cursor.fetchall()
            print(result)
            return result
    except Exception as e:
        print(e)


#GET요청
def get_main_data():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            #sql = "select * from shop.board"
            sql = "select id, image, created_time, content, views, title, user_id, (select count(*) from shop.reply as sr where sr.board_id = sb.id) as cmt from shop.board as sb;"
            cursor.execute(sql)
            board_data = cursor.fetchall()
            #print(board_data)
            #cursor.close()
            #con.close()
            
        return board_data
            
    except Exception as e:
        print(e)
        
def get_detail_data(id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = ""
            cursor.execute(sql)
            detail_data = cursor.fetchall()
        return detail_data
    
    except Exception as e:
        print(e)

    
    