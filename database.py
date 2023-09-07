
from pymysql import connect
import datetime

connectionString = {
    'host': '172.20.132.197',
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

def signup(id, password, name, phone):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = f"""INSERT INTO user (id,password, name,phone) VALUES("{id}","{password}","{name}","{phone}")"""
            print(cursor.execute(sql))
            con.commit()
            
    except Exception as e:
        print(e)
        
def checkid_duplicate(id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM user " + "where id = %s;"
            cursor.execute(sql, [id])
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
            sql = f"select id, image, created_time, content, views, title, user_id, (select count(*) from shop.reply as sr where sr.board_id = sb.id) as cmt from shop.board as sb where sb.id = {id};"
            cursor.execute(sql)
            detail_data = cursor.fetchone()
            #print(detail_data)
        return detail_data
    
    except Exception as e:
        print(e)


def post_board_data(user_id,title,content,filename):
    #print("here")
    #print(title,content)
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = f"""INSERT INTO shop.board (image,created_time,content,views,title,user_id) VALUES("{filename}",now(),"{content}",0,"{title}","{user_id}")"""
            cursor.execute(sql)
            con.commit()
            
    except Exception as e:
        print(e)

        
def comments(user_id, comment, board):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            sql = """INSERT INTO reply (user_id, board_id ,content, created_time) VALUES(%s, %s, %s, %s )"""
            cursor.execute(sql, [user_id, board, comment ,now ])
            con.commit()
    except Exception as e:
        print(e)
        
def get_comments(board):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT user_id, content, created_time FROM reply " + "where board_id = %s;"  
            cursor.execute(sql, [board])
            detail_data = cursor.fetchall()
            #print(detail_data)
        return detail_data   
    except Exception as e:
        print(e)

def count_view(board_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = f"UPDATE shop.board SET views = views + 1 WHERE id = {board_id};"
            cursor.execute(sql)
            con.commit()
            
    except Exception as e:
        print(e)

# mypage
def get_mypage(id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT title FROM shop.board WHERE user_id = %s;"
            cursor.execute(sql, [id])
            posts = cursor.fetchall()
            
            post_titles = [post[0] for post in posts]
            
            return post_titles
    
    except Exception as e:
        print(e)
 
 
# edit
def get_edit(title):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT id, created_time, content, title FROM shop.board WHERE title = %s;"
            cursor.execute(sql, [title])
            edit_data = cursor.fetchone()
        
            return edit_data
        print(title)
    except Exception as e:
        print(e)
       

def get_user_info(user_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = f""" select * from shop.user where id = "{user_id}"; """
            cursor.execute(sql)
            user_info = cursor.fetchone()
            print(user_info)
        return user_info
        
    except Exception as e:
        print(e)

def update_user_info(before_user_id, after_user_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = f"""UPDATE shop.user SET id = "{after_user_id}" WHERE id = "{before_user_id}";"""
            cursor.execute(sql)
            con.commit()
            
    except Exception as e:
        print(e)


def delete_user_info(user_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = f""" delete from shop.user where id = "{user_id}"; """
            cursor.execute(sql)
            con.commit()
            
    except Exception as e:
        print(e)
    