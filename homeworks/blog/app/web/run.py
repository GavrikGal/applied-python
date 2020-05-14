from flask import Flask, render_template
from . import config


class Web_app():
    def __init__(self):
        self.app = Flask(__name__,
            template_folder=config.template_folder,
            static_folder=config.static_folder)

        self.app.secret_key = config.secret_key
        self.app.config['dbconfig'] = config.dbconfig

app = Flask(__name__,
            template_folder=config.template_folder,
            static_folder=config.static_folder)

print(__name__)

app.secret_key = config.secret_key
app.config['dbconfig'] = config.dbconfig


@app.route('/')
def entry_page() -> 'html':
    return render_template('index.html',
                           the_title='Привет! Это какой-то блог. Запуск из run', )


print('webapp running')


if __name__ == '__main__':
    app.run()
