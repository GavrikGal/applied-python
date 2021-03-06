from flask import render_template, session, Blueprint
from ...service import blogs_service


bp = Blueprint('base', __name__)
blogs_service = blogs_service.Blogs_service()


@bp.route('/')
def entry_page() -> 'html':

    blogs = blogs_service.all_blogs()
    blogs_titles = ('Название', 'Автор',)

    if 'user_name' in session:
        return render_template('index.html',
                               the_title='Список всех блогов',
                               the_blogs_titles=blogs_titles,
                               the_blogs=blogs,
                               the_username=session['user_name'])
    else:
        return render_template('index.html',
                               the_title='Список всех блогов',
                               the_blogs_titles=blogs_titles,
                               the_blogs=blogs,)


