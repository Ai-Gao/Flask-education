# coding='utf-8'
class BaseConfig(object):
    """配置基类"""
    """每个配置文件都需要一个SECRET_KEY"""
    SECRET_KEY = 'makesure to set a very secret key'
 # 分页每页显示的数量通常写在配置文件中

    INDEX_PER_PAGE = 6

    ADMIN_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123@127.0.0.1:3306/simpledu?charset=utf8'

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
