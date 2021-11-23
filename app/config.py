from app.settings import DevelopmentConfig as Cfg

class Config(Cfg):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:"Fuwei123321."@120.25.77.192/Bingtang_blog?charset=utf8'