from flask import Blueprint, redirect, request, session, render_template
from ...service import blogs_service, usersservice, postservice
from .common import authenticated

bp = Blueprint('posts', __name__)
blogs_service = blogs_service.Blogs_service()
# user_service = usersservice.UsersService()      # Нннадо?
post_service = postservice.PostService()


@bp.route('/add_post/<blog_id>')
@authenticated
def add_post(blog_id):
    blog = blogs_service.find_by_id(blog_id)
    blogs = blog.user.blogs
    blogs_titles = ('Название', 'Добавить')

    return render_template('edit_post.html',
                           the_title='Хочешь добавить новый пост?',
                           the_blog_name=blog.name,
                           the_blog_id=blog.id,
                           the_blogs_titles=blogs_titles,
                           the_user_blogs=blogs,
                           the_username=session['user_name'])


@bp.route('/cancel_update_post/<blog_id>')
def cancel_update_blog(blog_id) -> 'html':
    return redirect('/blog/{}'.format(blog_id))


@bp.route('/update_post/<blog_id>', methods=['POST'])
@authenticated
def update_post(blog_id) -> 'html':
    post_service.add_post(request.form['post_title'],
                          request.form['post_content'],
                          request.form.getlist('blog_ids'))
    return redirect('/blog/{}'.format(blog_id))
