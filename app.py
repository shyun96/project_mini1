from flask import Flask, render_template,request,redirect,url_for
import sys
import database

app = Flask(__name__, static_folder='./resources/')

@app.route('/', methods = ["GET", "POST"])
def index():
    dic = {
        'img' : '/resources/aaa.jpg',
        'topic' : '보노보노 미침',
        'view' : 30,
        'cmt' : 75,
        'usrname' : '냉철한해물칼국수'
    }
    dic2 = {
        'img' : '/resources/ddddd.jpg',
        'topic' : '보노보노',
        'view' : 40,
        'cmt' : 40,
        'usrname' : '냉철한박광민칼국수'
    }
    
    data_lst = []
    data_lst.append(dic)
    data_lst.append(dic2)
    
    if request.method == "POST":
        sorting_option = request.form['sorting_option']
        #print(sorting_option)
        if sorting_option == "최신순":
            return render_template("index.html", data_lst = data_lst)
        else:
            sorted_data_lst = sorted(data_lst, key=lambda x: x['view'], reverse=True)
            #sorted_data_lst = sorted(data_lst.items(),key = lambda x:x[2],reverse = True)
            return render_template("index.html", data_lst = sorted_data_lst)
            
    else:
        return render_template("index.html",data_lst=data_lst)


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/create')
def create_BB():
    return render_template('create.html')

@app.route('/detail/<aa>',methods = ["GET"])
def detail(aa):
    #data = request.args.get('data')
    print(aa)
    return render_template('detail.html',data=aa)

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