# production settings

from .base_settings import *

ALLOWED_HOSTS = [config('ALLOWED_HOSTS')]

# postgres db for heroku
DATABASES['default'] = dj_database_url.config(
    conn_max_age=600, ssl_require=True)
