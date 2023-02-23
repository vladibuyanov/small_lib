from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length

from myapp.core.models.user import User


class SettingsForm(FlaskForm):
    def __init__(self, user_id, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        user = User.query.get(user_id)
        self.name.render_kw['placeholder'] = user.name
        self.email.render_kw['placeholder'] = user.email
        self.psw.render_kw['placeholder'] = '******'
        self.place.render_kw['placeholder'] = user.place

    name = StringField('Name', render_kw={'class': "form-control"})
    email = StringField('Email', validators=[Email()],
                        render_kw={'class': "form-control"})
    psw = PasswordField('Password', validators=[Length(min=4, max=100)],
                        render_kw={'class': "form-control"})
    place = StringField('Place', render_kw={'class': "form-control"})

