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


@bp.route('/edit_post/<blog_id>/<post_id>')
@authenticated
def edit_post(blog_id, post_id):
    blog = blogs_service.find_by_id(blog_id)
    post = post_service.find_by_id(post_id)
    blogs = blog.user.blogs
    blogs_titles = ('Название', 'Добавить')
    post_blogs_ids = [blog.id for blog in post.blogs]

    return render_template('edit_post.html',
                           the_title='Хочешь изменить свой пост?',
                           the_blog_name=blog.name,
                           the_blog_id=blog.id,
                           the_blogs_titles=blogs_titles,
                           the_post_id=post.id,
                           the_post_title=post.title,
                           the_post_content=post.content,
                           the_post_blogs_ids=post_blogs_ids,
                           the_user_blogs=blogs,
                           the_username=session['user_name'])


@bp.route('/cancel_update_post/<blog_id>')
def cancel_update_blog(blog_id) -> 'html':
    return redirect('/blog/{}'.format(blog_id))


@bp.route('/cancel_update_exist_post/<blog_id>')
def cancel_update_exist_post(blog_id) -> 'html':
    return redirect('/edit_blog/{}'.format(blog_id))


@bp.route('/update_post/<blog_id>', methods=['POST'])
@authenticated
def update_post(blog_id) -> 'html':
    if request.form['post_id']:
        if not request.form.getlist('blog_ids'):
            return render_template('warning.html',
                                   the_title='Внимание!',
                                   the_message='Вы не отметили в каком блоге разместить пост, это приведет к удалению поста. Вы хотите чтобы пост был удален?',
                                   the_confirm_text='Удалить',
                                   the_confirm_href='/delete_post/{}/{}'.format(blog_id, request.form['post_id']),
                                   the_cancel_text='Отмена',
                                   the_cancel_href='/edit_post/{}/{}'.format(blog_id, request.form['post_id']))
        post_service.update_post(request.form['post_id'],
                                 request.form['post_title'],
                                 request.form['post_content'],
                                 request.form.getlist('blog_ids'))
        return redirect('/edit_blog/{}'.format(blog_id))
    else:
        post_service.add_post(request.form['post_title'],
                              request.form['post_content'],
                              request.form.getlist('blog_ids'))
        return redirect('/blog/{}'.format(blog_id))


@bp.route('/delete_post/<blog_id>/<post_id>')
@authenticated
def delete_post(blog_id, post_id):
    post_service.delete_post(post_id)
    return redirect('/edit_blog/{}'.format(blog_id))


@bp.route('/post/<blog_id>/<post_id>')
def post(blog_id, post_id):
    post = post_service.find_by_id(post_id)

    return render_template('post.html',
                           the_post=post,
                           the_comments=post.comments,
                           the_blog_id=blog_id)
