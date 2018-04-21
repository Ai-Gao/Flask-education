# coding='utf-8'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, Required
from simpledu.models import db, User
from wtforms import ValidationError

# 创建RegisterForm()表单类
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3,24), message='用户名长度要在3~24位'])
    email = StringField('邮箱', validators=[Required(), Email(message="请输入合法的email地址")])
    password = PasswordField('密码', validators=[Required(),Length(6,24), message='密码长度要在6`24位'])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password'), message='密码不相等'])
    submit = SubmitField('提交')

# 实现注册功能 (根据表单提交的数据创建用户)
    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

# 在注册表单中验证某些表单是否已经存在(使用 validationsError)
# field.data 获取表单数据

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


# 创建LoginForm()表单类
class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(),Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

# 自定义验证邮箱是否存在及密码是否正确

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')

    # Q self.email.data
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
