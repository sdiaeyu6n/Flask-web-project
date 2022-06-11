from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# from app import login_manager
from flask_login import LoginManager, UserMixin

db = SQLAlchemy() # 데이터베이스 저장
login_manager = LoginManager()


class User(UserMixin, db.Model):
    __table_name__ = 'user'
 
    id = db.Column(db.Integer, primary_key=True) # 기본 키는 데이터타입 integer, 기본키로 설정한 속성은 자동으로 1씩 증가
    userid = db.Column(db.String(32), unique=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
 
    posts = db.relationship('Post', backref='author', lazy=True)# 이후 사용자를 user라는 변수에 저장하면, user.posts를 통해 사용자의 product(post)에 접근가능
    # db.relationship(객체이름, post.author를 통해 product owner에게 접근 가능)  
 
    def __init__(self, userid, username, email, password):
        self.userid = userid
        self.username = username
        self.email = email
    
        self.set_password(password)
    
    def __repr__(self):
            return f"<User('{self.id}', '{self.username}', '{self.email}')>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password) # 문자열(비밀번호)을 암호화된 해시로 바꿔줌

    def check_password(self, password):
        return check_password_hash(self.password, password) # 암호화된 해시와 문자열을 비교해서 문자열이 동일한 해시를 갖는 경우 참을 반환

 

class Post(db.Model):
    __table_name__ = 'post'
 
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(120))
    content = db.Column(db.Text)
    price = db.Column(db.Integer)
    # status = db.Column(db.String(10)) # 판매 or 품절
    # image = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
    def __repr__(self):
        # return f"<Post('{self.keyword}', '{self.content}', '{self.price}', '{self.status})>"
        return f"<Post('{self.keyword}', '{self.content}', '{self.price}')>"

    # def __init__(self, keyword, content, price):
    #     self.keyword = keyword
    #     self.content = content
    #     self.price = price