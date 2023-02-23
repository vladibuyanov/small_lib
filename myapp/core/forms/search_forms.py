from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    searched = StringField('Searched', render_kw={'class': ""})
    submit = SubmitField('Search', render_kw={'class': "font-color main-color"})
