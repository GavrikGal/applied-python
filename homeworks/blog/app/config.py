import os


base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

dbconfig = {'host': '127.0.0.1',
            'user': 'blog',
            'password': 'blogpasswd',
            'database': 'blogdb', }