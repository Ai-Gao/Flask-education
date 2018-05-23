# coding='utf-8'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import Length, Email, EqualTo, Required, Regexp, URL, NumberRange
from simpledu.models import db, User, Course, Live
from wtforms import ValidationError, TextAreaField, IntegerField

# 创建RegisterForm()表单类
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(message='用户名不能为空'), Length(3,24, message='用户名长度要在3~24个字符之间')])
    email = StringField('邮箱', validators=[Required(message='邮箱不能为空'), Email(message="请输入合法的email地址")])
    password = PasswordField('密码', validators=[Required(message='密码不能为空'),Length(6,24, message='密码长度要在6~24个字符之间') ])
    repeat_password = PasswordField('重复密码', validators=[Required(message='密码不能为空'), EqualTo('password', message='密码要相等') ])
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
# 自定义表单验证器

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')
"""
   # 创建用户用于用户信息的修改
    def create_user(self):
        user=User(username=self.username.data,
                  email=self.email.data,
                  password=self.password.data
                )
        db.session.add(user)
        db.session.commit()
        return user
"""

# 创建LoginForm()表单类
class LoginForm(FlaskForm):
    # email = StringField('邮箱', validators=[Required(),Email()])
    username = StringField('用户名', validators=[Required(), Length(3,24, message=('用户名长度要在3~24位'))])
    password = PasswordField('密码', validators=[Required(), Length(6,24, message='密码长度要在6~24位')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

# 自定义验证邮箱是否存在及密码是否正确

  #  def validate_email(self, field):
  #      if field.data and not User.query.filter_by(email=field.data).first():
  #          raise ValidationError('该邮箱未注册')


# 自定义验证用户名是否存在
    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名未注册')

# 自定义验证密码是否正确
    def validate_password(self, field):
        #user = User.query.filter_by(email=self.email.data).first()
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

# 创建CourseForm 用于课程的添加编辑
class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[Required(),Length(5, 32)])
    description = TextAreaField('课程简介', validators=[Required(), Length(20, 256)])
    image_url = StringField('封面图片', validators=[Required(), URL()])
    author_id = IntegerField('作者ID', validators=[Required(), NumberRange(min=1,message='无效的用户ID')])
    submit = SubmitField('提交')

    course = None

   # 创建课程时,编辑课程时都需要验证
    def validate_author_id(self, field):
        # 首先判断当前author是否存在,继而对课程进行编辑,删除操作

        if not self.course or self.course.author_id != field.data:
            if Course.query.filter_by(author_id=field.data).first():
                raise ValidationError('用户已存在')

        if not User.query.get(field.data):
            raise ValidationError('无效的用户ID')

    # 验证添加的课程是否已经存在
    # 验证已有的属性
    def validate_name(self, field):
        if not self.course or self.course.name != field.data:
            if Course.query.filter_by(name=field.data).first():
                raise ValidationError('课程已经存在')

        #if Course.query.filter_by(name = field.data).first():
        #    raise ValidationError('课程已经存在')

    #def validate_author_id(self, field):
    #    if not self.course or self.course.author_id != field.data:
    #        if Course.query.filter_by(field.data):
    #            raise ValidationError('用户ID已经存在')

    # 定义一个方法保存未修改的数据对象
    def set_course(self, course):
        self.course = course

    def create_course(self):
        course = Course()
        # 使用课程表单数据填充 course 对象
        # 使用表单字段中的数据填充传递的obj
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

# 创建添加用户表单
class UserForm(FlaskForm):

    username = StringField('用户名', validators=[Required(), Length(3,24)])
    #id = IntegerField('用户ID', validators=[Required(), NumberRange(min=1, message='无效的用户ID')])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    role = IntegerField('用户角色', validators=[Required(),NumberRange(min=1, message='无效的用户角色')])
    job = StringField('工作', validators=[Required(), Length(3,24)])
    img = StringField('头像', validators=[Required()])
    submit = SubmitField('提交')

    user = None
    def validate_username(self,field):
        #创建user 验证,update user 并且字段值发生改变
        if not self.user or self.user.username != field.data:
            if User.query.filter_by(username = field.data).first():
                raise ValidationError('用户名字已经存在')

    def set_user(self,user):
        self.user= user

    def validate_email(self,field):
        if self.user and self.user.email != field.data:
            if User.query.filter_by(email = field.data).first():
                raise ValidationError('邮箱已经存在')

    def create_user(self):
        user=User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self,user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

# 定义LiveForm
class LiveForm(FlaskForm):
    name = StringField('直播名', validators=[Required(), Length(3,24)])
    up_id = IntegerField('用户ID', validators=[Required(), NumberRange(min=1, message='无效的用户ID')])
    live_url = StringField('直播地址', validators=[Required(), URL()])
    submit = SubmitField('提交')

# 自定义验证函数 直播名
    def validate_name(self, field):
        if Live.query.filter_by(name=field.data).first():
            raise ValidationError('直播名已存在')

    def validate_id(self, field):
        #if User.query.filter_by(id=field.data).first():
        #    raise ValidationError('用户名已存在')
        if not User.query.get(field.data):
            raise ValidationError('无效的用户ID')

    # 添加直播到数据库
    def create_live(self):
        live = Live()
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live

# 自动以验证函数 message
class MessageForm(FlaskForm):
    text = StringField('系统消息', validators=[Required(), Length(1,256)])
    submit = SubmitField('提交')
