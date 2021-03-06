import os

class Config:
    AC_TOKEN = os.getenv('AC_TOKEN')
    API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
    AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
    AVATAR_BASE_URL = "https://cdn.discordapp.com/avatars/"
    DEFAULT_AVATAR = "https://discordapp.com/assets/"\
                "1cbd08c76f8af6dddce02c5138971129.png"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    OAUTH2_CLIENT_ID = os.environ['OAUTH2_CLIENT_ID']
    OAUTH2_CLIENT_SECRET = os.environ['OAUTH2_CLIENT_SECRET']
    OAUTH2_REDIRECT_URI = 'http://localhost:5000/api/callback'
    SECRET_KEY = os.environ['OAUTH2_CLIENT_SECRET']
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_URL = API_BASE_URL + '/oauth2/token'
    VERSION_INFO = (0, 0, 1)
    VERSION = '.'.join(str(c) for c in VERSION_INFO)



