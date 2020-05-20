from flask import Blueprint, redirect, request, session, render_template
from ...service import blogs_service, usersservice, postservice
from .common import authenticated

bp = Blueprint('blogs', __name__)
blogs_service = blogs_service.Blogs_service()
user_service = usersservice.UsersService()
post_service = postservice.PostService()


@bp.route('/add_blog', methods=['POST'])
@authenticated
def add_blog() -> 'html':
    blogs_service.add_blog(request.form['blog_name'],
                           session['user_id'])

    return redirect('/user_blogs')


@bp.route('/update_blog', methods=['POST'])
@authenticated
def update_blog() -> 'html':
    blogs_service.update_blog(request.form['blog_id'],
                              request.form['blog_name'])
    return redirect('/user_blogs')


@bp.route('/cancel_update_blog')
def cancel_update_blog() -> 'html':
    return redirect('/user_blogs')


@bp.route('/user_blogs')
@authenticated
def user_blogs() -> 'html':
    blogs = user_service.find_by_id(session['user_id']).blogs
    blogs_titles = ('Название', 'Удалить', 'Редактировать')
    return render_template('user_blogs.html',
                           the_title='Тут все твои блоги',
                           the_blogs_titles=blogs_titles,
                           the_user_blogs=blogs,
                           the_username=session['user_name'])


@bp.route('/delete_blogs', methods=['POST'])
@authenticated
def delete_blogs() -> 'html':
    for id in request.form.getlist('delete_ids'):
        blogs_service.delete_blog_id(id)
    return redirect('/user_blogs')


@bp.route('/edit_blog/<blog_id>')
@authenticated
def edit_blog(blog_id):
    blog = blogs_service.find_by_id(blog_id)
    return render_template('edit_blog.html',
                           the_title='Тут можешь изменить свой блог',
                           the_blog_name=blog.name,
                           the_blog_id=blog.id,
                           the_username=session['user_name'])


@bp.route('/blog/<blog_id>')
def blog(blog_id):
    blog = blogs_service.find_by_id(blog_id)
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = None
    return render_template('blog.html',
                           the_title='Это блог',
                           the_blog_name=blog.name,
                           the_blog_id=blog.id,
                           the_blog_author=blog.user.first_name,
                           the_posts=blog.posts,
                           the_username=user_name)
