import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import User, Post

from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from flask import session
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

app = Flask(__name__)
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoppingmall.sqlite3'
app.config['SECRET_KEY'] = "software engineering"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect()
csrf.init_app(app)

# db = SQLAlchemy(app)

# class User(db.Model): # 데이터 모델을 나타내는 객체 선언
#     __tablename__ = 'user'

#     userid = db.Column(db.String(32), primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)

#     posts = db.relationship('Post', backref="author", lazy=True) # 이후 사용자를 user라는 변수에 저장하면, user.posts를 통해 사용자의 product(post)에 접근가능
#     # db.relationship(객체이름, post.author를 통해 product owner에게 접근 가능)

#     def __init__(self, userid, username, email, password):
#         self.userid = userid
#         self.username = username
#         self.email = email
#         self.set_password(password)

#     def __repr__(self):
#         return f"<user('{self.userid}', '{self.username}', '{self.email}')>"

#     def set_password(self, password):
#         self.password = generate_password_hash(password) # 문자열(비밀번호)을 암호화된 해시로 바꿔줌

#     def check_password(self, password):
#         return check_password_hash(self.password, password) # 암호화된 해시와 문자열을 비교해서 문자열이 동일한 해시를 갖는 경우 참을 반환


# class Post(db.Model):
#     __table_name__ = 'post'

#     userid = db.Column(db.String(32), primary_key=True)
#     keyword = db.Column(db.String(120), unique=True, nullable=False)
#     content = db.Column(db.Text)

#     user_id = db.Column(db.String(32), db.ForeignKey('user.userid')) # user 테이블의 id를 외래키로 하는 user_id 컬럼 생성


# 일단 하드코딩이에요 ~~ db 에서 가져오는 걸로 바꿀 것임
posts = [
    {
        'author': {
            'username': 'test-user'
        },
        'title': '첫 번째 포스트',
        'content': '첫 번째 포스트 내용입니다.',
        'date_posted': datetime.strptime('2018-08-01', '%Y-%m-%d')
    },
    {
        'author': {
            'username': 'test-user'
        },
        'title': '두 번째 포스트',
        'content': '두 번째 포스트 내용입니다.',
        'date_posted': datetime.strptime('2018-08-03', '%Y-%m-%d')
    },
]

@app.route('/')
def hello():
	return 'Hello World!'

@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html', posts=posts)

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    # form 관리 - WTF 패키지 이용
    form = RegisterForm()
    if form.validate_on_submit(): # 내용이 채워지지 않은 항목이 있는지 체크
        
        userid = form.data.get('userid')
        username = form.data.get('username')
        email = form.data.get('email')
        password = form.data.get('password')

        usertable = User(userid, username, email, password)

        db.session.add(usertable)
        db.session.commit()

        return "회원가입 완료"

    return render_template('registration.html', form=form)
    # if request.method == 'GET':
    #     return render_template("registration.html")
    # else:
    #     userid = request.form.get('userid')
    #     username = request.form.get('username')
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #     password2 = request.form.get('re_password')

    #     if not (userid and email and password and password2):
    #         return "입력되지 않은 정보가 있습니다."
    #     elif password != password2:
    #         return "비밀번호가 일치하지 않습니다."
    #     else:
    #         usertable = User(userid, username, email, password)
    #         db.session.add(usertable)
    #         db.session.commit()
    #         return "회원가입 완료"
    #     return redirect('/')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm() # 로그인폼
    if form.validate_on_submit() or request.method == 'POST':
        error = None
        usertable = User.query.filter_by(userid=form.userid.data).first()
        if not usertable:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(usertable.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['userid'] = form.data.get('userid') # form에서 가져온 userid를 세션에 저장
            return redirect('/mainpage')
        flash(error)

        # print('{} 로그인' .format(form.data.get('userid')))
        # session['userid'] = form.data.get('userid') # form에서 가져온 userid를 세션에 저장
        # return redirect('/mainpage')
    return render_template('login.html', form=form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.pop('userid', None)
    return redirect('/mainpage')


@app.route('/mypage')
def mypage():
    return render_template('mypage.html', title = 'mypage')


@app.route('/upload_product', methods = ['GET', 'POST'])
def upload_product():
    if request.method == 'POST':
        f = request.files['image']
        f.save(secure_filename(f.filename))
        return '상품이 업로드 되었습니다.'
    else:
        return render_template('upload_product.html', title = 'upload')


if __name__ == '__main__':
    
    db.create_all() # db 생성
    db.session.rollback()

    app.run(debug = True)

