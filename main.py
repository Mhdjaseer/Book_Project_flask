from flask import Flask
from extensions import db,jwt
from auth import auth_bp
from view import book_bp
from admin import admin_bp
from users import user_bp
from flask_migrate import Migrate

def create_app():



    app=Flask(__name__)

    app.config.from_prefixed_env()

    # initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # registering blueprints
    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(book_bp, url_prefix='/api')
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(user_bp,url_prefix='/user')
    

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    return app