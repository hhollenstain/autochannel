import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
# from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
# from flask_mail import Mail
from autochannel.config import Config
from autochannel.database import AcDb

import logging

LOG = logging.getLogger(__name__)

# db = SQLAlchemy()
bcrypt = Bcrypt()
# login_manager = LoginManager()
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'info'
# mail = Mail()

class AcApp:

    def __init__(self):
        self.db = None

    def create_app(self, config_class=Config):
        """[summary]
        
        Keyword Arguments:
            config_class {[type]} -- [description] (default: {Config})
        
        Returns:
            [type] -- [description]
        """
        app = Flask(__name__)
        app.config.from_object(Config)
        self.db_init = AcDb(app)
        db = self.db_init.db_session()
        self.db = db

        # self.db.init_app(app)
        bcrypt.init_app(app)


        from autochannel.api.routes import mod_api
        from autochannel.site.routes import mod_site
        from autochannel.errors.routes import mod_errors
        app.register_blueprint(mod_api, url_prefix='/api')
        app.register_blueprint(mod_site)
        app.register_blueprint(mod_errors)

        LOG.info(dir(app))
        return app
    
    def create_database(self):
        LOG.info('RUNNING CREATES???')
        self.db_init.create_database()

