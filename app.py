from flask import Flask, render_template,request,redirect,url_for,session,flash
import sys
import database, img_resize
from os import path
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='./resources/')
app.secret_key = 'secretkey'
UPLOAD_FOLDER = path.join('.', 'resources/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods = ["GET", "POST"])
def index():
    #print(session['id'])
    board_data_lst = []
    board_data = database.get_main_data()
    for data in board_data:
        data_dic = {
            'id' : data[0],
            'image' : data[1],
            'create_time' : data[2],
            'content' : data[3],
            'views' : data[4],
            'title' : data[5],
            'user_id' : data[6],
            'comment_cnt' : data[7]
        }
        board_data_lst.append(data_dic)
    print(board_data_lst)
    if request.method == "POST":
        sorting_option = request.form['sorting_option']
    
        if sorting_option == "최신순":
            sorted_time_data_lst = sorted(board_data_lst, key=lambda x: x['create_time'], reverse=True)
            if 'id' in session:
                return render_template("index.html", data_lst = sorted_time_data_lst, id = session['id'])
            else:
                return render_template("index.html", data_lst = sorted_time_data_lst)
        else:
            sorted_views_data_lst = sorted(board_data_lst, key=lambda x: x['views'], reverse=True)
            if 'id' in session:
                return render_template("index.html", data_lst = sorted_views_data_lst, id = session['id'])
            else:
                return render_template("index.html", data_lst = sorted_views_data_lst)
        
    else:
        sorted_time_data_lst = sorted(board_data_lst, key=lambda x: x['create_time'], reverse=True)
        if 'id' in session:
            return render_template("index.html",data_lst=sorted_time_data_lst, id = session['id'])
        else: 
            return render_template("index.html",data_lst=sorted_time_data_lst)


@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        id_ = request.form['id']
        pwd = request.form['password']

        isid = database.id_check(id_, pwd)
        if(isid) :
            session['id'] = id_
            return redirect(url_for('index'))
        else:
            flash("로그인 정보가 없습니다. 재로그인 해주세요. ")
            return redirect(url_for('login'))

@app.route('/logout', methods = ["GET"])     
def logout():
    session.clear()
    print("here")
    return redirect(url_for('index'))
    #return id_info

@app.route('/create', methods=['POST','GET'])
def create_board_data():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        img_file = request.files['image']
        print('------------------------')
        print(title,content,img_file)
        print(img_file.filename)
        print('------------------------')
        #https://stackoverflow.com/questions/58720113/flask-resfull-app-permission-error-on-file-save 참조
        img_file.save(path.join(app.config['UPLOAD_FOLDER'], secure_filename(img_file.filename)))
        ImgFile = '/resources/' + img_file.filename
        img_resize.img_resize('.'+ ImgFile)
        #ImgFile = '/resources/' + img_file.filename
        database.post_board_data(session['id'],title,content,ImgFile)
        #database.post_board_data(sess,title,content,img_file.filename)
        return redirect(url_for('index'))
    else:
        return render_template('create.html')

@app.route('/detail/<id>',methods = ["POST","GET"])
def detail(id):
    print(333333333333333333333)
    if request.method == "GET":
        database.count_view(id)
        detail_data = database.get_detail_data(id)
        detail_data_dic = {
            'id' : detail_data[0],
            'image' : detail_data[1],
            'create_time' : detail_data[2],
            'content' : detail_data[3],
            'views' : detail_data[4],
            'title' : detail_data[5],
            'user_id' : detail_data[6],
            'comment_cnt' : detail_data[7]
            }
        reply_data_lst = []
        reply_data = database.get_comments(id)
        for data in reply_data:
            reply_data_dic = {
                'user_id' : data[0],
                'content' : data[1],
                'created_time' : data[2]
            }
            reply_data_lst.append(reply_data_dic)
        print(reply_data_lst)
        return render_template('detail.html',data=detail_data_dic, reply_data = reply_data_lst)
    else :
        content = request.form['content']
        print("-----------")
        print(content)
        print("------------------")
        user_id = session['id'] # 현재 로그인한 사용자의 ID 가져오기
        database.comments(user_id, content, id)
        return redirect(url_for("detail", id = id))
        #print(detail_data_dic)


@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        id_ = request.form['id']
        pwd = request.form['password']
        name_ = request.form['name']
        phone_ = request.form['phone']
        
        isid = database.checkid_duplicate(id_)
        if(isid) :
            flash("중복된 아이디 입니다. ")
            return redirect(url_for('signup'))
        else:
            database.signup(id_, pwd, name_, phone_)
            flash("회원가입 되셨습니다. ")
            session['id'] = id_
            return redirect(url_for('index'))

# mypage
@app.route('/mypage')
def mypage():
    # 로그인 상태 확인
    id = session.get('id')

    # 사용자가 작성한 글 목록 가져오기 (제목만)
    titles = database.get_mypage(id) 
    
    return render_template('mypage.html', id=id, titles=titles)


# edit
@app.route('/edit/<string:title>', methods=["POST", "GET"])
def edit(title):
    
    # if request.method == "GET":
    #     database.count_view(title)
    #     edit_data = database.get_edit(title)
    #     edit_data_dic = {
    #         'id': edit_data[0],
    #         'create_time': edit_data[1],
    #         'content': edit_data[2],
           
    #     }
    #     return render_template('edit.html', data=edit_data_dic)
    
    request.method == "GET"
        
    database.count_view(title)
    edit_data = database.get_edit(title)
    edit_data_dic = {

        'id': edit_data[0],
        'create_time': edit_data[1],
        'content': edit_data[2],
        'title' : edit_data[3]
        
        }
    return render_template('edit.html', data=edit_data_dic)
    
    # else:
    #     content = request.form['content']
    #     print("-----------")
    #     print(content)
    #     print("------------------")
    #     id = session['id']  # 현재 로그인한 사용자의 ID 가져오기
    #     database.comments(id, content)
    #     return redirect(url_for("edit", title=title))




# edit
# @app.route('/edit_post/<user_id>/<post_title>', methods=['GET', 'POST'])
# def edit_post(user_id, post_title):

#     try:
#         return  database.get_post(user_id, post_title) 
    
   
        
   
#         post = database.get_post(user_id, post_title)
#     except Exception as e:
#         print(e)
    
#     return render_template('edit_post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
