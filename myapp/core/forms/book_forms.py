from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField

from myapp.core.models.book import Book


class BookAddForm(FlaskForm):
    title = StringField('Book', render_kw={'class': ""})
    author = StringField('Author', render_kw={'class': ""})
    year_of_publication = StringField('Year of Publication', render_kw={'class': ""})
    about = TextAreaField('About', render_kw={'class': '', 'rows': 8})


class BookChangeForm(FlaskForm):
    def __init__(self, book_id=None, *args, **kwargs):
        super(BookChangeForm, self).__init__(*args, **kwargs)
        if book_id:
            book = Book.query.get(book_id)
            self.title.render_kw['placeholder'] = book.title
            self.author.render_kw['placeholder'] = book.author
            self.year_of_publication.render_kw['placeholder'] = book.year_of_publication
            self.about.render_kw['placeholder'] = book.about

    title = StringField('Book', render_kw={'class': ""})
    author = StringField('Author', render_kw={'class': ""})
    year_of_publication = StringField('Year of Publication', render_kw={'class': ""})
    about = TextAreaField('About', render_kw={'class': '', 'rows': 8})

