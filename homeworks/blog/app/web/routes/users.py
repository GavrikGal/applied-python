from flask import render_template, request, redirect, Blueprint
from ...service import usersservice, password_service


bp = Blueprint('users', __name__)
users_service = usersservice.UsersService()
password_service = password_service


@bp.route('/users', methods=['GET'])
def users_page() -> 'html':

    users = users_service.all_users()

    if not users:
        return 'Error'

    contents = [(user.id, user.first_name, user.last_name, user.login) for user in users]

    titles = ('id', 'Имя', 'Фамилия', 'Логин')
    return render_template('users.html',
                           the_title='Управление пользователями',
                           the_row_title=titles,
                           the_data=contents,)


@bp.route('/add_user', methods=['POST'])
def add_user() -> 'html':

    users_service.add_user(request.form['first_name'],
                                      request.form['last_name'],
                                      request.form['login'],
                                      request.form['password'],)

    return redirect('users')

