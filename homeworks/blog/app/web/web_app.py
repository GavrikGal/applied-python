from flask import Flask
from .routes import base, users, auth, blogs, posts, comments
from . import config


app = Flask(__name__,
            template_folder=config.template_folder,
            static_folder=config.static_folder)

app.secret_key = config.secret_key
app.config['dbconfig'] = config.dbconfig

app.register_blueprint(base.bp)
app.register_blueprint(users.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(blogs.bp)
app.register_blueprint(posts.bp)
app.register_blueprint(comments.bp)
