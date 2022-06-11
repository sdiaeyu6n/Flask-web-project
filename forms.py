from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash

class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('password_2')]) #비밀번호 확인
    password_2 = PasswordField('repassword', validators=[DataRequired()])

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    # class UserPassword(object):
    #     def __init__(self, message=None):
    #         self.message = message
            
    #     def __call__(self, form, field):
    #         userid = form['userid'].data
    #         password = field.data
            
    #         usertable = User.query.filter_by(userid=userid).first()
    #         # print(usertable, userid, password, usertable.password)
    #         if not usertable:
    #             raise ValueError('존재하지 않는 사용자입니다.')
    #         elif not check_password_hash(usertable.password, form.password.data):
    #             raise ValueError('비밀번호가 올바르지 않습니다.')

    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class PostForm(FlaskForm):
    keyword = StringField('keyword', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])