class BaseConfig(object):
    """配置基类"""
    """每个配置文件都需要一个SECRET_KEY"""
    SECRET_KEY = 'makesure to set a very secret key'

class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123456@mysqldb:3306/simpledu?charset=utf8'

class ProductionConfig(BaseConfig):
    """生产环境配置"""
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:gaofei123456@mysqldb:3306/simpledu?charset=utf8'

class TestingConfig(BaseConfig):
    """测试环境配置"""
    pass


configs = {
        'development' :DevelopmentConfig,
        'production':ProductionConfig,
        'testing': TestingConfig

        }
