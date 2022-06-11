import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import User, Post
from flask_login import LoginManager, current_user
from flask_login import UserMixin
from models import login_manager

# from flask_migrate import Migrate

from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from flask import session
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm, PostForm, EmptyForm

app = Flask(__name__)
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoppingmall.sqlite3'
app.config['SECRET_KEY'] = "software engineering"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# login_manager = LoginManager(app)
# login_manager.login_view = 'auth.login'

login_manager.init_app(app)
csrf = CSRFProtect()
csrf.init_app(app)


# 일단 하드코딩이에요 ~~ db 에서 가져오는 걸로 바꿀 것임
# posts = [
#     {
#         'author': {
#             'username': 'test-user'
#         },
#         'title': '첫 번째 포스트',
#         'content': '첫 번째 포스트 내용입니다.',
#         'date_posted': datetime.strptime('2018-08-01', '%Y-%m-%d')
#     },
#     {
#         'author': {
#             'username': 'test-user'
#         },
#         'title': '두 번째 포스트',
#         'content': '두 번째 포스트 내용입니다.',
#         'date_posted': datetime.strptime('2018-08-03', '%Y-%m-%d')
#     },
# ]

@app.route('/')
def hello():
    posts = Post.query.all()
    return render_template('mainpage.html', posts=posts)

@app.route('/testpage')
def testpage():
    users = User.query.all()
    posts = Post.query.all()
    return render_template('testpage.html', users = users, posts = posts)


@app.route('/mainpage')
def mainpage():
    userid = session.get('userid', None)
    posts = Post.query.all()
    return render_template('mainpage.html', userid=userid, posts = posts)

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
    form = PostForm()
    if form.validate_on_submit():

        keyword = form.data.get('keyword')
        content = form.data.get('content')
        price = form.data.get('price')
        u = User.query.get(1)
    
        # userid = current_user._get_current_object()

        posttable = Post(keyword=keyword, content=content, price=price, author=u)

        db.session.add(posttable)
        db.session.commit()

        # f = request.files['image']
        # f.save(secure_filename(f.filename))
        return '상품이 업로드 되었습니다.'
    
    return render_template('upload_product.html', title='upload', form=form)

# @app.route('/follow/<username>', methods=['POST'])
# def follow(username):
#     form = EmptyForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=username).first()
#         if user is None:
#             flash('User {} not found.'.format(username))
#             return redirect(url_for('mainpage'))
#         if user == current_user:
#             flash('You cannot follow yourself!')
#             return redirect(url_for('user', username=username))
#         current_user.follow(user)
#         db.session.commit()
#         flash('You are following {}!'.format(username))
#         return redirect(url_for('mypage', username=username))
#     else:
#         return redirect(url_for('mainpage'))


# @app.route('/unfollow/<username>', methods=['POST'])
# def unfollow(username):
#     form = EmptyForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=username).first()
#         if user is None:
#             flash('User {} not found.'.format(username))
#             return redirect(url_for('mainpage'))
#         if user == current_user:
#             flash('You cannot unfollow yourself!')
#             return redirect(url_for('user', username=username))
#         current_user.unfollow(user)
#         db.session.commit()
#         flash('You are not following {}.'.format(username))
#         return redirect(url_for('mypage', username=username))
#     else:
#         return redirect(url_for('mainpage'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # db 생성
    db.session.rollback()

    app.run(debug = True)