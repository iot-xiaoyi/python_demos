import os

from flask import Flask
import click
from . import db
from . import auth
from . import blog

def create_app(test_config=None):
    #应用需要知道在哪里设置路径， 使用 __name__ 是一个方便的方法, 是当前模块的名称
     # instance_relative_config=True告诉应用配置文件是相对于instance folder的相对路径，
     # 实例文件夹flaskr包的外面，用于存放本地数据，不应当提交到版本控制系统
    app = Flask(__name__, instance_relative_config=True)  
    #设置一个应用的 缺省配置，在开发过程中， 为了方便可以设置SECRET_KEY为 'dev' ，但是在发布的时候应当使用一个随机值来 重载它。
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in 
        #test_config 也会被传递给工厂，并且会替代实例配置。这样可以实现 测试和开发的配置分离，相互独立
        app.config.from_mapping(test_config)
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    
    # app.register_blueprint(blog.blog_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(blog.blog_bp)

    return app

