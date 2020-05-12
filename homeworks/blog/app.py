from flask import Flask, render_template, request
from homeworks.blog.DBcm import UseDataBase, ConnectionError, CredentialsError, SQLError


app = Flask(__name__)
app.secret_key = 'SecretKey'

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'blog',
                          'password': 'blogpasswd',
                          'database': 'blogdb', }


@app.route('/')
def entry_page() -> 'html':
    return render_template('index.html',
                           the_title='Welcome to blog', )


@app.route('/users')
def users_page() -> 'html':

    try:
        with UseDataBase(app.config['dbconfig']) as cursor:
            _SQL = """SELECT id, first_name, last_name, login FROM users"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()

        titles = ('id', 'Имя', 'Фамилия', 'Логин')
        return render_template('users.html',
                               the_title='Управление пользователями',
                               the_row_title=titles,
                               the_data=contents,)
    except ConnectionError as err:
        print('Something went wrong:', str(err))
    except CredentialsError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


if __name__ == '__main__':
    app.run()
