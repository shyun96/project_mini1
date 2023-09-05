from flask import Flask, render_template,request,redirect,url_for,session,flash
import sys
import database

app = Flask(__name__, static_folder='./resources/')
app.secret_key = 'secretkey'

@app.route('/', methods = ["GET", "POST"])
def index():
    #print(session['id'])
    board_data_lst = []
    board_data = database.get_board_data()
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
    
    if request.method == "POST":
        sorting_option = request.form['sorting_option']
        
        if sorting_option == "최신순":
            sorted_time_data_lst = sorted(board_data_lst, key=lambda x: x['create_time'])
            return render_template("index.html", data_lst = sorted_time_data_lst)
        
        else:
            sorted_views_data_lst = sorted(board_data_lst, key=lambda x: x['views'], reverse=True)
            return render_template("index.html", data_lst = sorted_views_data_lst)
            
    else:
        return render_template("index.html",data_lst=board_data_lst)


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
            return redirect(url_for('index',id_info = id_))
        else:
            flash("로그인 정보가 없습니다. 재로그인 해주세요. ")
            return redirect(url_for('login'))


    #return id_info

@app.route('/create')
def create_BB():
    return render_template('create.html')

@app.route('/detail/<id>',methods = ["GET"])
def detail(id):
    return render_template('detail.html',data=id)

@app.route('/signup')
def signup():
    return render_template('signup.html')

# @app.route('/applydata')
# def signup():
#     Name = request.args.get("NaMe")
#     username = request.args.get("userName")
#     password = request.args.get("userPassword")
#     TelePhone = request.args.get("TelePhone")
#     database.save(username,Name,TelePhone,password)
#     #print(user1)
#     #return user1
#     return render_template("m.html")

# @app.route('/dd',methods=['POST'])
# def main():
#     if request.method == 'POST':
#         return render_template('index.html')
#     return redirect(url_for(''))


if __name__ == '__main__':
    app.run(debug=True)
