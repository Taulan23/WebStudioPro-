from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, URL, NumberRange, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ContentForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=2, max=100)])
    content_type = SelectField('Тип контента', choices=[('lecture', 'Лекция'), ('course', 'Курс'), ('presentation', 'Презентация'), ('test', 'Тест')], validators=[DataRequired()])
    category = StringField('Категория', validators=[DataRequired(), Length(min=2, max=50)])
    url = StringField('URL', validators=[DataRequired(), URL()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Добавить контент')

class RatingForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Rating')

class OptionForm(FlaskForm):
    text = StringField('Вариант ответа', validators=[DataRequired()])
    is_correct = BooleanField('Правильный ответ')

class QuestionForm(FlaskForm):
    text = TextAreaField('Вопрос', validators=[DataRequired()])
    options = FieldList(FormField(OptionForm), min_entries=4)

class TestForm(FlaskForm):
    title = StringField('Название теста', validators=[DataRequired()])
    description = TextAreaField('Описание теста', validators=[DataRequired()])
    questions = FieldList(FormField(QuestionForm), min_entries=6)
    submit = SubmitField('Создать тест')

class LectureForm(FlaskForm):
    title = StringField('Название лекции', validators=[DataRequired()])
    description = TextAreaField('Описание лекции', validators=[DataRequired()])
    content = TextAreaField('Содержание лекции', validators=[DataRequired()])
    submit = SubmitField('Создать лекцию')
