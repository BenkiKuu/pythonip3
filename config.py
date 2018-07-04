import os


class Config:
    """
    General configuration parent class
    """
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') 
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    SECRET_KEY=os.environ.get('SECRET_KEY')


class ProdConfig(Config):
    """
    Production configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    """
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestConfig(Config):
    """
    Testing configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    """
    pass


class DevConfig(Config):
    """
    Development configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    """

    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}
