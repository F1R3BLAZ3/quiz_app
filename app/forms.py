from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class QuestionForm(FlaskForm):
    question_text = StringField('Question', validators=[DataRequired()])
    answer_a = StringField('Answer A', validators=[DataRequired()])
    answer_b = StringField('Answer B', validators=[DataRequired()])
    answer_c = StringField('Answer C', validators=[DataRequired()])
    answer_d = StringField('Answer D', validators=[DataRequired()])
    correct_answer_id = SelectField('Correct Answer', 
                                     choices=[('1', 'Answer A'), 
                                              ('2', 'Answer B'), 
                                              ('3', 'Answer C'), 
                                              ('4', 'Answer D')], 
                                     validators=[DataRequired()])
    submit = SubmitField('Add Question')
