from myapp import Book, User
from myapp.core.forms.search_forms import SearchForm


def main_func() -> list:
    user_res = User.query.limit(3).all()
    books_res = Book.query.limit(3).all()
    return [user_res, books_res]


def search_func(request):
    form = SearchForm()

    if request.method == 'GET':
        return form

    if form.validate_on_submit():
        searched = form.searched.data

        is_books = Book.query.filter(Book.title.like(f'%{searched}%'))
        is_user = User.query.filter(User.name.like(f'%{searched}%'))

        is_books = is_books.order_by(Book.title).all()
        is_user = is_user.order_by(User.name).all()

        return form, is_books, is_user
