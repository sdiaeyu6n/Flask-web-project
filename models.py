from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy() # 데이터베이스 저장

class User(db.Model): # 데이터 모델을 나타내는 객체 선언
    __tablename__ = 'user'

    userid = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    posts = db.relationship('Post', backref="author", lazy=True) # 이후 사용자를 user라는 변수에 저장하면, user.posts를 통해 사용자의 product(post)에 접근가능
    # db.relationship(객체이름, post.author를 통해 product owner에게 접근 가능)

    def __init__(self, userid, username, email, password):
        self.userid = userid
        self.username = username
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return f"<user('{self.userid}', '{self.username}', '{self.email}')>"

    def set_password(self, password):
        self.password = generate_password_hash(password) # 문자열(비밀번호)을 암호화된 해시로 바꿔줌

    def check_password(self, password):
        return check_password_hash(self.password, password) # 암호화된 해시와 문자열을 비교해서 문자열이 동일한 해시를 갖는 경우 참을 반환


class Post(db.Model):
    __table_name__ = 'post'

    userid = db.Column(db.String(32), primary_key=True)
    keyword = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text)

    user_id = db.Column(db.String(32), db.ForeignKey('user.userid')) # user 테이블의 id를 외래키로 하는 user_id 컬럼 생성
