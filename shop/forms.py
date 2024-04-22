from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,PasswordField
from wtforms.validators import DataRequired,Length, EqualTo

class ProductForm(FlaskForm):
    subject = StringField('상품 이미지', validators=[DataRequired('상품이미지은 필수입력 항목입니다.')])
    content = StringField('상품명', validators=[DataRequired('상품명은 필수입력 항목입니다.')])
    price = StringField('가격', validators=[DataRequired('가격은 필수입력 항목입니다.')])
    description = TextAreaField('상품 설명', validators=[DataRequired('상품설명은 필수입력 항목입니다.')])

class UserLoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    
class UserCreateForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    name = StringField('사용자이름', validators=[DataRequired(), Length(min=1, max=25)])
    address = StringField('주소', validators=[DataRequired(), Length(min=3, max=30)])
    