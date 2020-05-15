from flask import request, redirect, session, Blueprint
from ...service import users_service, password_service


bp = Blueprint('auth', __name__)
users_service = users_service.Users_service()
password_service = password_service


@bp.route('/sign_in', methods=['POST'])
def sign_in() -> 'html':
    user = users_service.find_by_login(request.form['sign_login'])
    if not user:
        return redirect('/sign_out')
    if password_service.verify_password(user.password_hash, request.form['sign_password']):
        session['username'] = user.first_name
    else:
        return redirect('/sign_out')
    return redirect('/')


@bp.route('/sign_out', methods=['GET'])
def sign_out() -> 'html':
    if 'username' in session:
        del session['username']
    return redirect('/')
