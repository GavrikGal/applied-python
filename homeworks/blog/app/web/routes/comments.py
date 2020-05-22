from flask import Blueprint, redirect, request, session, render_template
from ...service import commentservice, usersservice, postservice
from .common import authenticated


bp = Blueprint('comments', __name__)
comment_service = commentservice.CommentService()
user_service = usersservice.UsersService()
post_service = postservice.PostService()


@bp.route('/add_comment/<blog_id>/<post_id>', methods=['POST'])
@authenticated
def add_comment(blog_id, post_id):
    comment_service.add_comment(request.form['comment_text'],
                                user_service.find_by_id(session['user_id']),
                                post_service.find_by_id(post_id),
                                None)
    return redirect('/post/{}/{}'.format(blog_id, post_id))


@bp.route('/reply_comment/<blog_id>/<post_id>/<comment_id>', methods=['POST'])
@authenticated
def reply_comment(blog_id, post_id, comment_id):
    parent_comment = comment_service.find_by_id(comment_id)
    comment_service.add_comment(request.form['comment_text'],
                                user_service.find_by_id(session['user_id']),
                                None,
                                parent_comment)
    return redirect('/post/{}/{}'.format(blog_id, post_id))
