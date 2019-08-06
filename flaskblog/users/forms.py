from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=32)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=255)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #custom validators----------------------------------------
    def validate_password(self, password):
        if not (any(x.isupper() for x in password.data) and any(x.islower() for x in password.data) and any(x.isdigit() for x in password.data)):
            raise ValidationError('Password must cointain at least one number, one capital letter and one lower case letter.')
    
    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first() is not None:
            raise ValidationError('Username already in use. Try another')
    
    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first() is not None:
            raise ValidationError('Email already in use. Try another')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=32)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['png','jpg'])])
    submit = SubmitField('Update')

    #custom validators----------------------------------------
    def validate_username(self,username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first() is not None:
                raise ValidationError('Username already in use. Try another')
        
    def validate_email(self,email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first() is not None:
                raise ValidationError('Email already in use. Try another')



#Reset
class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    

    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first() is None:
            raise ValidationError('Account with that email does not exist. Register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=255)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

    def validate_password(self, password):
        if not (any(x.isupper() for x in password.data) and any(x.islower() for x in password.data) and any(x.isdigit() for x in password.data)):
            raise ValidationError('Password must cointain at least one number, one capital letter and one lower case letter.')
 