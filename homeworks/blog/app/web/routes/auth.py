from flask import request, redirect, session, Blueprint, g
from ...service import usersservice, password_service


bp = Blueprint('auth', __name__)
users_service = usersservice.UsersService()


@bp.route('/sign_in', methods=['POST'])
def sign_in() -> 'html':
    user = users_service.find_by_login(request.form['sign_login'])
    if not user:
        return redirect('/sign_out')
    if password_service.verify_password(user.password_hash, request.form['sign_password']):
        session['user_name'] = user.first_name
        session['user_id'] = user.id
    else:
        return redirect('/sign_out')
    return redirect('/')


@bp.route('/sign_out', methods=['GET'])
def sign_out() -> 'html':
    if 'user_name' in session:
        del session['user_name']
        del session['user_id']
    return redirect('/')
