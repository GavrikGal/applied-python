from flask import render_template, session, Blueprint


bp = Blueprint('base', __name__)


@bp.route('/')
def entry_page() -> 'html':
    if 'username' in session:
        return render_template('index.html',
                               the_title='Привет! Это какой-то блог',
                               the_username=session['username'])
    else:
        return render_template('index.html',
                               the_title='Привет! Это какой-то блог', )


