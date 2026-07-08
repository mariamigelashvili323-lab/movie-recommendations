from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed
from choices import choices


class RegisterForm(FlaskForm):

    username = StringField("შეიყვანე მომხმარებლის სახელი", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("შეიყვანე იმეილი", validators=[DataRequired(), Email()])
    password = PasswordField("შეიყვანე პაროლი", validators=[DataRequired(), Length(min=8, max=20,
                                                                                   message="PASSWORD MUST INCLUDE MINIMUM-8 SYMBOLS AND MAXIMUM-20")])
    repeat_password = PasswordField("გაიმეორე პაროლი", validators=[DataRequired(), EqualTo("password")])
    gender = RadioField("აირჩიე სქესი", choices=[('female', 'ქალი'), ('male', 'კაცი')], validators=[DataRequired()])
    country = SelectField(choices=choices)
    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
   
    username = StringField("შეიყვანე მომხმარებლის სახელი", validators=[DataRequired()])
    password = PasswordField("შეიყვანე პაროლი", validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField("შესვლა")


class MovieForm(FlaskForm):
    title = StringField("ფილმის/სერიალის სახელი", validators=[DataRequired(), Length(max=100)])
    genre = StringField('ჟანრი', validators=[DataRequired(), Length(max=55)])
    director = StringField("რეჟისორი", validators=[DataRequired(), Length(max=55)])
    image_url = StringField('ფოტოს ლინკი (სურვილისამებრ)', validators=[Length(max=300)])
    year = IntegerField('გამოშვების წელი', validators=[DataRequired()])
    submit = SubmitField('ფილმის დამატება')


class UpdateProfileForm(FlaskForm):
    username = StringField('ახალი სახელი', validators=[DataRequired(), Length(min=2, max=50)])
    avatar = FileField('პროფილის ფოტო', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'მხოლოდ სურათები!')])
    submit = SubmitField('პროფილის განახლება')