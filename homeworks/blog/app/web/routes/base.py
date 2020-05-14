from flask import render_template
from ..run import app


@app.route('/')
def entry_page() -> 'html':
    return render_template('index.html',
                           the_title='Привет! Это какой-то блог', )
