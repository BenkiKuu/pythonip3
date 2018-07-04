from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config_options

app = Flask(__name__)
bootstrap = Bootstrap()
# app.config['SECRET_KEY'] = 'fb004d605b70a23de5b6681898e5ca50'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# from app import views
def create_app(config_name):
    """
    Function that takes configuration setting key as an argument
    Args:
        config_name : name of the configuration to be used
    """

    # Initialising application
    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Initialising flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # configure Uploadset
    # configure_uploads(app, photos)

    # Regestering the main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
