from .. import config


class Configuration(object):
    secret_key = 'SecretKey'
    template_folder = config.base_dir + '\\web\\templates'
    static_folder = config.base_dir + '\\web\\static'

    dbconfig = config.dbconfig
