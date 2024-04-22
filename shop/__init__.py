from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
from markupsafe import Markup

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    def nl2br(value):
        return Markup(value.replace('\n', '<br>'))

    app.jinja_env.filters['nl2br'] = nl2br

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, product_views,auth_views,order_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(product_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(order_views.bp)
    
   
    
    return app