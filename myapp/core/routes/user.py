from flask import Blueprint, render_template, request,  redirect, url_for
from flask_login import login_required, current_user

from myapp.core.functions.user import user_page_func, user_exchange_history_func, \
    user_settings_func, user_delete_func

users = Blueprint('users', __name__)

methods = ['GET', 'POST']
base_url = '/user'
redirect_page = 'main.main_view'
template_path = 'pages/user'


@users.route(f'{base_url}/<int:user_id>')
def user_page_view(user_id):
    template = f'{template_path}/user_page.html'
    data = user_page_func(user_id)
    return render_template(template, users=data[0], user=data[1], user_books=data[2], borrowed_books=data[3])


@users.route(f'{base_url}/<int:user_id>/exchange_history')
@login_required
def user_exchange_history_view(user_id):
    template = f'{template_path}/exchange_history.html'
    data = user_exchange_history_func(user_id)

    return render_template(
        template, users=data[0], books=data[1], users_requests=data[2],
        my_requests=data[3], user_id=user_id
    )


@users.route(f'{base_url}/user_settings/<int:user_id>', methods=methods)
@login_required
def user_settings_view(user_id):
    if current_user.id != user_id:
        return redirect(url_for(redirect_page))

    template = f'{template_path}/user_settings.html'
    user = user_settings_func(request, user_id)

    if request.method == 'GET':
        return render_template(template, user_settings=user[0], form=user[1])
    else:
        return redirect(url_for(redirect_page, user_id=user_id))


@users.route(f'{base_url}/user_settings/delete/<int:user_id>', methods=methods)
@login_required
def user_delete_view(user_id):
    user_delete_func(user_id)
    return redirect(url_for(redirect_page))
