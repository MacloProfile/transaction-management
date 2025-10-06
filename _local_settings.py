DEBUG = True
ALLOWED_HOSTS = ['*']

from integration_utils.bitrix24.local_settings_class import LocalSettingsClass

DOMAIN = 'domain'


APP_SETTINGS = LocalSettingsClass(
    portal_domain='',
    app_domain=DOMAIN,
    app_name='',
    salt='',
    secret_key='',
    application_bitrix_client_id='',
    application_bitrix_client_secret='',
    application_index_path='/',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name_db',
        'USER': 'login',
        'PASSWORD': 'password',
        'HOST': 'localhost',
    },
}