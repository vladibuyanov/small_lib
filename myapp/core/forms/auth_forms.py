from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginFrom(FlaskForm):
    email = StringField('Email: ',
                        validators=[Email()],
                        render_kw={'class': "form-control"})
    psw = PasswordField('Password: ',
                        validators=[DataRequired(), Length(min=4, max=100)],
                        render_kw={'class': "form-control"})
    submit = SubmitField('Login',
                         render_kw={'class': "btn main-color font-color"})


class RegisterForm(FlaskForm):
    name = StringField('Name: ', render_kw={'class': "form-control"})
    email = StringField('Email: ', validators=[Email()], render_kw={'class': "form-control"})
    psw = PasswordField(
        'Password: ',
        validators=[DataRequired(), Length(min=4, max=100)],
        render_kw={'class': "form-control"}
    )
    psw_2 = PasswordField(
        'Confirm password: ',
        validators=[
            DataRequired(),
            EqualTo('psw', message='Incorrect password. Please, try again'),
        ],
        render_kw={'class': "form-control"}
    )
    submit = SubmitField('Registered', render_kw={'class': "btn main-color font-color"})
