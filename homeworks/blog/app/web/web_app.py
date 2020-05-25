from flask import Flask
from .routes import base, users, auth, blogs, posts, comments
from .config import Configuration

configuration = Configuration()
app = Flask(__name__,
            template_folder=configuration.template_folder,
            static_folder=configuration.static_folder)

app.config.from_object(configuration)
app.secret_key = configuration.secret_key


app.register_blueprint(base.bp)
app.register_blueprint(users.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(blogs.bp)
app.register_blueprint(posts.bp)
app.register_blueprint(comments.bp)
